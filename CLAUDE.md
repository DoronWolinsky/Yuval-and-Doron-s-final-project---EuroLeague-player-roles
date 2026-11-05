# CLAUDE.md

Maintenance notes for AI-assisted work in this repository. Read `README.md` first. `RESEARCH_ROADMAP.md` records the research decisions and their evidence.

## Ownership

- **Authors decide the research.** Doron and Yuval own the research question, the methodological decisions, the interpretation and the conclusions.
- **Assistance is support only.** It covers implementation, debugging, documentation and editing.
- **Ask before changing results.** Do not change any of the following without explicit approval from the authors:
  - the sample rule (5 games / 100 minutes);
  - the 17 features;
  - the preprocessing (shrinkage k = 10, `StandardScaler`);
  - the model (full-covariance GMM, k = 5, `reg_covar = 0.01`, `RANDOM_STATE = 42`);
  - any reported result.

## Key files

- **Final notebook:** `notebooks/EuroLeague_Player_Roles_Project.ipynb`, with 142 cells (69 code).
- **Rendered report:** `outputs/EuroLeague_Player_Roles_Project.html`.
- **Supporting material:** `notebooks/01_data_audit.ipynb` and `notebooks/02_coordinate_system_analysis.ipynb`. The early feasibility notebook is in `notebooks/archive/`. Do not edit these unless asked.
- **Notebook inputs:**
  - `data/raw/{euroleague_players,euroleague_points,players_bio}.csv`. `euroleague_points.csv` is gitignored and must be obtained separately.
  - `data/processed/height_overrides.csv`
  - `data/processed/player_positions_365scores.csv`
  - `data/processed/wikipedia_position_lookup/wikipedia_position_lookup.csv`
- **Notebook output:** `data/processed/player_season_team_features_with_position.csv` is the only file the notebook writes.

## Rules

- **Raw data.** Never modify `data/raw/`.
- **Untracked lookup files.** Do not commit the logs, cache or pilot files in `data/processed/wikipedia_position_lookup/`. They are untracked.
- **Paths.** Use `pathlib` and repository-relative paths. The notebook finds the repository root at runtime.
- **Positions.** Traditional positions are comparison labels only, never clustering inputs.
- **Evidence.** Every numerical claim in the notebook must be backed by an output in the notebook.
- **Notebook text.** The narrative is the authors' own: first-person plural, research content only, with no tool or workflow notes.
- **Dependencies.** Use only pandas, NumPy, SciPy, Matplotlib, Seaborn and scikit-learn unless the authors approve another dependency.
- **Git.** Commit or push only when asked. Never force-push.

## Editing and validation

- **Text edits.** Do not rerun the notebook for edits to prose or display strings. Edit the JSON, keep the cell IDs stable, and write it back with LF line endings (`json.dumps(nb, indent=1, ensure_ascii=False) + "\n"`). PyCharm can regenerate cell IDs when cells are moved; restore the originals if that happens.
- **Validate after every edit:**
  - `nbformat.validate`;
  - unique cell IDs;
  - `ast.parse` on every code cell;
  - no error outputs;
  - a diff against `git show HEAD:<path>` confirming that only the intended cells changed.
- **Re-render the HTML** from saved outputs after any notebook change:
  `python -m nbconvert --to html notebooks/EuroLeague_Player_Roles_Project.ipynb --output-dir outputs`.
  Then check the counts: 11 embedded images, 28 tables and no tracebacks.
- **Rerunning code.** If code or results must change, rerun on a scratch copy and take over only the intended outputs. A full run rewrites the processed CSV with last-digit float drift in the `*_std` columns. Unless the regeneration is intended, restore it with `git checkout`.
- **Booleans after a merge.** After a merge followed by `.fillna(...)` on a boolean column, cast with `.astype(bool)` before using `~`.
- **Consistency.** Keep `README.md` and `RESEARCH_ROADMAP.md` consistent with the notebook whenever results or decisions are described.
