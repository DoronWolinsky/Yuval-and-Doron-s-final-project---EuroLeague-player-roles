# CLAUDE.md

Persistent working instructions for this repository. Read this file, `CheckList.md`,
`README.md`, and the current main notebook before starting any task.

## Project

**Discovering New EuroLeague Player Roles Using Unsupervised Learning** — an academic data
science project by Doron and Yuval.

**Research question:** Can natural EuroLeague player roles be discovered from performance
data without relying on traditional position labels (Guard, Forward, Center)?

**Unit of observation:** player-season-team. The same player may appear in multiple rows
(different seasons and/or teams); these are not duplicates.

Traditional position (`position` in `players_bio.csv`) is **never used as a clustering
input** — only afterwards, to interpret and compare the discovered groups against it.

Data files and their roles are described in `README.md`. Do not silently change which file is
treated as the source of truth for a given kind of data (season totals, shot events,
biography).

## Hard rules

- Work on one explicitly approved stage at a time — see `CheckList.md` for the stage list.
  Do not start a later stage without explicit approval, even if it looks like a natural
  continuation.
- Never use traditional position as a training/clustering feature; only for post-hoc
  comparison.
- Never modify raw data files under `data/raw/`. Any derived dataset goes under
  `data/processed/`.
- Do not add unrelated libraries, models, or technologies. Stick to pandas, NumPy,
  Matplotlib, Seaborn, and scikit-learn (preprocessing, PCA, and the planned K-Means/GMM)
  unless a new dependency is genuinely required and approved.
- Do not modify `notebooks/EuroLeague_Unsupervised_Roles.ipynb`,
  `notebooks/01_data_audit.ipynb`, or `notebooks/02_coordinate_system_analysis.ipynb` unless
  explicitly asked — they are the original analysis and internal source material,
  respectively, not the active notebook.
- Use `pathlib.Path` and repository-relative paths — never hardcoded absolute local paths.
- Use `RANDOM_STATE = 42` for any sampling.
- Do not present assumptions as verified facts — every claim in the notebook must be backed
  by output produced in that notebook.
- All project artifacts are written in English — code, comments, notebook Markdown, docs,
  filenames, chart labels — except the future Hebrew presentation, which is out of scope
  until explicitly requested.
- Document important decisions in the notebook itself and, for anything needed to resume work
  later, in this file's "Current Work State" section — not in a separate history log.
- Do not create git commits or push unless explicitly requested.

## Repository structure

```text
euroleague-player-roles/
├── data/
│   ├── raw/                  # Never modify. Source of truth.
│   └── processed/            # Derived data only.
├── scripts/
│   └── wikipedia_position_lookup.py               # Builds the Wikipedia position lookup.
├── notebooks/
│   ├── EuroLeague_Unsupervised_Roles.ipynb        # Original analysis. Do not modify.
│   ├── 01_data_audit.ipynb                        # Internal source material. Do not modify.
│   ├── 02_coordinate_system_analysis.ipynb        # Internal source material. Do not modify.
│   └── EuroLeague_Player_Roles_Project.ipynb      # Main supervisor-facing notebook.
├── outputs/
│   ├── figures/
│   └── tables/
├── README.md
├── CLAUDE.md
├── CheckList.md
└── requirements.txt
```

## `CheckList.md`

The authoritative research roadmap: 16 stages from data understanding through the Hebrew
presentation, each with checkbox items and a short expected result or decision. It is the
reference for both Doron/Yuval and Claude Code on what's done and what's next. Tick boxes as
stages complete; don't turn it into a technical activity log, and don't redesign or renumber
its stages without being asked.

## The main notebook is a student deliverable, not an agent report

`notebooks/EuroLeague_Player_Roles_Project.ipynb` is the single notebook Doron and Yuval will
submit to their supervisor and use as the factual basis for their presentation. It must read
as if two students wrote it about their own project. The user edits it by hand at times —
treat the file on disk as always authoritative over anything described in an earlier
conversation.

It must contain **only** research-relevant explanations, implementations, results, and
decisions — never agent instructions, task scopes, approval workflows, completion reports, or
notes about how the notebook itself should be structured. Those belong in this file.

### No visible task boundaries

The notebook is one continuous narrative. It must never reveal where one Claude Code task
ended and another began.

- No sections titled (or effectively titled) `What's Next`, `Next Steps`,
  `Proposed Next Task`, `Task Summary`, `Task Completion`, `What This Notebook Covers`,
  `Notebook Scope`, `Setup`, `Implementation Plan`, `Decision Required`, or
  `Remaining Uncertainty`.
- Do not announce or propose future work inside the notebook — the next task comes directly
  through Claude Code. When the notebook currently ends at some stage, it may simply end after
  the last completed result and its interpretation.
- New work continues naturally from the previous result, e.g. *"The previous checks showed
  that the three datasets can be combined using the player-season-team key. We therefore
  aggregated the shot events..."* — then the implementation, result, and decision that follows.
- No meta-explanations of ordinary mechanics (imports, path resolution, helper functions,
  export code, random seeds, notebook execution, internal source notebooks, Claude Code
  itself). Setup code may stay without its own Markdown explanation unless it embeds a
  genuinely research-relevant choice.

### Voice

- First-person plural ("we loaded...", "we found...", "we decided to..."), as Doron and Yuval
  describing their own work.
- Direct, practical, technically accurate English; name the mechanism, then its purpose or
  result — not ornate academic prose, not an AI-report template.
- Never mention Claude, AI assistance, prompts, task scopes, approval workflows, or
  compliance. Never use report-style labels ("What is being checked", "Decision Required
  Before Continuing", "Objective/Interpretation/Decision" headers) or defensive/workflow
  wording ("as required", "this task was intentionally limited to", "the project owner must
  decide"). State the research action and conclusion directly.
- Include a check, table, or figure only if it changes how the data is cleaned, joined,
  filtered, described, or modeled — one clear visualization beats several redundant ones.
- Opening should contain only what helps the supervisor understand the project: title,
  authors, research question, motivation, methodological goal. No contents summary unless the
  notebook becomes long enough to genuinely need one.

### Continuity

- Maintain **one continuous main notebook** — extend `EuroLeague_Player_Roles_Project.ipynb`
  rather than creating a new one, unless asked otherwise.
- Before any notebook task: read the current file on disk in full, continue from its current
  final result, never recreate a section the user removed, never overwrite manually revised
  prose with older generated wording, and don't modify it outside the explicitly approved
  stage.

### Consistency pass after notebook changes

After every coherent notebook task or batch of related notebook edits — and always before a
handoff, commit, or push — do one full consistency pass over the complete notebook. This is one
pass per meaningful unit of change, not after every individual edit. In that pass:

- Read the whole notebook as one continuous research narrative, not only the cells changed in
  the current task.
- Check whether a new discovery or decision makes an earlier explanation incomplete,
  misleading, or false. Where understanding changed over time, keep the honest sequence of the
  investigation but clearly mark the initial finding as initial and state the later corrected
  conclusion; never leave two unqualified contradictory claims in different parts of the
  notebook.
- Check that sample sizes, row counts, feature lists, thresholds, variable names, file names,
  stage numbers, methodological decisions, and reported results agree everywhere, and that
  every numerical statement is backed by visible output in the notebook (see Hard rules).
- Remove or update stale outputs, interpretations, forward-looking statements, and code that
  refer to an abandoned method.
- Confirm that Markdown comes after the output it interprets and that no conclusion appears
  before its evidence.
- Confirm the Voice rules above still hold: first-person plural, Doron and Yuval's own work, no
  Claude/task/handoff/approval language.
- Preserve manually written content; make only the smallest revisions needed to restore
  consistency.
- If code, calculations, figures, tables, or numerical claims changed, run a Restart Kernel +
  Run All equivalent and verify the complete execution. A prose-only edit does not need
  execution unless it changes the meaning of a numerical claim or its relationship to an
  output.
- Compare the notebook's final state with `README.md`, `CheckList.md`, and the Current Work
  State below; they must agree on completed work, the current stage, important decisions,
  produced files, and what remains open.
- In the final task report, state explicitly that the consistency pass was performed and list
  the earlier contradictions or stale statements that were corrected, or say explicitly that
  none were found.

This recurring pass supplements the final full editorial review in CheckList Stage 15; it does
not mark Stage 15, or any of its items, complete early.

## Working conventions

- Notebooks must run top-to-bottom after Restart Kernel + Run All, from the repository root,
  with no absolute local paths. The notebook resolves the repository root at runtime.
- Do not write conclusions before the corresponding code output exists.
- After a `merge` that can introduce `NaN` into a boolean column, followed by `.fillna(...)`,
  verify the result is actually `bool` dtype before applying `~` to it — `fillna` alone
  leaves it `object`-dtype, and `~` on Python `True`/`False` objects silently computes a
  bitwise complement instead of a logical negation, with no error. Cast with `.astype(bool)`.
- A Run All rewrites both processed feature CSVs (with last-digit float drift in the three
  `*_std` spatial columns) and re-renders the notebook's figures. Unless a regeneration is
  intended, restore those files with `git checkout`; when a column change is intended, replace
  only the intended fields in the existing CSV text so unaffected columns stay byte-identical.

## Current Work State

**Completed:** CheckList stages 1-5. **Next:** Stage 6, transforming and scaling the modeling
data — examine skew (strongest: `blocks_per_40` 2.08, `assists_per_40` 1.30,
`raw_shot_distance_std` -1.30) and extreme values of the 17 features, decide on
transformations, standardize, and build the final modeling matrix. Not started.

**Data and sample (stages 1-4):**
- Eligible sample: `eligible_for_modeling` = at least **5 games and 100 minutes** — 4,568 of
  6,307 rows, all 19 seasons (196-273 rows each). `10 games / 200 minutes` is reserved as a
  Stage 10 sensitivity check.
- Rates are per 40 minutes (`season total / minutes * 40`, `*_per_40`, `PER_40_SOURCE_COLUMNS`);
  NaN where minutes are 0 (303 rows, none eligible).
- Height: `players_bio.csv` marks missing height with `NaN` (27 players) **and** `0` (58
  players). 62 players with eligible rows have externally verified heights in
  `data/processed/height_overrides.csv` (provenance for the 51 zero-height players:
  `zero_height_player_research.csv`); the notebook replaces only `NaN`/`0` for those IDs (198
  eligible rows). The 7 other zero-height players have no eligible rows and stay as recorded.
- Shooting percentages are `NaN` when attempts are 0 (flags `has_three_point_attempts`,
  `has_free_throw_attempts`), then filled with the eligible median among shooters (0.348 3P%,
  0.769 FT%; never from position).
- Shot coordinates: basket at `(0, 0)`, distances in raw units; the `(-1, -1)` placeholder is
  excluded from spatial features. The A-J `zone` letters are undocumented and mark different
  court areas in E2007-E2008 than later, so zone shares are descriptive/QA only and are not
  relabelled.
- Position: `position` (EuroLeague, 3 categories) and `position_reconciled` (365scores, with
  a Wikipedia fallback; 97.8% of eligible rows) are comparison-only, never clustering inputs.
  Two players (`P011826`, `P012613`) never got a 365scores lookup (504 timeout) and use
  `position_wiki`.

**Stage 5 decision — `FINAL_CLUSTERING_FEATURES` (17, ordered):** `two_point_attempts_per_40`,
`three_point_attempts_per_40`, `two_points_percentage`, `three_points_percentage`,
`free_throws_percentage`, `assists_per_40`, `turnovers_per_40`, `offensive_rebounds_per_40`,
`defensive_rebounds_per_40`, `steals_per_40`, `blocks_per_40`, `fouls_committed_per_40`,
`fouls_received_per_40`, `height_cm`, `median_raw_shot_distance`, `raw_shot_distance_std`,
`lateral_shot_position_std`. Complete for all eligible rows; largest |r| 0.826 (median
distance vs lateral spread).
- Both foul measures stay (r = 0.010 with each other); `fouls_committed_per_40` has r = -0.57
  with minutes per game, accepted and explained in the notebook.
- Shot location uses these three original coordinate summaries. A PCA of the seven summaries
  was tested and rejected (one component was only court side), so no `spatial_pc*` columns
  are model inputs.
- Excluded: `points_per_40`, free-throw attempts per 40 and free-throw attempt rate, all
  attempt shares, the `has_*` flags (QA only), the other four coordinate summaries, zone
  shares, raw totals, playing-time and coverage fields, `valuation`, `plus_minus`,
  identifiers/metadata, and all position columns.

**Files:**
- `data/processed/player_season_team_features.csv` (6,307 × 79, complete table) and
  `data/processed/player_season_team_features_with_position.csv` (6,307 × 83, adds the four
  position-enrichment columns; the table the later stages should use). Neither is the
  modeling matrix yet.
- `outputs/tables/final_clustering_feature_decisions.csv` (one decision per column) and
  `outputs/tables/player_season_team_feature_dictionary.csv` (83 rows; `selected` for the 17).
- Position provenance: `data/processed/wikipedia_position_lookup/wikipedia_position_lookup.csv`
  (from `scripts/wikipedia_position_lookup.py`), `data/processed/player_positions_365scores.csv`,
  and the QA tables `outputs/tables/position_source_agreement_summary.csv`,
  `position_source_disagreements.csv`, and `position_reconciled_vs_euroleague_position.csv`.
- Outputs of the internal source notebooks (`01_data_audit`, `02_coordinate_system_analysis`)
  stay as they were produced, including audit-era names such as `*_per_36` in
  `outputs/tables/candidate_columns_for_research.csv`; they are not active inputs.

## Handoff rule

Whenever Claude Code stops working:

1. Update `CheckList.md` only for work that was actually completed.
2. Update the "Current Work State" section above with: the last completed stage, the current
   incomplete stage if work stopped mid-way, the exact remaining work, the relevant files
   created or changed, and the next intended stage.
3. Do not write a long completion report into either file.
4. Do not place this handoff information inside the notebook.
5. Do not mark an entire checklist stage complete if only part of it was implemented.

This matters because Doron and Yuval both work with Claude Code from separate computers.
