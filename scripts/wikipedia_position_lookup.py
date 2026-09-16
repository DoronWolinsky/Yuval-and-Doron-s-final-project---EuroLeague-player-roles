"""
Temporary side-task utility (not part of the CheckList pipeline).

Looks up the standard five-position basketball classification (Point Guard,
Shooting Guard, Small Forward, Power Forward, Center) for unique EuroLeague
players from Wikipedia, using player_id (from data/raw/players_bio.csv) as the
authoritative identifier and player names only to locate the Wikipedia page.

Not yet wired into the main notebook or merged into the project feature table.
See the side-task instructions for scope and open decisions.

Usage:
    python scripts/wikipedia_position_lookup.py --pilot
    python scripts/wikipedia_position_lookup.py --full
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata

# Windows consoles default to a legacy codepage (e.g. cp1255) that can't
# encode many Wikipedia page titles (accents, non-Latin scripts). Reconfigure
# stdout to UTF-8 once so every print() call below is safe, instead of
# wrapping each call site individually.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
except AttributeError:
    pass
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
BIO_PATH = REPO_ROOT / "data" / "raw" / "players_bio.csv"
OUTPUT_DIR = REPO_ROOT / "data" / "processed" / "wikipedia_position_lookup"
CACHE_PATH = OUTPUT_DIR / "lookup_cache.json"
LOOKUP_TABLE_PATH = OUTPUT_DIR / "wikipedia_position_lookup.csv"

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = (
    "EuroLeagueRolesResearch/0.1 "
    "(academic unsupervised-learning project on EuroLeague player roles; "
    "contact: doronew14@gmail.com)"
)
REQUEST_DELAY_SECONDS = 1.0
MAX_RETRIES = 3
TIMEOUT_SECONDS = 15

CANONICAL_POSITIONS = [
    "Point Guard",
    "Shooting Guard",
    "Small Forward",
    "Power Forward",
    "Center",
]

# Longer/more specific phrases first so "point guard" matches before a bare "guard".
POSITION_PATTERNS = [
    (re.compile(r"\bpoint[\s-]*guard\b|\bpg\b", re.IGNORECASE), "Point Guard"),
    (re.compile(r"\bshooting\s*guard\b|\bsg\b", re.IGNORECASE), "Shooting Guard"),
    (re.compile(r"\bsmall\s*forward\b|\bsf\b", re.IGNORECASE), "Small Forward"),
    (re.compile(r"\bpower\s*forward\b|\bpf\b", re.IGNORECASE), "Power Forward"),
    # "pivot" is the Spanish/French basketball term for center.
    (re.compile(r"\bcent(?:er|re)\b|\bpivot\b|\bc\b", re.IGNORECASE), "Center"),
]


# ---------------------------------------------------------------------------
# HTTP plumbing: identifiable User-Agent, rate limiting, retries.
# ---------------------------------------------------------------------------

def _api_get(params: dict) -> Optional[dict]:
    params = {**params, "format": "json"}
    url = f"{API_URL}?{urlencode(params)}"
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            time.sleep(REQUEST_DELAY_SECONDS)
            return data
        except HTTPError as e:
            last_error = e
            if e.code == 429:
                time.sleep(REQUEST_DELAY_SECONDS * 5 * attempt)
            elif 500 <= e.code < 600:
                time.sleep(REQUEST_DELAY_SECONDS * 2 * attempt)
            else:
                break  # non-transient (e.g. 400) -- retrying won't help
        except (URLError, TimeoutError) as e:
            last_error = e
            time.sleep(REQUEST_DELAY_SECONDS * 2 * attempt)
    print(f"  [warn] API request failed after retries: {last_error}")
    return None


def wiki_search(query: str, limit: int = 5) -> list[dict]:
    data = _api_get({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "srprop": "snippet",
    })
    if not data:
        return []
    return data.get("query", {}).get("search", [])


def wiki_get_wikitext(title: str) -> Optional[tuple[str, str]]:
    """Return (resolved_title, wikitext) for a page, following redirects."""
    data = _api_get({
        "action": "query",
        "titles": title,
        "redirects": 1,
        "prop": "revisions",
        "rvslots": "main",
        "rvprop": "content",
    })
    if not data:
        return None
    pages = data.get("query", {}).get("pages", {})
    for _, page in pages.items():
        if "missing" in page:
            continue
        revisions = page.get("revisions")
        if not revisions:
            continue
        content = revisions[0]["slots"]["main"].get("*", "")
        return page.get("title", title), content
    return None


# ---------------------------------------------------------------------------
# Name normalization
# ---------------------------------------------------------------------------

def normalize_name(raw_name: str) -> str:
    """Convert 'LAST, FIRST' or all-caps 'FIRST LAST' into 'First Last'."""
    raw_name = raw_name.strip()
    if "," in raw_name:
        last, first = [p.strip() for p in raw_name.split(",", 1)]
        raw_name = f"{first} {last}"
    return " ".join(word.capitalize() for word in raw_name.split())


def name_from_slug(slug: str) -> str:
    return " ".join(word.capitalize() for word in slug.split("-"))


def strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)
    )


# ---------------------------------------------------------------------------
# Infobox extraction and position normalization
# ---------------------------------------------------------------------------

INFOBOX_RE = re.compile(r"\{\{\s*Infobox\s+basketball\s+biography", re.IGNORECASE)


def extract_infobox_block(wikitext: str) -> Optional[str]:
    match = INFOBOX_RE.search(wikitext)
    if not match:
        return None
    # Track brace nesting to find the end of this template call.
    start = match.start()
    depth = 0
    i = start
    while i < len(wikitext) - 1:
        two = wikitext[i:i + 2]
        if two == "{{":
            depth += 1
            i += 2
            continue
        if two == "}}":
            depth -= 1
            i += 2
            if depth == 0:
                return wikitext[start:i]
            continue
        i += 1
    return wikitext[start:start + 4000]  # fallback if unbalanced


def extract_field_raw(infobox: str, field_name: str) -> Optional[str]:
    """Return a field's raw wikitext value, respecting [[...]] / {{...}} nesting
    so an internal '|' (e.g. a piped wikilink, or a template argument) does not
    truncate the value early."""
    header = re.search(rf"\|\s*{field_name}\s*=", infobox, re.IGNORECASE)
    if not header:
        return None
    start = header.end()
    n = len(infobox)
    i = start
    depth = 0
    while i < n:
        two = infobox[i:i + 2]
        if two in ("[[", "{{"):
            depth += 1
            i += 2
            continue
        if two in ("]]", "}}"):
            depth = max(0, depth - 1)
            i += 2
            continue
        ch = infobox[i]
        if depth == 0 and (ch == "|" or ch == "\n"):
            break
        i += 1
    raw_value = infobox[start:i].strip()
    raw_value = re.sub(r"<!--.*?-->", "", raw_value, flags=re.DOTALL).strip()
    return raw_value or None


def clean_display_value(raw_value: str) -> str:
    text = raw_value
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", text)  # [[a|b]] -> b ; [[a]] -> a
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)  # drop simple (non-nested) templates
    text = re.sub(r"<[^>]+>", "", text)  # drop stray HTML tags
    return text.strip(" \t{}").strip()


def extract_field(infobox: str, field_name: str) -> Optional[str]:
    """Backward-compatible cleaned-text accessor built on extract_field_raw."""
    raw_value = extract_field_raw(infobox, field_name)
    if raw_value is None:
        return None
    cleaned = clean_display_value(raw_value)
    return cleaned or None


def canonical_positions_in_text(text: str) -> list[str]:
    """Return the canonical positions found in `text`, ordered by where each
    first appears in the text (leftmost first) -- not by an arbitrary internal
    pattern order. This ordering is what the first-listed-position
    normalization rule relies on."""
    matches = []
    for pattern, canonical in POSITION_PATTERNS:
        m = pattern.search(text)
        if m:
            matches.append((m.start(), canonical))
    matches.sort(key=lambda item: item[0])
    ordered: list[str] = []
    for _, canonical in matches:
        if canonical not in ordered:
            ordered.append(canonical)
    return ordered


def extract_birth_year(infobox: str) -> Optional[int]:
    # Use the raw value: birth dates are usually wrapped in a
    # {{Birth date and age|YYYY|MM|DD}} template, and the year must be read
    # from inside the template's braces, not from the cleaned display text.
    birth_date_raw = extract_field_raw(infobox, "birth_date")
    if not birth_date_raw:
        return None
    match = re.search(r"(1[89]\d{2}|20\d{2})", birth_date_raw)
    return int(match.group(1)) if match else None


# Demonym / adjectival forms for nationalities as they appear in
# data/raw/players_bio.csv, so "Argentina" (bio) can be matched against
# "Argentine" (Wikipedia infobox nationality/demonym text).
NATIONALITY_ALIASES: dict[str, list[str]] = {
    "argentina": ["argentine", "argentinian"],
    "bosnia and herzegovina": ["bosnian", "herzegovinian"],
    "cote d'ivoire": ["ivorian"],
    "cote divoire": ["ivorian"],
    "ivory coast": ["ivorian"],
    "croatia": ["croatian"],
    "czech republic": ["czech"],
    "democratic republic of the congo": ["congolese"],
    "democratic republic of the congo (zaire)": ["congolese"],
    "congo": ["congolese"],
    "france": ["french"],
    "germany": ["german"],
    "greece": ["greek"],
    "iceland": ["icelandic"],
    "ireland": ["irish"],
    "netherlands": ["dutch"],
    "north macedonia": ["macedonian"],
    "poland": ["polish"],
    "puerto rico": ["puerto rican"],
    "russian federation": ["russian"],
    "spain": ["spanish"],
    "sweden": ["swedish"],
    "switzerland": ["swiss"],
    "turkiye": ["turkish", "turkey"],
    "united kingdom": ["british", "english", "scottish", "welsh"],
    "united states of america": ["american", "usa", "u.s.", "united states"],
    "denmark": ["danish"],
    "finland": ["finnish"],
    "israel": ["israeli"],
    "italy": ["italian"],
    "philippines": ["filipino", "philippine"],
    "slovakia": ["slovak"],
    "trinidad and tobago": ["trinidadian", "tobagonian"],
    "new zealand": ["new zealander", "kiwi"],
    "china": ["chinese"],
    "brazil": ["brazilian"],
    "cuba": ["cuban"],
    "chile": ["chilean"],
    "venezuela": ["venezuelan"],
    "colombia": ["colombian"],
    "mexico": ["mexican"],
    "canada": ["canadian"],
    "australia": ["australian"],
    "austria": ["austrian"],
    "belgium": ["belgian"],
    "senegal": ["senegalese"],
    "nigeria": ["nigerian"],
    "cameroon": ["cameroonian"],
    "gabon": ["gabonese"],
    "mali": ["malian"],
    "niger": ["nigerien"],
    "chad": ["chadian"],
    "guinea": ["guinean"],
    "ghana": ["ghanaian"],
    "angola": ["angolan"],
    "tunisia": ["tunisian"],
    "iran": ["iranian"],
}


def nationality_matches(expected_nationality: str, haystack: str) -> bool:
    expected = expected_nationality.strip().lower()
    haystack_lower = haystack.lower()
    candidates = {expected, *NATIONALITY_ALIASES.get(expected, [])}
    return any(c in haystack_lower for c in candidates if c)


def classify_birth_year_evidence(expected_year: Optional[int], wiki_year: Optional[int]) -> str:
    """Classify how a project birth year compares to the one extracted from a
    Wikipedia infobox. Exact matches are strong identity evidence; clear
    mismatches must never be overridden by other (weaker) signals; small
    (1-2 year) discrepancies are surfaced separately rather than silently
    treated as acceptable, since they could be a source-data error either way."""
    if expected_year is None or wiki_year is None:
        return "unavailable"
    diff = abs(expected_year - wiki_year)
    if diff == 0:
        return "exact_match"
    if diff <= 2:
        return "small_discrepancy"
    return "clear_mismatch"


# ---------------------------------------------------------------------------
# Lookup result record
# ---------------------------------------------------------------------------

@dataclass
class LookupResult:
    player_id: str
    original_name: str
    normalized_search_name: str
    selected_page_title: Optional[str] = None
    wikipedia_url: Optional[str] = None
    raw_position: Optional[str] = None
    position_wiki: Optional[str] = None
    status: str = "not_attempted"
    manual_review_reason: Optional[str] = None
    candidate_titles: str = ""
    # Operational normalization rule for this dataset: when Wikipedia's
    # infobox lists more than one playing position, position_wiki takes the
    # first one listed (see canonical_positions_in_text); this flag records
    # when that rule -- rather than a single unambiguous position -- was what
    # produced position_wiki, purely for QA/reporting purposes.
    first_position_rule_applied: bool = False
    # How the selected Wikipedia page was located: "direct" (an exact/redirect
    # title match on the search name), "search" (found via the basketball/
    # EuroLeague-context search API), or "" if no page was ever selected.
    match_method: str = ""
    # "bio_name" when players_bio.csv had first_name/last_name; "slug_fallback"
    # when the search name had to be derived from the profile slug instead.
    name_source: str = "bio_name"
    # Identity-verification evidence (QA-facing; see evaluate_candidate):
    # the birth year read from the selected page's infobox, how it compares
    # to players_bio.csv's `born` year, and -- when the page was accepted --
    # which piece of evidence justified accepting it.
    birth_year_wiki: Optional[int] = None
    birth_evidence: str = "unavailable"  # exact_match / small_discrepancy / clear_mismatch / unavailable
    identity_accept_reason: Optional[str] = None


def page_url(title: str) -> str:
    return "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")


def is_basketball_infobox(infobox_text: Optional[str], full_text: str) -> bool:
    if infobox_text is not None:
        return True
    return bool(re.search(r"basketball player", full_text, re.IGNORECASE))


def evaluate_candidate(
    title: str, wikitext: str, expected_birth_year: Optional[int],
    expected_nationality: Optional[str], match_source: str,
) -> dict:
    """Conservative identity verification for one candidate Wikipedia page.

    Evidence is read only from specific infobox fields (birth_date,
    nationality, birth_place) -- never from arbitrary infobox/prose text --
    so a country name that merely appears in a league name, team name, or
    career history is never treated as identity evidence.

    Verification hierarchy (a false 'unresolved' is preferred to assigning
    another person's position to a player):
      1. If both sides have a birth year and they clearly differ (>2 years):
         reject outright. Nationality can never override this.
      2. If both sides have a birth year and it matches exactly: accept.
      3. If both sides have a birth year but differ by 1-2 years: reject,
         but classify distinctly ("small_discrepancy") for manual inspection
         rather than silently deciding it is fine.
      4. If a birth year isn't available on both sides: fall back to an
         explicit nationality-field match, or -- lacking even that -- a
         direct/exact title hit with no contradicting evidence at all.
      5. Otherwise: insufficient evidence, reject.
    """
    infobox = extract_infobox_block(wikitext)
    is_bball = is_basketball_infobox(infobox, wikitext[:3000])
    result = {
        "is_basketball": is_bball,
        "infobox": infobox,
        "birth_year_wiki": None,
        "birth_evidence": "unavailable",
        "nationality_text": None,
        "birth_place_text": None,
        "nat_field_match": False,
        "decision": "reject_not_basketball",
        "accept_reason": None,
    }
    if not is_bball:
        return result

    birth_year_wiki = extract_birth_year(infobox) if infobox else None
    nationality_text = extract_field(infobox, "nationality") if infobox else None
    birth_place_text = extract_field(infobox, "birth_place") if infobox else None
    birth_evidence = classify_birth_year_evidence(expected_birth_year, birth_year_wiki)

    # Nationality evidence is scoped strictly to the nationality/birth_place
    # FIELD values -- not the whole infobox -- so a league/team name that
    # happens to contain a country word is never mistaken for identity
    # evidence (the root cause of the Devin Booker false match).
    nat_hay = " ".join(t for t in (nationality_text, birth_place_text) if t)
    nat_field_match = bool(expected_nationality) and bool(nat_hay) and nationality_matches(
        expected_nationality, nat_hay
    )

    result.update({
        "birth_year_wiki": birth_year_wiki,
        "birth_evidence": birth_evidence,
        "nationality_text": nationality_text,
        "birth_place_text": birth_place_text,
        "nat_field_match": nat_field_match,
    })

    if birth_evidence == "clear_mismatch":
        result["decision"] = "reject_clear_mismatch"
        return result

    if birth_evidence == "exact_match":
        result["decision"] = "accept"
        result["accept_reason"] = "exact_birth_year"
        return result

    if birth_evidence == "small_discrepancy":
        result["decision"] = "reject_small_discrepancy"
        return result

    # birth_evidence == "unavailable": conservative fallback evidence only.
    if nat_field_match:
        result["decision"] = "accept"
        result["accept_reason"] = "nationality_field"
        return result

    if match_source == "direct":
        # An exact/redirect title hit on our normalized name, with no
        # birth year or nationality evidence available to contradict it, is
        # treated as a sufficiently specific name match.
        result["decision"] = "accept"
        result["accept_reason"] = "direct_name_match_no_contradicting_evidence"
        return result

    result["decision"] = "reject_insufficient_evidence"
    return result


def lookup_player(
    player_id: str, first_name: Optional[str], last_name: Optional[str],
    slug_used: Optional[str], born: Optional[str], nationality: Optional[str],
) -> LookupResult:
    if isinstance(first_name, str) and isinstance(last_name, str) and first_name and last_name:
        original_name = f"{last_name.strip()}, {first_name.strip()}"
        search_name = normalize_name(original_name)
        name_source = "bio_name"
    elif isinstance(slug_used, str) and slug_used:
        original_name = slug_used
        search_name = name_from_slug(slug_used)
        name_source = "slug_fallback"
    else:
        result = LookupResult(
            player_id=player_id, original_name="", normalized_search_name="",
            status="no_usable_name",
            manual_review_reason="players_bio.csv has neither a name nor a slug for this player_id",
        )
        return result

    result = LookupResult(
        player_id=player_id, original_name=original_name,
        normalized_search_name=search_name, name_source=name_source,
    )

    expected_birth_year = None
    if isinstance(born, str) and born:
        m = re.match(r"(\d{4})", born)
        if m:
            expected_birth_year = int(m.group(1))
    expected_nationality = nationality if isinstance(nationality, str) and nationality else None

    print(f"  searching: {search_name!r} (player_id={player_id})")

    # Candidates: (title, source) -- try a direct/exact title lookup first
    # (handles the common case where the page title is the plain name, or a
    # redirect resolves diacritics for us), then fall back to context search.
    candidates: list[tuple[str, str]] = []
    seen_titles: set[str] = set()
    direct_fetch = wiki_get_wikitext(search_name)
    prefetched: dict[str, tuple[str, str]] = {}
    if direct_fetch:
        resolved_title, wikitext = direct_fetch
        candidates.append((resolved_title, "direct"))
        seen_titles.add(resolved_title)
        prefetched[resolved_title] = (resolved_title, wikitext)

    search_hits = wiki_search(f"{search_name} basketball EuroLeague")
    if not search_hits:
        search_hits = wiki_search(f"{search_name} basketball player")
    for hit in search_hits[:5]:
        title = hit["title"]
        if title not in seen_titles:
            candidates.append((title, "search"))
            seen_titles.add(title)

    if not candidates:
        result.status = "no_page_found"
        result.manual_review_reason = "Wikipedia search returned no results"
        return result

    result.candidate_titles = "; ".join(c[0] for c in candidates)

    # Fetch candidates lazily and stop as soon as one is ACCEPTED under the
    # conservative verification hierarchy in evaluate_candidate. This keeps
    # the full-run cost down (most players settle on the first or second
    # candidate) while still trying further candidates -- including a fresh
    # search result -- whenever the current one is rejected.
    evaluated = []  # (resolved_title, wikitext, evaluation, source)
    for title, src in candidates:
        fetched = prefetched.get(title) or wiki_get_wikitext(title)
        if not fetched:
            continue
        resolved_title, wikitext = fetched
        evaluation = evaluate_candidate(
            resolved_title, wikitext, expected_birth_year, expected_nationality, src
        )
        evaluated.append((resolved_title, wikitext, evaluation, src))
        if evaluation["decision"] == "accept":
            break

    basketball_candidates = [c for c in evaluated if c[2]["is_basketball"]]

    if not basketball_candidates:
        result.status = "page_found_not_basketball_player"
        result.manual_review_reason = (
            "Wikipedia page(s) found but none identifiable as a basketball-biography page"
        )
        if evaluated:
            result.selected_page_title = evaluated[0][0]
            result.wikipedia_url = page_url(evaluated[0][0])
            result.match_method = evaluated[0][3]
        return result

    accepted = [c for c in basketball_candidates if c[2]["decision"] == "accept"]

    if not accepted:
        # No candidate passed verification. Report the most informative
        # rejection reason, preferring a confirmed mismatch (we know it's a
        # different person) over a merely inconclusive one.
        def _priority(c):
            order = {"reject_clear_mismatch": 0, "reject_small_discrepancy": 1}
            return order.get(c[2]["decision"], 2)

        best = sorted(basketball_candidates, key=_priority)[0]
        title, wikitext, evaluation, src = best
        result.selected_page_title = title
        result.wikipedia_url = page_url(title)
        result.match_method = src
        result.birth_year_wiki = evaluation["birth_year_wiki"]
        result.birth_evidence = evaluation["birth_evidence"]

        if evaluation["decision"] == "reject_clear_mismatch":
            result.status = "page_found_identity_mismatch"
            result.manual_review_reason = (
                f"Selected page's birth year ({evaluation['birth_year_wiki']}) clearly differs "
                f"from players_bio.csv ({expected_birth_year}); rejected as a different person."
            )
        elif evaluation["decision"] == "reject_small_discrepancy":
            result.status = "birth_year_small_discrepancy"
            result.manual_review_reason = (
                f"Birth year differs by 1-2 years (players_bio.csv={expected_birth_year}, "
                f"wikipedia={evaluation['birth_year_wiki']}); not auto-accepted, flagged for review."
            )
        elif len(basketball_candidates) > 1:
            result.status = "ambiguous_multiple_pages"
            result.manual_review_reason = (
                f"{len(basketball_candidates)} basketball-player Wikipedia pages found; "
                "none confirmed by birth year, a nationality-field match, or a direct name match."
            )
        else:
            result.status = "page_found_identity_unconfirmed"
            result.manual_review_reason = (
                "Basketball page found but identity could not be confirmed via birth year, "
                "a nationality-field match, or a direct name match."
            )
        return result

    title, wikitext, evaluation, src = accepted[0]
    result.selected_page_title = title
    result.wikipedia_url = page_url(title)
    result.match_method = src
    result.birth_year_wiki = evaluation["birth_year_wiki"]
    result.birth_evidence = evaluation["birth_evidence"]
    result.identity_accept_reason = evaluation["accept_reason"]

    infobox = evaluation["infobox"]
    # Retired players' infoboxes commonly repurpose 'position' for a post-playing
    # role (e.g. "Sporting director", "Head coach"); their actual playing
    # position, if still documented, lives in 'career_position'. Prefer that
    # field when present, and only fall back to 'position' otherwise.
    raw_position = None
    if infobox:
        raw_position = extract_field(infobox, "career_position") or extract_field(infobox, "position")
    result.raw_position = raw_position

    if not raw_position:
        result.status = "position_unavailable"
        result.manual_review_reason = "Basketball page confirmed but has no 'position' field in its infobox"
        return result

    # Operational normalization rule: when Wikipedia explicitly lists more than
    # one playing position, take the first canonical position listed in the
    # text (leftmost in raw_position), rather than sending the player to
    # manual review. The complete original text is preserved in raw_position.
    positions_found = canonical_positions_in_text(raw_position)
    if positions_found:
        result.position_wiki = positions_found[0]
        result.status = "matched"
        result.first_position_rule_applied = len(positions_found) > 1
    else:
        result.status = "position_text_unrecognized"
        result.manual_review_reason = f"Could not map position text to a canonical position: {raw_position!r}"

    return result


# ---------------------------------------------------------------------------
# Cache (resumability)
# ---------------------------------------------------------------------------

def load_cache() -> dict:
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp_path = CACHE_PATH.with_suffix(".json.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    # os.replace can transiently fail on Windows (e.g. antivirus/indexer
    # briefly holding the file); retry a few times before falling back to a
    # direct (non-atomic) write so one flaky rename doesn't abort the run.
    for attempt in range(5):
        try:
            tmp_path.replace(CACHE_PATH)
            return
        except OSError:
            time.sleep(0.3 * (attempt + 1))
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    try:
        tmp_path.unlink()
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def load_unique_players() -> pd.DataFrame:
    bio = pd.read_csv(BIO_PATH)
    assert bio["player_id"].is_unique, "players_bio.csv is expected to have one row per player_id"
    return bio


def run_lookups(player_ids: list[str], bio: pd.DataFrame) -> list[LookupResult]:
    cache = load_cache()
    results = []
    bio_indexed = bio.set_index("player_id")
    for i, pid in enumerate(player_ids, 1):
        if pid in cache:
            print(f"[{i}/{len(player_ids)}] {pid}: using cached result")
            results.append(LookupResult(**cache[pid]))
            continue
        row = bio_indexed.loc[pid]
        print(f"[{i}/{len(player_ids)}] {pid}: looking up")
        result = lookup_player(
            player_id=pid,
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
            slug_used=row.get("slug_used"),
            born=row.get("born"),
            nationality=row.get("nationality"),
        )
        results.append(result)
        cache[pid] = asdict(result)
        save_cache(cache)
    return results


def revalidate_matched_players(bio: pd.DataFrame, limit: Optional[int] = None) -> dict:
    """Re-verify every currently 'matched' player's SELECTED page under the
    corrected (conservative) identity-verification hierarchy.

    Cheap path: re-fetch only the already-selected page (one request) and
    re-run evaluate_candidate on it. If it still passes, keep it (recomputing
    position deterministically from the same infobox).

    If it now fails, the previously selected page is wrong (or no longer
    confidently confirmable) -- re-run the normal direct+search lookup_player
    flow fresh for that player, so a real alternative candidate can still be
    found rather than blindly discarding the player. Progress is cached and
    resumable via a per-record "_revalidated" marker, same as the main run.
    """
    cache = load_cache()
    bio_indexed = bio.set_index("player_id")
    matched_ids = [
        pid for pid, rec in cache.items()
        if rec.get("status") == "matched" and not rec.get("_revalidated")
    ]
    if limit is not None:
        matched_ids = matched_ids[:limit]

    summary = {
        "checked": 0, "kept_same_page": 0, "failed_verification": 0,
        "recovered_via_research": 0, "became_unresolved": 0, "position_changed": 0,
    }

    for i, pid in enumerate(matched_ids, 1):
        rec = cache[pid]
        row = bio_indexed.loc[pid]
        born = row.get("born")
        expected_birth_year = None
        if isinstance(born, str) and born:
            m = re.match(r"(\d{4})", born)
            if m:
                expected_birth_year = int(m.group(1))
        expected_nationality = row.get("nationality") if isinstance(row.get("nationality"), str) else None

        title = rec.get("selected_page_title")
        old_position = rec.get("position_wiki")
        print(f"[{i}/{len(matched_ids)}] revalidating {pid} ({title})")
        summary["checked"] += 1

        fetched = wiki_get_wikitext(title) if title else None
        if fetched:
            resolved_title, wikitext = fetched
            evaluation = evaluate_candidate(
                resolved_title, wikitext, expected_birth_year, expected_nationality,
                rec.get("match_method") or "search",
            )
        else:
            evaluation = {"decision": "reject_insufficient_evidence", "is_basketball": False, "infobox": None}

        if evaluation["decision"] == "accept":
            infobox = evaluation["infobox"]
            raw_position = None
            if infobox:
                raw_position = extract_field(infobox, "career_position") or extract_field(infobox, "position")
            rec["raw_position"] = raw_position
            rec["birth_year_wiki"] = evaluation.get("birth_year_wiki")
            rec["birth_evidence"] = evaluation.get("birth_evidence", "unavailable")
            rec["identity_accept_reason"] = evaluation.get("accept_reason")
            if raw_position:
                positions_found = canonical_positions_in_text(raw_position)
                if positions_found:
                    rec["position_wiki"] = positions_found[0]
                    rec["status"] = "matched"
                    rec["first_position_rule_applied"] = len(positions_found) > 1
                    rec["manual_review_reason"] = None
                else:
                    rec["position_wiki"] = None
                    rec["status"] = "position_text_unrecognized"
                    rec["manual_review_reason"] = f"Could not map position text to a canonical position: {raw_position!r}"
            else:
                rec["position_wiki"] = None
                rec["status"] = "position_unavailable"
                rec["manual_review_reason"] = "Basketball page confirmed but has no 'position' field in its infobox"
            rec["_revalidated"] = True
            cache[pid] = rec
            summary["kept_same_page"] += 1
            if rec["position_wiki"] != old_position:
                summary["position_changed"] += 1
        else:
            summary["failed_verification"] += 1
            fresh = lookup_player(
                player_id=pid, first_name=row.get("first_name"), last_name=row.get("last_name"),
                slug_used=row.get("slug_used"), born=born, nationality=row.get("nationality"),
            )
            fresh_dict = asdict(fresh)
            fresh_dict["_revalidated"] = True
            fresh_dict["_previous_page_rejected"] = title
            fresh_dict["_previous_position_wiki"] = old_position
            cache[pid] = fresh_dict
            if fresh.status == "matched":
                summary["recovered_via_research"] += 1
            else:
                summary["became_unresolved"] += 1
            if fresh.position_wiki != old_position:
                summary["position_changed"] += 1

        save_cache(cache)

    return summary


PILOT_PLAYER_IDS = [
    "P005928",  # Facundo Campazzo -- clear single-position page
    "PJDR",     # Milos Teodosic -- Wikipedia lists two positions
    "PLRU",     # Marko Simonovic (Serbia, b.1986) -- ambiguous shared name
    "P012711",  # Marko Simonovic (Montenegro, b.1999) -- ambiguous shared name
    "P005929",  # Luka Doncic -- direct ASCII name != accented Wikipedia title
    "A15DSO",   # Octavio Da Silveira -- expected: no usable Wikipedia page
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", action="store_true", help="Run only the small pilot sample")
    parser.add_argument("--full", action="store_true", help="Run the lookup for every unique player")
    parser.add_argument(
        "--revalidate", action="store_true",
        help="Re-verify every cached 'matched' player's selected page under the corrected identity logic",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Process at most this many not-yet-cached (or not-yet-revalidated) players, then stop",
    )
    args = parser.parse_args()

    bio = load_unique_players()

    if args.revalidate:
        summary = revalidate_matched_players(bio, limit=args.limit)
        print("\nRevalidation summary:", summary)
        cache = load_cache()
        rows = [LookupResult(**{k: v for k, v in cache[pid].items() if not k.startswith("_")}) for pid in bio["player_id"].tolist()]
        df = pd.DataFrame([asdict(r) for r in rows])
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(LOOKUP_TABLE_PATH, index=False)
        print(f"Wrote {len(df)} rows to {LOOKUP_TABLE_PATH}")
        return

    if args.full:
        player_ids = bio["player_id"].tolist()
    else:
        player_ids = PILOT_PLAYER_IDS

    if args.limit is not None:
        cache = load_cache()
        pending = [pid for pid in player_ids if pid not in cache]
        player_ids = [pid for pid in player_ids if pid in cache] + pending[: args.limit]

    results = run_lookups(player_ids, bio)

    df = pd.DataFrame([asdict(r) for r in results])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / ("pilot_results.csv" if not args.full else "wikipedia_position_lookup.csv")
    df.to_csv(out_path, index=False)
    print(f"\nWrote {len(df)} rows to {out_path}")
    summary = df[["player_id", "normalized_search_name", "selected_page_title", "raw_position", "position_wiki", "status"]].to_string(index=False)
    try:
        print(summary)
    except UnicodeEncodeError:
        print(summary.encode("ascii", errors="backslashreplace").decode("ascii"))


if __name__ == "__main__":
    main()
