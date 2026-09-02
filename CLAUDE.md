# CLAUDE.md

Persistent, durable instructions for working on this project. Read this file, `README.md`,
and `docs/project-state.md` before starting any task — do not rely on conversation memory
alone.

## Project

**Discovering New EuroLeague Player Roles Using Unsupervised Learning** — an academic data
science project. See `docs/project-state.md` for the full research goal, research question,
data inventory, decisions, and open questions.

## Hard rules

- **Read first.** Before every task, read `README.md`, `CLAUDE.md`, `docs/project-state.md`,
  and `CheckList.md`.
- **One task at a time.** Work only on the explicitly approved active task. Do not start the
  next task without explicit approval, even if it seems like a natural continuation.
- **Do not silently change the research question**: "Can natural EuroLeague player roles be
  discovered from performance data without relying on traditional position labels?"
- **Do not silently change the intended unit of observation** for the final model:
  player-season-team.
- **Do not silently change the source-of-truth mapping** for the data files (see
  `docs/project-state.md` § Data inventory).
- **Never use traditional position (`position` in `players_bio.csv`) as a training/clustering
  feature.** It may only be used after clustering, for interpretation and comparison.
- **Never modify the raw data files** under `data/raw/`. Any derived dataset goes under
  `data/processed/`.
- **Do not add unrelated libraries, models, or technologies.** Stick to pandas, NumPy,
  Matplotlib, and Seaborn unless a new dependency is genuinely required and approved.
- **Do not perform Feature Engineering, PCA, or clustering during the Data Audit.** Those are
  separate, later, separately-approved tasks.
- **Document every important decision** in the relevant notebook's Markdown cells and in
  `docs/project-state.md`.
- **Keep all analysis reproducible**: use `pathlib.Path` and repository-relative paths (never
  hardcoded absolute local paths), and `RANDOM_STATE = 42` for any sampling.
- **Do not present assumptions as verified facts.** Every claim in a notebook must be backed
  by output produced in that notebook.
- **Stop and report ambiguities** before making decisions that materially affect methodology
  (e.g. how to handle coverage gaps, which coordinate system to assume, whether to include an
  outcome-quality column as a feature).
- **All project artifacts must be written in English** — code, comments, notebook Markdown,
  docs, filenames, chart labels, everything except the future Hebrew presentation deliverable
  (which is out of scope until explicitly requested).
- **Do not create git commits** unless explicitly requested. (This repository is not
  currently a git repository.)
- **Do not modify `notebooks/EuroLeague_Unsupervised_Roles.ipynb`** — it is the original
  feasibility-analysis notebook and is preserved as-is.
- **Do not modify a completed, approved notebook** (e.g. `notebooks/01_data_audit.ipynb`)
  while working on a later task, unless that notebook's own task is explicitly reopened.

## Repository structure

```text
euroleague-player-roles/
├── data/
│   ├── raw/                  # Never modify. Source of truth.
│   │   ├── euroleague_players.csv
│   │   ├── euroleague_points.csv
│   │   └── players_bio.csv
│   └── processed/            # Derived data only.
│       └── merged_euroleague_players.csv
├── notebooks/
│   ├── EuroLeague_Unsupervised_Roles.ipynb        # Original analysis. Do not modify.
│   ├── 01_data_audit.ipynb                        # Internal source material. Do not modify.
│   ├── 02_coordinate_system_analysis.ipynb        # Internal source material. Do not modify.
│   └── EuroLeague_Player_Roles_Project.ipynb      # Main supervisor-facing project notebook.
├── outputs/
│   ├── figures/               # Includes figures/coordinates/ (internal supporting material).
│   └── tables/                # Includes tables/coordinates/ (internal supporting material).
├── src/
├── docs/
│   └── project-state.md
├── README.md
├── CLAUDE.md
├── CheckList.md               # Stage-by-stage project checklist (see below).
└── requirements.txt
```

## `CheckList.md` — the project roadmap

`CheckList.md` is the authoritative, stage-by-stage breakdown of the whole project, from data
understanding through the final Hebrew presentation, written by the user as a checkbox list.
Treat it the same way as `docs/project-state.md`: read it before starting a task, and keep it
in sync with what has actually been done.

- Each stage lists concrete checkbox items plus a short "Result of this stage" or "Decision
  required from this stage" note.
- When a task completes items in `CheckList.md`, tick the corresponding boxes (`- [x]`) and,
  if useful, fill in or update that stage's result/decision note — don't leave it stale.
- `docs/project-state.md`'s "Future tasks" section is a condensed summary; `CheckList.md` is
  the detailed source of truth for what each upcoming stage actually involves. If the two
  ever disagree, treat `CheckList.md` as authoritative for stage scope and
  `docs/project-state.md` as authoritative for decisions/results already made, and reconcile
  them rather than picking one silently.
- Do not renumber or restructure `CheckList.md`'s stages on your own initiative — it reflects
  the user's own plan. Add detail or tick boxes; don't redesign it without being asked.

## The project notebook is a student deliverable, not an agent report

`notebooks/EuroLeague_Player_Roles_Project.ipynb` is the main notebook Doron and Yuval will
submit to their supervisor, and later use as the factual basis for their presentation. It
must read as if two students wrote it about their own project — because that's what it is.
The user has manually edited this notebook directly at least once; treat manual edits the
same as any other authoritative change to the project.

**Internal working rules belong here and in `docs/project-state.md`, never in the notebook:**
task scopes, approval workflows, file-management rules, validation/compliance procedures,
completion reports, and instructions about how a notebook should be structured. The notebook
itself must contain only research-relevant explanations, implementations, results, and
decisions.

### Main notebook continuity — no visible task boundaries

The notebook is **one continuous academic project notebook**. It must never reveal where one
Claude Code task ended and another began. New work is integrated directly into the existing
research narrative — it must read as the next step Doron and Yuval took *because of* the
previous result, not as a new agent task starting up.

- Do not create visible task boundaries inside the notebook (no "this stage covers...", no
  restating scope, no summarizing what was just done as if closing out a ticket).
- Do not add sections titled (or effectively titled) `What's Next`, `Next Steps`,
  `Proposed Next Task`, `Task Summary`, `Task Completion`, `What This Notebook Covers`,
  `Notebook Scope`, `Setup`, `Implementation Plan`, `Decision Required`, or
  `Remaining Uncertainty`.
- Do not end the notebook by proposing or announcing future work. The next task is provided
  directly through Claude Code — it does not need to be proposed or announced inside the
  notebook. When the notebook currently ends at some stage, it may simply end after the last
  completed result and its interpretation.
- When a new project stage is implemented, continue naturally from the previous result, e.g.
  *"The previous checks showed that the three datasets can be combined using the
  player-season-team key. We therefore aggregated the shot events before joining them with
  the season-level statistics."* — then the implementation, result, explanation, and decision
  that follows from it.
- The notebook should eventually read as one uninterrupted process: understanding the
  problem, examining the data, preparing the data, building the features, selecting the
  method, training the model, evaluating the clusters, interpreting the discovered roles,
  comparing them with traditional positions, and presenting conclusions and limitations.
  These stages must never look like separate prompts or agent tasks.

### No meta-explanations

Do not explain ordinary notebook mechanics to the supervisor. In particular, do not add
Markdown explaining imports, repository-root detection, path handling, helper functions,
figure-export code, table-export code, random seeds, notebook execution, internal source
notebooks, Claude Code instructions, prompt boundaries, task approval, or why the notebook
follows a certain structure. Necessary setup code may remain in the notebook for
reproducibility, but it does not need a separate Markdown explanation unless it embeds a
genuinely research-relevant choice (e.g. a filtering rule, not the fact that a path is
resolved at runtime).

### Audience and voice

Concretely, the notebook must never:

- Mention Claude, AI assistance, prompts, task scopes, approval workflows, compliance, or any
  internal repository-management instruction.
- Use administrative/report-style section labels or templates — no "What is being checked",
  "Why it matters", "How this may affect the research", "Decision Required Before
  Continuing", "Remaining Uncertainty", "Objective / Implementation / Finding /
  Interpretation / Decision" headers, or similar QA-report scaffolding.
- Explain how the notebook itself was designed, why cells are ordered a certain way, or that
  a check was included "as required" — that belongs in this file, not the notebook.
- Use defensive or workflow-oriented wording, e.g. "We did not check everything that could
  theoretically be checked", "This task was intentionally limited to...", "This independently
  confirms...", "As required...", "The project owner must decide...", "This notebook was
  designed to...", "This section is included because...". State the research action and
  conclusion directly instead.
- Include a check, table, or figure just because it is technically possible to produce.
  Keep only what changes how the data is cleaned, joined, filtered, described, or modeled, or
  that the supervisor needs as a concrete fact.

Write in first-person plural ("we loaded...", "we found...", "we decided to..."), as Doron
and Yuval describing their own work. Use direct, practical, technically accurate English;
short-to-medium sentences; name the mechanism, then its purpose or result (Doron's usual
style) — not ornate academic prose, and not an AI-report template either. For each meaningful
step, cover: (1) what we wanted to determine, (2) what we implemented, (3) what the result
showed, (4) what we decided to do because of that result — as continuous prose, without
mechanically labeling each part as its own subsection. One clear visualization or check beats
several redundant ones proving the same point.

### Notebook introduction

The opening of the notebook should contain only what helps the supervisor understand the
project: title, authors, research question, motivation, and a short explanation of the
methodological goal. Do not add a contents summary explaining what the notebook will cover,
unless the notebook later becomes long enough to genuinely need a table of contents.

### One continuous main project notebook

Maintain **one continuous main project notebook** rather than separate per-task notebooks.
When a new stage of work is added, extend `EuroLeague_Player_Roles_Project.ipynb` rather than
creating another standalone notebook, unless asked otherwise. Exploratory/diagnostic work for
a new question may still happen in a scratch or internal notebook first, but only the
material that earns its place for the supervisor gets folded into the main notebook,
rewritten in the voice and scope described above.

### Source of truth — preserving manual edits

The user may edit `EuroLeague_Player_Roles_Project.ipynb` by hand at any time; the file on
disk is always authoritative over anything generated earlier in a conversation. Before every
future notebook task:

1. Read the current `EuroLeague_Player_Roles_Project.ipynb` in full.
2. Continue from its current final analytical result — do not assume the state described in
   an earlier conversation or in `docs/project-state.md` still matches the file.
3. Do not recreate sections the user removed, and do not replace manually revised prose with
   older generated wording.
4. Keep `01_data_audit.ipynb` and `02_coordinate_system_analysis.ipynb` as internal reference
   material only — do not pull their old report-style wording back into the main notebook.
5. Do not modify the main notebook outside the explicitly approved analytical task.

## Working conventions

- Notebooks must run top-to-bottom after Restart Kernel + Run All, from the repository root,
  without absolute local paths. Each notebook resolves the repository root at runtime.
- Do not write conclusions before the corresponding code output exists.
- **After `merge` (or any operation that can introduce `NaN` into a boolean column) followed
  by `.fillna(...)`, verify the resulting column's `dtype` is actually `bool` before applying
  `~` to it.** `fillna` alone does not fix an `object`-dtype column — `~` on Python `True`/
  `False` objects silently computes a bitwise complement (`~True == -2`, `~False == -1`)
  instead of a logical negation, with no error. This happened once in this project (a
  `has_event_data` flag built via `merge` + `fillna(False)`) and printed a wrong count without
  raising until a later cell tried to use it as a row mask. Cast explicitly with
  `.astype(bool)` after `fillna` whenever a flag column passes through a `merge`.
