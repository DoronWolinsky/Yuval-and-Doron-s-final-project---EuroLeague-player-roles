# Discovering New EuroLeague Player Roles Using Unsupervised Learning

An academic data science project exploring whether natural EuroLeague player roles can be
discovered from performance data with unsupervised machine learning, without relying on
traditional position labels (Guard / Forward / Center).

## Research question

Can natural EuroLeague player roles be discovered from performance data without relying on
traditional position labels such as Guard, Forward, and Center?

Traditional position labels are **never used as a clustering input**. They are used only
after clustering, for interpretation and comparison against the discovered groups.

## Data

Four data files are used, described in full in `docs/project-state.md`:

| File | Path | Granularity |
|---|---|---|
| `euroleague_players.csv` | `data/raw/` | one row per player-season-team |
| `euroleague_points.csv` | `data/raw/` | one row per recorded shot/action event |
| `players_bio.csv` | `data/raw/` | one row per player |
| `merged_euroleague_players.csv` | `data/processed/` | one row per enriched event (derived) |

Files under `data/raw/` are never modified. Any derived dataset is written under
`data/processed/`.

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
├── src/                       # Reusable project code (currently empty)
├── docs/
│   └── project-state.md       # Living project-state document
├── README.md
├── CLAUDE.md                  # Durable working rules for AI-assisted sessions
└── requirements.txt
```

`notebooks/EuroLeague_Player_Roles_Project.ipynb` is the main project notebook — read this one
first. `01_data_audit.ipynb` and `02_coordinate_system_analysis.ipynb` hold the fuller
diagnostic work behind it and are kept as internal reference material.

## Running the notebooks

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Open the notebook in Jupyter or PyCharm and run it from the repository root — for example:
   ```bash
   python -m nbconvert --to notebook --execute --inplace notebooks/EuroLeague_Player_Roles_Project.ipynb
   ```
   or open it in Jupyter/PyCharm and use *Restart Kernel and Run All*.

Each notebook resolves the repository root at runtime (see its Setup cell), so it does not
depend on the current working directory Jupyter/PyCharm happens to start from, and it contains
no hardcoded absolute local paths.

## Project status

The current completed step is data preparation — understanding the three raw tables, the
checks needed before combining them, how they join together, and what the shot coordinates
represent (`notebooks/EuroLeague_Player_Roles_Project.ipynb`). See `docs/project-state.md` for
the full status, approved decisions, open questions, and the next proposed task — the next
task requires explicit approval before starting.
