# Discovering EuroLeague Player Roles with Unsupervised Learning

**Doron and Yuval**

Traditional basketball positions say little about how a player actually plays. Can unsupervised learning find meaningful player roles in performance data alone? And do those roles distinguish players in ways that positions do not?

**[Full report (HTML)](outputs/EuroLeague_Player_Roles_Project.html)** · **[Research notebook](notebooks/EuroLeague_Player_Roles_Project.ipynb)**

GitHub shows the HTML as source code, so download it to view it in a browser. The notebook renders directly on GitHub, with all outputs saved.

---

## Data

- **Season statistics:** 6,307 player-season-team observations, covering 19 EuroLeague seasons (E2007–E2025).
- **Shot events:** 755,145 recorded shots with court coordinates.
- **Biographies:** 2,363 players, with height and the league's three broad position categories.

The season statistics and shot events come from the [EuroLeague & EuroCup Datasets](https://www.kaggle.com/datasets/babissamothrakis/euroleague-datasets) on Kaggle, and the biographies from the EuroLeague API. The shot-event file exceeds GitHub's size limit, so it is not included.

**Position enrichment.** The league records only Guard, Forward and Center, so we built five-position labels (Point Guard to Center) ourselves:
- **365scores.** We collected positions by **web scraping**. We then removed 27 incorrect matches to coaches and general managers, leaving 1,341 players with valid labels.
- **Wikipedia.** We resolved 1,900 of 2,363 players through the Wikipedia API, verifying identity mainly by birth year.
- **Combining the sources.** 365scores took priority where both sources gave a position, and Wikipedia filled the gaps. The combined label covers 97.8% of the modeling sample.

The labels were **never used as clustering inputs**, only afterwards to interpret the roles.

**Height repair.** `players_bio.csv` marks missing heights with both `NaN` and `0`. We verified 62 players' heights against external sources, which corrected 198 eligible rows.

## Method

**Sample.**
- We kept observations with at least **5 games and 100 minutes**: 4,568 rows (72.4%), with every season represented by 196–273 rows.
- The participation distributions showed no natural cutoff. We compared four rules, and the stricter ones removed real rotation roles along with the noise.

**Features (17).**
- **Rates per 40 minutes, computed from season totals:** two- and three-point attempts, assists, turnovers, offensive and defensive rebounds, steals, blocks, and fouls committed and received.
- **The three shooting percentages.** Their extreme values came mostly from very few attempts, so in the modeling matrix we used an attempt-weighted shrinkage estimate, `(makes + 10·prior) / (attempts + 10)`.
- **Height.**
- **Three shot-location summaries** from the raw coordinates: median shot distance, its variation, and lateral spread. The A–J zone labels covered different court areas in E2007–E2008 than in later seasons, so we excluded them. We also tested and rejected a PCA of the coordinate summaries, because one component only captured court side.
- **Excluded as outcome, quality or playing-time measures:** points, valuation, plus-minus and minutes.

All features were standardized. PCA served only for exploration: PC1 (38.1% of the variance) runs from interior to perimeter play, and the projection shows a continuum rather than separated groups.

**K-Means vs. GMM.**
- **Baseline.** K-Means with k = 2–12 gave low silhouette scores (0.299 at k = 2, falling to 0.081 at k = 12), consistent with overlapping playing styles.
- **Why a mixture model.** A Gaussian mixture model (GMM) gives each observation membership probabilities, which suit that kind of structure, and it lets the Bayesian information criterion (BIC) guide the number of components.
- **Agreement.** GMM and K-Means partitions agreed only moderately: ARI 0.409 between K-Means with k = 4 and the selected five-component GMM.

**Covariance collapse.**
- **The problem.** With default regularization (`reg_covar = 1e-6`), BIC appeared to favour **k = 10**. That solution contained collapsed components built on legitimate zero values: the 443 rows with no three-point attempts and the 865 rows with no blocks. The near-zero variance inflated the likelihood, so the apparent preference for k = 10 was an artifact, not evidence of extra roles.
- **The fix.** With `reg_covar` set to 0.01 or 0.1, no component collapsed, and BIC was lowest at **k = 5** under both settings.
- **The selected model.** Under 0.01 the BIC was 155,866. k = 6 was a close second (ΔBIC = 23), and k = 4 was well behind (ΔBIC = 884).
- **Membership certainty.** 77.1% of observations have a maximum membership probability of at least 0.9.

**Robustness.**
- **Random initializations.** Across ten initializations, the mean pairwise ARI was 0.978 (minimum 0.929), and at least 96.8% of observations kept their component.
- **Stricter threshold.** We refitted the full pipeline on a 10 games / 200 minutes sample (3,679 rows). BIC again chose k = 5, and the ARI with the main model on the shared rows was 0.887.

## Results

| Role | Observations | Profile |
|---|---:|---|
| Playmaking guards | 1,054 | High assists and turnovers; shorter; little rebounding |
| Low-post centers | 756 | Almost no three-point attempts; narrow shot locations; tallest; most rebounds and blocks |
| Low-usage forwards | 976 | Flattest profile; few turnovers and fouls drawn |
| Perimeter shooters | 1,162 | Longest shot distance; most three-point attempts; fewest two-point attempts |
| Mobile stretch bigs | 620 | Tall, with high rebounding and blocks, but wider shot locations and some three-point shooting |

**Beyond traditional positions.**
- **Centers split.** 69% were low-post centers and 24% were mobile stretch bigs.
- **Guards split by style.** Point Guards and Shooting Guards divided between the same two roles in reversed proportions. Point Guards were 54% playmaking guards and 40% perimeter shooters; Shooting Guards were 36% and 44%. The split reflects ball-handling versus shooting more than the nominal position.
- **Two roles combine positions.** Low-usage forwards were 38% Small Forwards and 37% Power Forwards; mobile stretch bigs were 50% Power Forwards and 31% Centers.
- **Limited agreement.** The adjusted Rand index (ARI) between the roles and the positions was 0.210. A low ARI alone does not show that the roles are better. Together with the splits above, it shows that the roles and positions divide players differently.

The roles **complement** traditional positions. Showing that they are more *accurate* would require an independent validation criterion, and none was available.

## Limitations

- **Analysis choices.** The participation threshold, the feature set, the shrinkage of shooting percentages and the regularization all shape the result. k = 6 was a close alternative.
- **Shot coordinates.** The units are undocumented, and consistent recording across all seasons has not been established.
- **Overlapping roles.** 3.5% of observations have a maximum membership probability below 0.6.
- **Repeated players.** A player appears once per season and team, so role sizes count observations, not distinct players.
- **Imperfect position labels.** Where both sources gave a position, 365scores and Wikipedia disagreed for 383 of 1,141 players. Each player has one label for all seasons, and 2.2% of eligible observations have no five-category label.

## Repository contents

- **`notebooks/EuroLeague_Player_Roles_Project.ipynb`:** the full analysis, with saved outputs.
- **`outputs/EuroLeague_Player_Roles_Project.html`:** the rendered report.
- **`data/raw/`:** season statistics (`euroleague_players.csv`) and player biographies (`players_bio.csv`).
- **`data/processed/`:**
  - the 365scores and Wikipedia position tables;
  - the verified height overrides;
  - `player_season_team_features_with_position.csv`, the final feature table with position labels.
