# Discovering New EuroLeague Player Roles Using Unsupervised Learning

An academic data science project by Doron and Yuval exploring whether unsupervised machine
learning can discover meaningful EuroLeague player roles from performance data, and whether
those roles add useful distinctions beyond traditional basketball positions.

## Research question

Can unsupervised learning discover meaningful EuroLeague player roles from performance data,
and do these roles offer useful distinctions beyond the traditional basketball positions?

Position labels are **never used as a clustering input**; they are external reference labels
used only after clustering. The primary comparison is with the five traditional positions
(Point Guard, Shooting Guard, Small Forward, Power Forward, Center) in `position_reconciled`,
compiled from 365scores and Wikipedia; the EuroLeague three-category `position` (Guard,
Forward, Center) is a supplementary, coarser comparison. The value of the discovered roles
lies in their basketball meaning and in what they add beyond these positions, not in whether
there are more clusters than positions.

## Data

| File | Path | Granularity |
|---|---|---|
| `euroleague_players.csv` | `data/raw/` | one row per player-season-team |
| `euroleague_points.csv` | `data/raw/` | one row per recorded shot/action event |
| `players_bio.csv` | `data/raw/` | one row per player |
| `merged_euroleague_players.csv` | `data/processed/` | one row per enriched event (derived) |
| `player_season_team_features_with_position.csv` | `data/processed/` | one row per player-season-team: all features, eligibility flag, and position labels (derived by the main notebook) |

`data/raw/euroleague_points.csv` and `data/processed/merged_euroleague_players.csv` are
excluded from this repository (`.gitignore`) because they exceed GitHub's 100MB file-size
limit; Doron and Yuval share them directly.

## Repository structure

```text
euroleague-player-roles/
├── data/
│   ├── raw/                  # Source-of-truth CSVs (never modified)
│   └── processed/            # Derived datasets
├── scripts/                  # Wikipedia position lookup used for position enrichment
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

Stages 1-9 of `CheckList.md` are complete: understanding the three raw datasets, building the
player-season-team feature table, defining the eligible modeling sample (4,568 of 6,307 rows,
at least 5 games and 100 minutes), resolving missing values in that sample, selecting the
final clustering features, preparing the modeling matrix (stabilizing shooting percentages
based on few attempts, then standardizing all features), exploring the matrix with PCA,
establishing a K-Means baseline (k = 4), and selecting the clustering model: a full-covariance
Gaussian mixture model with five components and covariance regularization `reg_covar = 0.01`.
PCA is used only for exploration and visualization; clustering uses the 17 standardized
features. The next stage is checking the robustness of the result (`CheckList.md` stage 10).

Rate features are expressed per 40 minutes, the length of a EuroLeague regulation game. The
final clustering feature set has 17 features: two- and three-point attempts per 40, the three
shooting percentages, assists, turnovers, offensive and defensive rebounds, steals, blocks,
fouls committed, and fouls received per 40, height, and three shot-location summaries (median
shot distance, variation in shot distance, and lateral spread of shots).

Important data limitations handled in the notebook:

- `players_bio.csv` marks a missing height with either `NaN` or `0`; the heights of the
  affected players in the modeling sample were verified externally and are listed in
  `data/processed/height_overrides.csv` (provenance in
  `data/processed/zero_height_player_research.csv`).
- The recorded shot-zone letters A-J are undocumented and refer to different court areas in
  E2007-E2008 than in later seasons, so zone shares are kept only as descriptive fields and
  shot location is described from the recorded coordinates.
- The EuroLeague biography data records only three broad positions, so the five-category
  position used for the main comparison was built from 365scores and Wikipedia. Both are used
  only to interpret the discovered roles, never as clustering inputs.

See `CheckList.md` for the full roadmap and `CLAUDE.md` for the current work state and working
rules.
