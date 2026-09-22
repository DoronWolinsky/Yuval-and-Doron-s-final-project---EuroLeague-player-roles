# Discovering New EuroLeague Player Roles Using Unsupervised Learning

An academic data science project by Doron and Yuval exploring whether natural EuroLeague
player roles can be discovered from performance data with unsupervised machine learning,
without relying on traditional position labels (Guard / Forward / Center).

## Research question

Can natural EuroLeague player roles be discovered from performance data without relying on
traditional position labels such as Guard, Forward, and Center?

Traditional position labels are **never used as a clustering input**. They are used only
after clustering, for interpretation and comparison against the discovered groups.

## Data

| File | Path | Granularity |
|---|---|---|
| `euroleague_players.csv` | `data/raw/` | one row per player-season-team |
| `euroleague_points.csv` | `data/raw/` | one row per recorded shot/action event |
| `players_bio.csv` | `data/raw/` | one row per player |
| `merged_euroleague_players.csv` | `data/processed/` | one row per enriched event (derived) |

`data/raw/euroleague_points.csv` and `data/processed/merged_euroleague_players.csv` are
excluded from this repository (`.gitignore`) because they exceed GitHub's 100MB file-size
limit; Doron and Yuval share them directly.

## Repository structure

```text
euroleague-player-roles/
├── data/
│   ├── raw/                  # Source-of-truth CSVs (never modified)
│   └── processed/            # Derived datasets
├── notebooks/
│   ├── EuroLeague_Unsupervised_Roles.ipynb        # Original feasibility analysis
│   ├── EuroLeague_Player_Roles_Project.ipynb      # Main project notebook (start here)
│   ├── 01_data_audit.ipynb                        # Internal source material
│   └── 02_coordinate_system_analysis.ipynb        # Internal source material
├── outputs/
│   ├── figures/               # Exported charts (.png)
│   └── tables/                # Exported analysis tables (.csv)
├── README.md
├── CLAUDE.md                  # Working instructions for Claude Code
├── CheckList.md               # Stage-by-stage project roadmap
└── requirements.txt
```

`notebooks/EuroLeague_Player_Roles_Project.ipynb` is the main project notebook — read this
one first. `01_data_audit.ipynb` and `02_coordinate_system_analysis.ipynb` hold the fuller
diagnostic work behind it and are kept as internal reference material.

## Running the notebook

```bash
pip install -r requirements.txt
```

Then open `notebooks/EuroLeague_Player_Roles_Project.ipynb` in Jupyter or PyCharm and run it
from the repository root (Restart Kernel + Run All), or:

```bash
python -m nbconvert --to notebook --execute --inplace notebooks/EuroLeague_Player_Roles_Project.ipynb
```

## Status

Stages 1-4 of `CheckList.md` are complete: understanding the three raw datasets, building the
player-season-team feature table, defining the eligible modeling sample (4,568 of 6,307 rows,
at least 5 games and 100 minutes), and resolving missing values in that eligible sample.

Height cleaning handles two distinct missing-value sentinels found in `players_bio.csv`: the
original `NaN` values, and a separately discovered `height_cm == 0` sentinel. Both are
corrected through the same mechanism, `data/processed/height_overrides.csv`, which now lists
62 uniquely verified players in total -- the original 11 `NaN`-height players plus 51 players
later found to carry the `0` sentinel (167 eligible rows). All 62 heights are externally
verified physical measurements, not statistical imputations, preferring 365Scores when a
reliable identity match was available and falling back to Wikipedia otherwise. Detailed
provenance for the 51-player correction is in
`data/processed/zero_height_player_research.csv`. The notebook applies an override only to a
verified `player_id`, and only where the recorded height is `NaN` or `0`, so an existing
positive height is never overwritten; 7 additional zero-height players exist only outside the
eligible modeling sample and were intentionally left untouched. Yuval's five-category position
enrichment and the project's shooting-location/spatial features are unaffected by this
correction.

The next stage is selecting the final clustering feature set (`CheckList.md` stage 5). See
`CheckList.md` for the full roadmap and `CLAUDE.md` for current work state and working rules.
