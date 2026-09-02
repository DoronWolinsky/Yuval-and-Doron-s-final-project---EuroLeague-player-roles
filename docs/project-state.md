# Project State

Living document. Read this together with `README.md` and `CLAUDE.md` before starting any
task. This file is the source of truth for status, decisions, and open questions — update it
whenever an important decision is made or a task completes.

## Research goal

Use unsupervised machine learning to discover natural groups of EuroLeague players based on
observed playing style and statistical behavior, as an alternative to fixed traditional
position labels.

## Research question

Can natural EuroLeague player roles be discovered from performance data without relying on
traditional position labels such as Guard, Forward, and Center?

The goal is **not** to predict a player's traditional position. Traditional position labels
must not be used as input features during clustering. They may only be used after clustering
for external comparison, cluster interpretation, measuring overlap between discovered roles
and traditional positions, and demonstrating whether discovered roles capture distinctions
traditional positions do not.

## Intended unit of observation

**player-season-team**, for the final model. The same player may appear multiple times
(different seasons and/or teams); these are not automatically treated as duplicates, since a
player's role may change between seasons or teams.

## Data inventory

| File | Path | Granularity | Role |
|---|---|---|---|
| `euroleague_players.csv` | `data/raw/euroleague_players.csv` | one row per player-season-team | Source of truth for season-level statistics: playing time, shooting volume/efficiency, playmaking, rebounding, steals, blocks, turnovers, fouls. |
| `euroleague_points.csv` | `data/raw/euroleague_points.csv` | one row per recorded shot/scoring-related event | Source of truth for shot/action types, outcomes, coordinates, zones, and available shot-context indicators. |
| `players_bio.csv` | `data/raw/players_bio.csv` | one row per player | Source of truth for height, traditional position, nationality, birth date, and scraping status. Scraped `club_code`/`club_name` reflect the club **at scraping time** and must not replace historical `team_id`. |
| `merged_euroleague_players.csv` | `data/processed/merged_euroleague_players.csv` | one row per enriched event | Existing derived artifact (event data + bio columns joined on `player_id`). Not an independent raw source; a reproducible pipeline should rebuild derived data from the three raw files. |

## Previously completed work

- Initial feasibility analysis based on shot types, shot distribution, shooting percentages,
  shot coordinates, shot distance, player height, and action volume.
- A Gaussian Mixture Model was fitted; BIC was used to evaluate the number of clusters.
- An initial run on a 50% sample produced **eight clusters** (preliminary — not assumed to
  hold after the feature set and unit of observation change).
- Enrichment of the original data with additional player information via Playwright web
  scraping (`players_bio.csv`).

## Supervisor feedback

Approved by supervisor **Zeev Kalyuzhner**. Praised: enrichment via web scraping (Playwright),
the GMM + BIC methodology, the initial 8-cluster result, and the potential to challenge
traditional position classifications.

Recommended (not yet started — each requires separate approval before beginning):

1. Expand the feature set to include playmaking, rebounding, and defensive statistics
   (assists, rebounds, steals, blocks).
2. Interpret resulting clusters and assign meaningful basketball role names based on cluster
   profiles and representative players.
3. Create a 2D PCA visualization of players colored by cluster.

## Current active task

**Player-season-team feature table — completed.** Built directly inside
`notebooks/EuroLeague_Player_Roles_Project.ipynb` (appended after the user's manually edited
content, which was preserved exactly as-is and re-read from disk before this task began). The
notebook now has 63 cells. See "Player-season-team feature table" below for the full result.

This produced `data/processed/player_season_team_features.csv` — a complete, one-row-per-
player-season-team table with season totals, per-36 rates, shooting-mix shares, and shot-
location statistics. **This is not yet the training matrix.** No statistical imputation,
scaling, PCA, or clustering has been performed, and no eligible training sample has been
selected yet.

**`notebooks/EuroLeague_Player_Roles_Project.ipynb`** remains the main project notebook —
written in first person plural, in the students' own voice, read as one continuous research
narrative with no visible task boundaries. This is the notebook to read, present from, and
extend with future work. **Always re-read it from disk before starting a new notebook task —
it may have been edited by hand since the last recorded state.**

`notebooks/01_data_audit.ipynb` and `notebooks/02_coordinate_system_analysis.ipynb` remain
**internal source material / working notes** — they contain the fuller diagnostic detail that
informed the main notebook but that a supervisor does not need to see, and their old
report-style wording must not be pulled back into the main notebook. They are not deleted and
not further edited; treat them as an archive, not as something to present or extend.

## Player-season-team feature table

- **File:** `data/processed/player_season_team_features.csv`
- **Shape:** 6,307 rows x 76 columns — one row per `season_player_id`, keyed on
  `season_code + player_id + team_id` (both confirmed unique after the join).
- **Data dictionary:** `outputs/tables/player_season_team_feature_dictionary.csv` (76 rows,
  one per feature-table column: group, source, definition, calculation, missing-value
  meaning, intended use, and a preliminary `eligible_for_clustering` status —
  `candidate`/`exclude`/`comparison_only`/`quality_flag`/`undecided` — not a final list).
- **Supporting table:** `outputs/tables/season_vs_event_shot_attempt_comparison.csv` — compares
  season-total vs. event-derived field-goal attempt counts per player-season-team. Result:
  6,306 of 6,307 rows match exactly; the single mismatch (`E2017`, player `P008003`, team
  `KHI`) has an event count 15 shots higher than the season total and is left undocumented-but-
  flagged rather than resolved. Season totals are used for volume features; event data is used
  only for coordinate/zone features.
- **Feature groups:** identifiers; descriptive/comparison (`height_cm`, `position`,
  `nationality`, `born`); participation & coverage flags (`has_positive_minutes`,
  `has_positive_games`, `has_event_data`, `has_valid_spatial_data`, and shot-count columns);
  season totals plus 12 per-36 rate columns (derived from totals, not from the provided
  `minutes_per_game`); shooting-mix shares (season- and event-derived, including
  `free_throw_attempt_rate`); coordinate/zone spatial summaries (mean/median/std lateral,
  longitudinal, and raw distance from the `(0,0)` basket estimate, plus one attempt share per
  observed `zone` letter `A`-`J`); `valuation`/`plus_minus` retained but marked excluded.
- **Coverage:** 459 rows have `has_event_data = False` (zero shot events **and** zero
  field-goal attempts in the season totals — confirmed to be extremely low-participation
  players, not a data gap). A further 14 rows have `has_event_data = True` but
  `has_valid_spatial_data = False` (free-throw events only, no field-goal attempts) — a
  distinction not previously documented. 5,834 rows have usable spatial statistics.
- **No imputation performed.** `height_cm` (27 missing), `position` (54 missing), all
  undefined per-36/share values (denominator 0), and all spatial features for the 473 rows
  without valid shots are left as `NaN`. Standard deviations are `NaN` for the 126
  player-season-team groups with exactly one valid shot (undefined, not zero).
- **No eligible training sample defined yet.** The provisional 300-minutes/10-games
  participation rule mentioned during this task was used only to reason about the 459-row
  group, not applied as a filter — no rows were removed from the feature table.

## Approved decisions

- Repository structure as defined in `README.md` / `CLAUDE.md`.
- Data files remain at their canonical paths under `data/raw/` and `data/processed/`; none
  were copied or renamed (no `(3)`-suffixed uploads were present — see Data Audit notebook
  Section 1 execution log / completion report).
- `RANDOM_STATE = 42` used for all deterministic sampling.
- Tolerance of `0.01` used for per-game-vs-total float consistency checks in
  `euroleague_players.csv` (values appear rounded to two decimals in the source).
- Notebooks resolve the repository root at runtime and use `pathlib.Path`-based
  repository-relative paths — no hardcoded absolute local paths.
- The main project notebook (`notebooks/EuroLeague_Player_Roles_Project.ipynb`) is a
  supervisor-facing deliverable written in the students' own voice — see `CLAUDE.md` § "The
  project notebook is a student deliverable, not an agent report" for the full writing rules.
  Report-style scaffolding ("What is being checked", "Decision Required Before Continuing",
  "Objective/Interpretation" labels, etc.) must not appear there; that style is confined to
  internal source notebooks and this file.
- The notebook must read as one continuous narrative with **no visible task boundaries**: no
  "Setup"/"What This Notebook Covers"/"What's Next"/"Task Summary"-style sections, and no
  announcing or proposing future work inside the notebook — the next task comes directly
  through Claude Code. New work continues naturally from the previous result instead.
- No meta-explanations of ordinary notebook mechanics (imports, path resolution, helper
  functions, export code, random seeds, notebook execution) — setup code may stay, but
  doesn't need its own Markdown explanation unless it embeds a research-relevant choice.
- One continuous main project notebook is maintained going forward, rather than a new
  standalone notebook per task.
- The notebook file on disk is always authoritative, including over anything described in an
  earlier conversation or in this document — the user may edit it by hand at any time. Always
  re-read it before a new notebook task, never recreate a section the user removed, and never
  overwrite manually revised prose with older generated wording.
- Shot-attempt subset of `euroleague_points.csv` defined as `action_id` in
  `{2FGA, 2FGAB, 2FGM, 3FGA, 3FGAB, 3FGM, DUNK, LAYUPATT, LAYUPMD}` (all field-goal attempt
  codes), explicitly excluding `FTM` (free throws, which carry a constant `(-1, -1)`
  coordinate sentinel, not a real location).
- Basket location estimate for coordinate-derived work: **`(coord_x=0, coord_y=0)`**
  (medium-high confidence; empirically derived, not from documentation — see below).
- `coord_x` = lateral offset from the basket; `coord_y` = longitudinal distance from the
  basket toward half-court (high confidence).
- Coordinates represent a single, shared, per-shot basket reference (one normalized
  half-court), not two mirrored court ends, and are not team- or game-specific (high
  confidence).

## Open questions

Status after the feature-table task:

1. ~~Coordinate system for `coord_x`/`coord_y`~~ — **resolved**, see "Coordinate System
   Analysis — conclusions" below.
2. **Treatment of the 459 player-season-team rows with no matching event data** —
   **addressed in the feature table, not fully resolved**: they are kept, flagged via
   `has_event_data = False`, and left with missing shot-location features (not filled). The
   remaining decision is whether they (and the 14 free-throw-only rows) are excluded from the
   final training sample via a participation threshold — not yet applied anywhere; none of
   the 459 would meet an illustrative 300-minutes/10-games bar, checked in the notebook.
3. **Usefulness of `timestamp`** in `euroleague_points.csv` — still open; not used in the
   feature table at all (left out of the built table entirely rather than resolved).
4. **Treatment of `valuation` and `plus_minus`** — **decided for now**: both are retained in
   the feature table for reference but explicitly marked `exclude` in the data dictionary
   (`outputs/tables/player_season_team_feature_dictionary.csv`), i.e. not treated as
   clustering candidates.
5. **Handling of missing `height_cm`/`position`**: **decided for now, not finalized** — both
   are left unfilled in the feature table (27 and 54 missing respectively). No imputation
   method has been implemented; the provisional plan (median height within the eligible
   sample once one is chosen, no position imputation ever) is documented in the notebook and
   in the feature-table entry below.
6. **Minimum shot-attempt / participation threshold** for the eligible training sample and
   for distributional coordinate features (`spatial_spread`, `zone_entropy`) — still not
   defined; needed before any imputation or sample-selection step.
7. **Physical-unit (centimeter) interpretation of raw coordinate units** — still only
   moderately confident; the feature table stores distances in raw coordinate units only, not
   centimeters.
8. **93 shot-attempt rows sharing the `FTM` sentinel coordinate `(-1, -1)`** —
   **resolved for the feature table**: excluded from spatial/zone aggregation (not deleted
   from raw data), consistent with excluding `FTM` rows themselves.

## Coordinate System Analysis — conclusions

Full evidence, confidence levels, and consequences are in
`notebooks/02_coordinate_system_analysis.ipynb` Section 14 and
`outputs/tables/coordinates/coordinate_decisions.csv`. Summary:

- `coord_x` = lateral offset from the basket (**high** confidence); `coord_y` = longitudinal
  distance from the basket toward half-court (**high** confidence).
- Basket location estimate: `(0, 0)` (**medium-high** confidence; empirical, not documented).
- Single, normalized half-court representation, shared across both teams per shot — no
  team/game mirroring (**high** confidence, tested at both dataset and per-game level).
- Coordinate convention (scale/sign/range) is stable across all 19 seasons (**high**
  confidence); `action_id` taxonomy and `zone` completeness are **not** stable — the dataset
  has three distinct action-taxonomy eras (`E2007`: 7 action codes; `E2008-E2014`: 10 codes
  including `DUNK`/`LAYUPATT`/`LAYUPMD`/blocked variants; `E2015-E2016`: back to 7;
  `E2017-E2025`: 5 codes only) — a genuinely new finding, not previously documented.
- `zone` missingness (141,019 rows project-wide, per the Data Audit) is now explained: it is
  almost entirely (140,926 of 141,019) attributable to `FTM` free-throw rows, which
  structurally have no zone; only 93 of 614,219 shot-attempt rows have a missing zone.
  `zone` is a reliable, spatially coherent field for shot-attempt rows.
- Euclidean shot distance from `(0,0)` is reliable in **relative** terms; physical-unit
  (centimeter) conversion is only **moderately** supported (see open question 7 above).
- 11 of 13 proposed coordinate-derived features are marked safe for a future Feature
  Engineering task; 2 (`spatial_spread`, `zone_entropy`) are postponed pending open question 6.
  Full list: `outputs/tables/coordinates/proposed_coordinate_features.csv`.

## Known data issues

Full, itemized, severity-rated list is in `outputs/tables/audit_issues.csv` (generated by
`notebooks/01_data_audit.ipynb`). Categories covered: missing biography data
(`height_cm`, `position`) concentrated around failed/partial scrapes; event-context columns
(`zone`, `fastbreak`, `second_chance`, `points_off_turnover`) with non-trivial missingness,
checked by season for a data-collection-era pattern; the season-level-vs-event-level
player-season-team coverage gap; the `timestamp` placeholder-value concentration; and any
season-level range/consistency violations found (see notebook Section 6.1). Refer to the
notebook and the exported tables for exact, measured counts rather than this summary.

## Future tasks (not yet approved)

Each requires separate, explicit approval before starting:

1. **Eligible training-sample selection and imputation** — define the participation
   threshold (e.g. minimum minutes/games), select the eligible player-season-team rows from
   `data/processed/player_season_team_features.csv`, and only then apply median height
   imputation within that sample (never using `position`). This is the natural next step
   after the completed feature table; resolves open questions 5 and 6 above.
2. **Final feature selection, scaling, and `X` matrix construction** — decide which
   `candidate`-tagged columns in the feature dictionary actually go into the clustering
   input, handle any remaining correlated/redundant columns (e.g. `total_rebounds` vs.
   offensive+defensive), and build the scaled training matrix. Not started.
3. PCA (2D visualization, supervisor recommendation 3) and clustering (GMM/BIC or otherwise)
   on the final feature set — re-evaluate cluster count; do not assume 8 clusters carries
   over.
4. Cluster interpretation and role naming (supervisor recommendation 2).
5. Expand features to include additional playmaking/rebounding/defensive detail if needed
   beyond what is already in the feature table (supervisor recommendation 1 — largely
   satisfied already by the per-36 rate columns).
6. Traditional-position comparison/overlap analysis (post-hoc only).
7. Hebrew 40-minute presentation (separate future deliverable, out of scope until requested).

## Files created during the Data Audit task

- `notebooks/01_data_audit.ipynb`
- `CLAUDE.md`
- `README.md`
- `docs/project-state.md`
- `requirements.txt`
- `outputs/tables/dataset_overview.csv`
- `outputs/tables/missing_values_summary.csv`
- `outputs/tables/missing_by_season_event_context.csv`
- `outputs/tables/range_check_summary_euroleague_players.csv`
- `outputs/tables/coordinate_stats.csv`
- `outputs/tables/action_id_action_crosstab.csv`
- `outputs/tables/height_audit_summary.csv`
- `outputs/tables/season_coverage_summary.csv`
- `outputs/tables/key_integrity_summary.csv`
- `outputs/tables/join_coverage_summary.csv`
- `outputs/tables/candidate_columns_for_research.csv`
- `outputs/tables/audit_issues.csv`
- `outputs/figures/missing_values_players_bio.png`
- `outputs/figures/missing_values_euroleague_points.png`
- `outputs/figures/missing_values_euroleague_players.png`
- `outputs/figures/missing_values_merged.png`
- `outputs/figures/missing_by_season_event_context.png`
- `outputs/figures/coordinate_distributions.png`
- `outputs/figures/height_distribution.png`
- `outputs/figures/height_by_position_descriptive.png`

## Files created during the Coordinate System Analysis task

- `notebooks/02_coordinate_system_analysis.ipynb`
- `outputs/tables/coordinates/coordinate_summary.csv`
- `outputs/tables/coordinates/coordinate_summary_by_season.csv`
- `outputs/tables/coordinates/coordinate_missingness_by_season.csv`
- `outputs/tables/coordinates/action_coordinate_coverage.csv`
- `outputs/tables/coordinates/zone_coordinate_summary.csv`
- `outputs/tables/coordinates/coordinate_candidate_baskets.csv`
- `outputs/tables/coordinates/coordinate_decisions.csv`
- `outputs/tables/coordinates/proposed_coordinate_features.csv`
- `outputs/figures/coordinates/coord_histograms.png`
- `outputs/figures/coordinates/coord_boxplots.png`
- `outputs/figures/coordinates/coord_scatter_sample.png`
- `outputs/figures/coordinates/coord_hexbin_full.png`
- `outputs/figures/coordinates/made_vs_missed_overlay.png`
- `outputs/figures/coordinates/twopt_vs_threept_scatter.png`
- `outputs/figures/coordinates/twopt_threept_density_overlay.png`
- `outputs/figures/coordinates/coord_y_bimodality_check.png`
- `outputs/figures/coordinates/coord_by_season_small_multiples.png`
- `outputs/figures/coordinates/coord_by_game_team.png`
- `outputs/figures/coordinates/coord_by_zone.png`
- `CLAUDE.md` (updated at the time — later revised again, see below)
- `docs/project-state.md` (this file, updated)

## Files created/updated during the notebook consolidation task

- `notebooks/EuroLeague_Player_Roles_Project.ipynb` — new main project notebook (34 cells at
  the time; since manually edited by the user down to 32 cells, see below).
- `outputs/figures/season_coverage.png`, `outputs/figures/height_distribution.png`
  (regenerated), `outputs/figures/shot_locations_2pt_3pt.png`,
  `outputs/figures/shot_locations_by_zone.png` — the figures actually used in the main
  notebook.
- `CLAUDE.md` — replaced the "mandatory notebook narrative structure" rule (which had caused
  the report-style scaffolding problem) with the corrected rule distinguishing internal
  documentation from the supervisor-facing notebook's own voice and scope.
- `docs/project-state.md` (this file) — updated to point to the new main notebook and mark
  `01_data_audit.ipynb`/`02_coordinate_system_analysis.ipynb` as internal source material.

`notebooks/01_data_audit.ipynb`, `notebooks/02_coordinate_system_analysis.ipynb`, and
`notebooks/EuroLeague_Unsupervised_Roles.ipynb` were **not modified** by this task — all
kept as-is (the first two as internal source material, the last as the original analysis).
No raw data file was modified.

## Files updated during the instruction-update task (manual notebook edit follow-up)

- `CLAUDE.md` — added the "Main notebook continuity", "No meta-explanations", and
  "Source of truth — preserving manual edits" rules (see that file for full text).
- `docs/project-state.md` (this file) — recorded the user's manual edit to the main notebook
  and updated the continuation instructions below accordingly.

`notebooks/EuroLeague_Player_Roles_Project.ipynb` was **explicitly not modified** in this
task — the user edited it by hand beforehand and asked only for the durable instructions to
be updated to match. Nothing else was touched.

## Files created/updated during the feature-table task

- `notebooks/EuroLeague_Player_Roles_Project.ipynb` — extended in place, continuing directly
  from the user's manually edited content (which was preserved exactly). 32 cells before this
  task, 64 after.
- `data/processed/player_season_team_features.csv` — the new complete feature table (6,307
  rows x 76 columns). See "Player-season-team feature table" above for full detail.
- `outputs/tables/player_season_team_feature_dictionary.csv` — one row per feature-table
  column.
- `outputs/tables/season_vs_event_shot_attempt_comparison.csv` — season-total vs.
  event-derived field-goal attempt comparison (6,306/6,307 exact matches).
- `outputs/figures/feature_table_coverage.png` — the one new figure added (a compact
  comparison of row counts by data-coverage requirement).
- `docs/project-state.md` (this file) — updated with the feature-table result, revised open
  questions, and revised future-task list.

**A bug worth recording:** the first draft of the event-join code produced `has_event_data`
as an `object`-dtype column (via `merge` + `fillna`, which leaves Python `True`/`False`
objects rather than a native boolean dtype). Using `~` (bitwise NOT) on that column silently
computed nonsense (`~True == -2`, `~False == -1` in Python) instead of a logical negation —
it printed `-12155` instead of `459` in the notebook's own diagnostic line, and crashed a
later cell that tried to use it as a boolean row mask. Caught during verification (not by the
first execution, which "succeeded" while printing a wrong number) and fixed by adding
`.astype(bool)` after the `fillna(False)`. **Rule for future work: after any `merge` used to
build a boolean flag column, verify its `dtype` is actually `bool` before applying `~` to
it** — `.fillna(...)` alone does not fix an `object`-dtype column's dtype.

`notebooks/01_data_audit.ipynb`, `notebooks/02_coordinate_system_analysis.ipynb`,
`notebooks/EuroLeague_Unsupervised_Roles.ipynb`, and every file under `data/raw/` were **not
modified** by this task.

## Exact instructions for continuing from the current state

1. Read `README.md`, `CLAUDE.md`, and this file.
2. Read `notebooks/EuroLeague_Player_Roles_Project.ipynb` **from disk, in full** — it has been
   manually edited by the user and is the authoritative current state, which may not exactly
   match the description recorded above. `01_data_audit.ipynb` and
   `02_coordinate_system_analysis.ipynb` are internal source material only; consult them for
   extra diagnostic detail if needed, but do not present, extend, or pull old wording from
   them into the main notebook.
3. Get explicit approval on open questions 2-8 above before starting Feature Engineering.
4. Only after approval, begin the Feature Engineering task by extending
   `notebooks/EuroLeague_Player_Roles_Project.ipynb` (continuing directly from its current
   final cell, with no visible task boundary) — building the player-season-team table from
   `euroleague_players.csv` totals plus the 11 approved coordinate-derived features. Write it
   in the same first-person, student-authored voice as the rest of the notebook, and do not
   announce or propose the step after it inside the notebook (see `CLAUDE.md`). Do not fold
   PCA, clustering, or cluster interpretation into that same step unless explicitly approved
   together.
5. Do not modify `notebooks/EuroLeague_Unsupervised_Roles.ipynb`, `notebooks/01_data_audit.ipynb`,
   `notebooks/02_coordinate_system_analysis.ipynb`, or any file under `data/raw/`.
