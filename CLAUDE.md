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
  Matplotlib, and Seaborn unless a new dependency is genuinely required and approved.
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

## Working conventions

- Notebooks must run top-to-bottom after Restart Kernel + Run All, from the repository root,
  with no absolute local paths. The notebook resolves the repository root at runtime.
- Do not write conclusions before the corresponding code output exists.
- After a `merge` that can introduce `NaN` into a boolean column, followed by `.fillna(...)`,
  verify the result is actually `bool` dtype before applying `~` to it — `fillna` alone
  leaves it `object`-dtype, and `~` on Python `True`/`False` objects silently computes a
  bitwise complement instead of a logical negation, with no error. Cast with `.astype(bool)`.

## Current Work State

**Completed:**
- CheckList stage 1 — understanding and examining the data.
- CheckList stage 2 — building the player-season-team feature table.
- CheckList stage 3 — defining the eligible modeling sample. Selected rule: **at least 5
  games and 100 minutes**. Eligible sample: 4,568 of 6,307 rows (72.4%), all 19 seasons
  represented (196-273 eligible rows each). `10 games / 200 minutes` is reserved as a
  sensitivity check for Stage 10, after clustering — not run yet.

**Current output:** `data/processed/player_season_team_features.csv` — the complete
6,307-row, 77-column table (unchanged row count), now including the boolean
`eligible_for_modeling` column. Not yet the final modeling matrix.

**In progress — CheckList stage 4, missing values in the eligible sample:** the notebook now
recalculates missingness on the 4,568 eligible rows and separates it into: (a) spatial
location/spread/shot-selection gaps, all eliminated by the Stage 3 eligibility rule (0
remaining); (b) a structural-zero ambiguity in the shooting-percentage columns — `0.0` is
recorded for zero attempts, not a real 0% (443 eligible rows for `three_points_percentage`,
34 for `free_throws_percentage`); (c) genuinely missing `height_cm` (31 eligible rows); (d)
comparison-only missing `position` (132 eligible rows). No imputation or exclusion has been
performed — only the diagnostic. Only items 1-2 of Stage 4 are checked off in `CheckList.md`.

**Not yet performed:** deciding whether height/shooting efficiency are clustering features,
imputing height (if used) from the eligible sample only, deciding how to treat the
shooting-percentage structural zeroes (if used), deciding whether to exclude or otherwise
handle rows still lacking a needed feature, final feature selection, scaling, PCA, K-Means,
GMM, cluster interpretation.

**Important unresolved decisions:**
- Whether height will be a clustering feature, and if so how to impute the 31 missing values
  (from the eligible sample only, never from position).
- Whether shooting efficiency will be a clustering feature, and if so how to treat rows where
  a `0.0` percentage means "no attempts" rather than "0% made."
- Final feature selection.
- Treatment of rows without valid spatial information (moot within the eligible sample
  itself — 0 such rows — but still relevant if any non-eligible row is ever reconsidered).

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
