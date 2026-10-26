# CLAUDE.md

Persistent working instructions for this repository. Read this file, `CheckList.md`,
`README.md`, and the current main notebook before starting any task.

## Project

**Discovering New EuroLeague Player Roles Using Unsupervised Learning** — an academic data
science project by Doron and Yuval.

**Research question:** Can unsupervised learning discover meaningful EuroLeague player roles
from performance data, and do these roles offer useful distinctions beyond the traditional
basketball positions?

**Unit of observation:** player-season-team. The same player may appear in multiple rows
(different seasons and/or teams); these are not duplicates.

Position labels are **never used as a clustering input** — only afterwards, as external
reference labels. The **primary** comparison is with the five traditional positions in
`position_reconciled` (365scores + Wikipedia); the EuroLeague three-category `position` is a
supplementary, coarser comparison. Early notebook sections that describe the original
three-category source data stay as historical narrative. Discovered roles are judged by their
basketball meaning and what they add beyond positions, never by having more clusters than
there are positions — don't use cluster count relative to 3 or 5 positions as a model-selection
argument.

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

## Proportionate analysis

- If an analysis, validation, diagnostic, transformation, plot, comparison, or output does not
  serve a real research decision, do not do it. Prefer the smallest amount of analysis needed
  to reach a defensible conclusion. When uncertain whether extra work is necessary, ask the
  user instead of expanding the analysis automatically.
- Do not re-verify what an earlier stage already established (e.g. completeness of the 17
  features, their distributions) without a concrete reason.
- Unusual values are not automatically problems: in this project an extreme rate may be the
  role signal the clustering should find. Do not transform or remove data for statistical
  neatness alone.
- `CheckList.md` items are decisions to settle, not a menu of diagnostics; an item that would
  add no evidence for a decision should be rewritten or dropped rather than performed.
- Do not create a file (table, figure, processed dataset) unless it is used later or needed as
  a deliverable.

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

This recurring pass supplements the final full editorial review in CheckList Stage 14; it does
not mark Stage 14, or any of its items, complete early.

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

**Completed:** CheckList stages 1-14. **Next:** Stage 15, rendering the notebook as HTML (split
out of the old Stage 14 into its own stage this round; the Hebrew presentation is now Stage 16).
Not started.

**Stage 14 decision (final):** one editorial/consistency read of the full notebook (prose only,
no new code/data/figures, no Run All needed). Cut one redundant transition paragraph in the
Stage 4 missing-value discussion. Condensed a Center-split/cross-position-merge point that had
been written out in full three times (Stage 12 cross-tab interpretation, Stage 12 decision
paragraph, Stage 13 Discussion) to one full explanation plus brief back-references, preserving
each paragraph's unique content. Rewrote Stage 13's Discussion from four bold-labeled sub-points
into flowing paragraphs; no facts, numbers, or citations changed. No AI-artifact code found
worth changing -- all helper functions are reused multiple times and legitimately justify their
existence. Notebook: 192 -> 191 cells (one markdown cell removed); validates, zero execution
errors, ends at the Limitations section, consistently first-person-plural. `git status` showed
only the notebook changed from this stage's edits -- no figures or processed CSVs touched, so
nothing needed restoring.

**Stage 13 decision (final):** added a short "Discussion" markdown section (prose only, no new
code/data/figures) that briefly recaps the five roles, the GMM k = 5 selection (Stage 9), and the
Stage 10 robustness checks, then states the answer to the research question: the roles are
basketball-meaningful and add information beyond position, evidenced by the Stage 12 cross-tabs
and low ARI (0.210/0.288), not by having more roles than positions. A "Limitations" subsection
separates better-supported points (the Stage 10 stability checks, the Stage 12 position
comparison itself, the small 2.2%/2.9% missing-label share) from more tentative ones (the
participation threshold, the 17-feature representation and its preprocessing, inconsistent
event-type/zone recording across seasons, undocumented shot-distance units, untested
longer-term playing-style drift across the 19 seasons -- distinct from the Stage 10 check, which
only ruled out an E2007-E2008 recording-period artifact -- the K-Means/GMM assumptions against
the continuum the Stage 7 PCA projection showed, and repeated players across seasons inflating
cluster sizes relative to distinct players). No Run All needed (no numeric/code changes).

**Stage 12 decision (final):** `position_reconciled` covers 97.8% of eligible rows (`position`
97.1%); unlabeled rows are dropped from each comparison (no further treatment needed). Primary
cross-tab (role x `position_reconciled`, counts/row-share/column-share, heatmap
`outputs/figures/role_vs_position_reconciled.png`): Center and Point Guard each concentrate into
one role (69%/24% Center -> low-post centers/mobile stretch bigs; 54%/40% Point Guard ->
playmaking guards/perimeter shooters), Small Forward and Power Forward each split three ways,
and Point Guard vs. Shooting Guard split the same two roles with shares reversed (Shooting
Guard 44% perimeter shooters / 36% playmaking guards) -- the guard split tracks
ball-handling-vs-shooting more than the official label. From the role side, mobile stretch bigs
(50% Power Forward + 31% Center) and low-usage forwards (38% Small Forward + 37% Power Forward)
each combine two positions the label keeps separate. The supplementary 3-category `position`
(no new figure) reproduces the same shape (Center 64%/27% low-post/mobile stretch; Guard
47%/43% playmaking/perimeter; Forward spread 44%/20%/20% across low-usage/perimeter/mobile
stretch). ARI is low against both labels (0.210 `position_reconciled`, 0.288 `position`,
computed with `adjusted_rand_score` on the labeled subset), well below the 0.4-0.5 internal
K-Means/GMM agreement from Stage 9. Decision: the roles add real information beyond position --
the Center split and the two cross-position merges are the clearest evidence -- not because
there are more roles than positions. Notebook state added: `role_position`, `counts`,
`role_share`, `position_share`, `ROLE_ORDER`, `POSITION_ORDER`, `role_position3`, `counts3`,
`role_share3`, `position_share3`, `ari_position_reconciled`, `ari_position`. New file:
`outputs/figures/role_vs_position_reconciled.png`. A Run All also regenerates `gmm_bic.png`,
`kmeans_model_selection.png`, `pca_explained_variance.png`, and `pca_projection_pc1_pc2.png` with
harmless byte-level drift -- restore those with `git checkout` unless a real regeneration is
intended (already restored after this stage's Run All).

**Stage 11 decision (final):** the five GMM components were named from their standardized
profiles (heatmap `outputs/figures/gmm_cluster_profiles.png`) and two representative-player
lists per component (highest posterior probability, and closest to `gmm_selected.means_`, each
deduplicated by player, both include `position_reconciled` for color): component 0 **playmaking
guards** (n = 1,054; assists z = +0.88, turnovers z = +0.54, height z = -0.79), component 1
**low-post centers** (n = 756; shot-distance spread z = -1.90, three-point attempts z = -1.50,
height z = +1.13, offensive rebounds z = +1.50, blocks z = +1.29 -- the most extreme profile),
component 2 **low-usage forwards** (n = 976; no |z| above 0.66, the flattest profile, defined by
low turnovers/fouls-drawn rather than one strong signal), component 3 **perimeter shooters**
(n = 1,162; median shot distance z = +1.23, three-point attempts z = +1.01, two-point attempts
z = -0.93), component 4 **mobile stretch bigs** (n = 620; height/rebounds/blocks elevated like
component 1 but far less extreme shot-location restriction, non-trivial three-point rate 2.66
per 40 vs component 1's 0.12). Victor Wembanyama's E2021 ASVEL season is component 4's top
"star" (posterior 1.0) but not a "textbook" example -- flagged in the notebook as an extreme,
confidently-assigned case rather than a typical one. Alberto Abalde's career (component 0 at
Joventut in E2017, then component 3 at Real Madrid from E2020 on with one component-2 season)
is used as the one multi-season role-change illustration. No cluster was revised. Notebook state
added: `cluster_profile`, `ROLE_NAMES`, `role_summary`, `representative_players()`,
`dist_to_own_mean`, `stars`, `textbook`, `abalde`. New file: `outputs/figures/gmm_cluster_profiles.png`.
A Run All also regenerates `gmm_bic.png`, `kmeans_model_selection.png`,
`pca_explained_variance.png`, and `pca_projection_pc1_pc2.png` with harmless byte-level drift --
restore those with `git checkout` unless a real regeneration is intended.

**Stage 10 decision (final):** the selected GMM (k = 5, full covariance, `reg_covar = 0.01`) is
stable. (1) Nine additional `random_state` refits gave BIC within 155,864-155,885 of the
original 155,866, pairwise ARI across all ten runs averaging 0.978 (min 0.929), and Hungarian-
matched agreement with the original run of at least 96.8%. (2) Refitting the full pipeline
(shrinkage prior, `StandardScaler`, GMM) on the stricter `10 games / 200 minutes` sample (3,679
of the 4,568 eligible rows, all already inside it) also selected k = 5 by BIC (124,041 vs 124,691
at k = 4 and 124,569 at k = 6) and reproduced matching cluster profiles on the shared rows (ARI
0.887, 94.9% matched agreement; profile means within 0.8 units of the full-sample model, mostly
within 0.3). (3) Each component's share of E2007-E2008 rows (8.4%-14.8%) stays close to the
10.8% overall share, so no component is a recording-period artifact, and no further sensitivity
comparison was run. Notebook state added: `match_components` (Hungarian alignment helper),
`stability_models`/`stability_labels`/`stability_summary` (seeds 0-8 plus the original 42),
`strict_rows`/`X_strict_scaled`/`strict_gmm`/`strict_labels`/`strict_bic_check`/
`profile_compare`, and `early_share_by_component`. No new files written (no new figures or
tables); this stage only adds notebook cells. A Run All regenerates
`outputs/figures/gmm_bic.png`, `kmeans_model_selection.png`, `pca_explained_variance.png`, and
`pca_projection_pc1_pc2.png` with harmless byte-level differences (not content changes) — restore
them with `git checkout` unless a real regeneration is intended.

**Stage 9 decision (final):** clustering model = `GaussianMixture(n_components=5,
covariance_type="full", reg_covar=0.01, n_init=10, max_iter=500, random_state=RANDOM_STATE)` on
`X_scaled`. Default `reg_covar=1e-6` gave BIC minimum k = 10 but collapsed components from k = 5
on (443 zero-3PA rows: zero variance in 3PA/40 and shrunk 3P%; 865 zero-block rows at k = 10) —
a Gaussian-likelihood artifact of legitimate point masses, not a data error. 0.01 and 0.1 both
remove the collapse and both put the BIC minimum at k = 5 (runner-up k = 6 +23 / k = 4 +12);
0.01 kept as the smaller tested value (a stated assumption, not a proven optimum; absolute BIC
not compared across settings). Under 0.01: k = 5 BIC 155,866, k = 6 +23 (close alternative),
k = 4 +884; weights 0.140-0.246, hard counts 620-1,162; 77.1% max posterior >= 0.9, 3.5% < 0.6;
component 2 least certain (0.881). ARI vs K-Means k = 4: GMM k = 4 0.513, GMM k = 5 0.409. No
position label was used. Notebook state kept: `fit_gmm_sweep`, `gmm_models` and `gmm_summaries`
(dicts by `reg_covar` -> k), `GMM_REG_COVAR`, `gmm_comparison`, `GMM_SELECTED_K`, `gmm_selected`,
`gmm_labels` and `gmm_posteriors` (indexed like `X_scaled`/`modeling_metadata`). Figure
`outputs/figures/gmm_bic.png`; no label file. The three GMM sweeps take about 1 minute of Run All.

**Stage 8 decision (final):** K-Means baseline is **k = 4** (`KMeans(n_clusters=4, n_init=20,
random_state=RANDOM_STATE)` on `X_scaled`; cluster sizes 1,228 / 1,268 / 1,166 / 906, silhouette
0.148). k = 2-12 were fitted; silhouette (full sample) falls from 0.299 at k = 2 to 0.081 at
k = 12, inertia gains drop sharply after k = 4, no degenerate clusters. k = 2 is valid but
mainly the PC1 interior/perimeter split; k = 5 (silhouette 0.134) is a similarly reasonable
alternative. k = 4 is a weakly supported practical baseline, not the number of roles. Cluster
sizes are a degeneracy check only — balanced sizes are neither expected nor preferred, since
roles need not be equally common. Stage 9 must choose the GMM cluster count independently on
`X_scaled`; the preliminary ~8-component GMM/BIC result (different feature representation) is
not a target to reproduce. Notebook state kept for Stage 9: `kmeans_models` (dict k -> fitted model), `kmeans_comparison` (per-k
inertia, silhouette, cluster sizes), `KMEANS_BASELINE_K`, `kmeans_baseline`, and
`kmeans_labels` (Series indexed like `X_scaled`/`modeling_metadata`). No label file is written;
figure `outputs/figures/kmeans_model_selection.png`.

**Stage 7 decision (final):** PCA is exploration/visualization only; K-Means and GMM use the
17 standardized features in `X_scaled`, not PCA components. Evidence (in the notebook): PC1
38.1%, PC2 13.3%, PC3 7.2% (cumulative 51.5% / 58.7%), PC4-PC10 3.1-6.1% each, 8 components to
pass 80%; the PC1-PC2 plane keeps only 0.04-0.28 of 3P%, steals, fouls committed, 2P%, FT%.
PC1 = interior-to-perimeter, PC2 = on-ball offensive involvement, PC3 = weak shooting-accuracy
vs fouls/steals contrast. The projection shows uneven density along a continuum, no separated
groups. The last notebook cells keep `modeling_pca`, `pca_scores`, `pca_loadings`, and
`pca_projection` (PC1/PC2 scores, `X_scaled` index) in notebook state for later 2D cluster plots,
and write `outputs/figures/pca_explained_variance.png` and `pca_projection_pc1_pc2.png`.

**Stage 6 decision (final):**
- The three shooting percentages are represented in the modeling matrix by k = 10
  attempt-weighted shrinkage, `(makes + 10 * prior_mean) / (attempts + 10)`, with the prior the
  eligible-sample attempt-weighted percentage (0.531 / 0.363 / 0.764). Reason: reliability —
  extreme raw 3P%/FT% values came almost entirely from 1-9 attempts. Zero-attempt rows get the
  prior, superseding the Stage 4 median fill for modeling only; `features` and the processed
  CSVs keep their Stage 4 percentage representation (observed percentages, median-filled where
  attempts are 0), while the modeling matrix uses the Stage 6 shrinkage-adjusted estimates.
  k = 5/10/20 were compared outside the
  notebook; do not re-test.
- All 17 features are then standardized with `StandardScaler` (fitted on the 4,568 eligible
  rows). The other 14 are untransformed — skew is treated as role signal, and no observation is
  removed for being unusual.
- The last two code cells build `modeling_features` (adjusted, unscaled), `X_scaled` (4,568 × 17,
  columns in `FINAL_CLUSTERING_FEATURES` order, index = `features` row index),
  `modeling_metadata` (`IDENTIFIER_COLS`), and `feature_scaler`, all kept in notebook state; no
  modeling-matrix file is written. The last cell also rewrites the Shooting efficiency row of
  `outputs/tables/final_clustering_feature_decisions.csv` with the shrinkage representation.

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
  0.769 FT%; never from position). This fill completes the feature table only; the modeling
  matrix uses the Stage 6 shrinkage estimate instead.
- Shot coordinates: basket at `(0, 0)`, distances in raw units; the `(-1, -1)` placeholder is
  excluded from spatial features. The A-J `zone` letters are undocumented and mark different
  court areas in E2007-E2008 than later, so zone shares are descriptive/QA only and are not
  relabelled.
- Position: `position_reconciled` (5 categories; 365scores, with a Wikipedia fallback; 97.8% of
  eligible rows) is the primary comparison label and `position` (EuroLeague, 3 categories) the
  supplementary one; both are comparison-only, never clustering inputs.
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
