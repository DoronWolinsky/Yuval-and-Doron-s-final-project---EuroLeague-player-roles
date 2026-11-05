# Research roadmap

This roadmap records the stages we planned for the project and, for each one, the question it had to answer, what we decided, and the evidence behind the decision.

The full analysis is in [`notebooks/EuroLeague_Player_Roles_Project.ipynb`](notebooks/EuroLeague_Player_Roles_Project.ipynb). Every number below comes from that notebook's outputs.

Two principles applied throughout:
- **Positions are not clustering inputs.** Traditional positions were never used to train the models. We used them only afterwards, to compare against the roles.
- **Roles are judged by meaning.** A role counts if it has a clear basketball meaning and draws distinctions that positions do not. Having more clusters than positions was never an argument in itself.

**Status:** the research stages (1–15) are complete. Only the recorded walkthrough (stage 16) remains.

---

## 1. Understanding the data

**Question:** What does one row of each source represent, and how can the sources be combined safely?

**Decision:**
- The unit of observation is the player-season-team. A player who changes teams mid-season gets one row per team. These rows are not duplicates.
- We joined the season totals, shot events and player biographies on season, player and team.
- We used the season totals for volume statistics and the event data only for shot location.

**Evidence:**
- The keys were unique, and all 19 seasons (E2007–E2025) were present in both files.
- Season and event shot-attempt counts agreed for 6,306 of 6,307 rows.
- Missing shot coordinates were stored as a `(-1, -1)` placeholder, which we excluded.

## 2. Building the player-season-team feature table

**Question:** Which playing-style measurements can be derived for each observation?

**Decision:**
- We expressed rates per 40 minutes, the length of a regulation game. We computed them from season totals, because the supplied per-game values mix playing time with playing style.
- We added shot-location summaries from the event coordinates.
- We kept undefined values missing at this stage rather than filling them.

**Evidence:** The result was one table of 6,307 player-season-team observations combining season statistics, per-40 rates, shot location, biography and coverage indicators.

## 3. Defining the eligible modeling sample

**Question:** How much playing time does an observation need before it represents a playing style rather than noise?

**Decision:** At least **5 games and 100 minutes**, which kept 4,568 of the 6,307 rows (72.4%). We kept 10 games / 200 minutes for a later robustness check.

**Evidence:**
- The participation distributions were strongly skewed and showed no natural cutoff. We therefore compared four rules: 5/100, 10/200, 10/300 and 15/400.
- The stricter rules also removed observations with substantial minutes and shot attempts. They cut some seasons as low as 96 or 49 rows.
- The chosen rule kept 196–273 rows in every season, and every eligible row had valid shot-location data.

## 4. Handling missing values

**Question:** Which missing values are genuine gaps, and how should each one be handled without using position?

**Decision:**
- **Heights.** We treated both `NaN` and `0` as missing heights. We replaced them only with externally verified values, recorded in `data/processed/height_overrides.csv` with sources in `zero_height_player_research.csv`.
- **Shooting percentages.** A recorded `0.0` with zero attempts is undefined, not a real 0%. We set these values to missing and, in the feature table, filled them with the median of the eligible shooters.
- **Position.** We left position missing where it was absent, because it is used only for comparison.

**Evidence:**
- 443 eligible rows had no three-point attempts, and 34 had no free-throw attempts.
- After the participation rule, no gaps remained in the shot-location features.

## 5. Selecting the features that define a role

**Question:** Which measurements describe *how* a player plays, rather than how good the player is or how much they play?

**Decision:** We selected 17 features:
- two- and three-point attempts per 40;
- the three shooting percentages;
- assists, turnovers, offensive and defensive rebounds, steals, blocks, fouls committed and fouls received per 40;
- height;
- three shot-location summaries: median shot distance, variation in shot distance and lateral spread.

We excluded:
- points, valuation and plus-minus, which are outcomes or quality measures;
- free-throw attempt measures, which overlap with fouls received;
- raw totals and playing-time fields;
- the A–J zone shares;
- all position columns.

**Evidence:**
- The zone letters mark different court areas in E2007–E2008 than in later seasons.
- A PCA of the seven coordinate summaries (93.6% of their variance in three components) produced one component that only described court side. We used three original summaries instead.
- The strongest remaining correlation was 0.826, between median distance and lateral spread.
- The two foul measures were nearly uncorrelated (r = 0.010).

## 6. Transforming and scaling the data

**Question:** How should unreliable percentages and differing scales be handled before distance- and likelihood-based clustering?

**Decision:**
- **Shrinkage.** In the modeling matrix, each shooting percentage became an attempt-weighted shrinkage estimate, `(makes + 10 · prior) / (attempts + 10)`. The priors were 0.531 for two-point, 0.363 for three-point and 0.764 for free-throw percentage.
- **Standardization.** We then standardized all 17 features.
- **No other transformations.** Skewed rates such as blocks and assists stayed untransformed, because their extremes are the role signal.

**Evidence:** Most extreme three-point and free-throw percentages came from very few attempts.

## 7. Exploring the structure with PCA

**Question:** Does the feature space contain separated groups, and should PCA be the clustering representation?

**Decision:** We used PCA for exploration only. Clustering used all 17 standardized features.

**Evidence:**
- PC1 (38.1% of the variance) ran from interior to perimeter play. PC2 (13.3%) measured on-ball offensive involvement.
- The PC1–PC2 projection showed a continuum of uneven density, not separated groups.
- The first two components kept little of several selected features.

## 8. K-Means baseline

**Question:** What does a simple partitioning method show about cluster structure?

**Decision:** We used K-Means with k = 4 as a weakly supported baseline for comparison, not as an estimate of the number of roles.

**Evidence:**
- Silhouette scores were low throughout: 0.299 at k = 2, 0.148 at k = 4 and 0.081 at k = 12.
- Inertia gains flattened after k = 4.
- No cluster was degenerate.

## 9. Gaussian mixture models and model selection

**Question:** How many components does a model with membership probabilities support?

**Decision:** We selected a full-covariance GMM with **five components** and `reg_covar = 0.01`.

**Evidence:**
- **Collapsed components.** With the default regularization, the BIC favoured k = 10. That solution had components collapsed onto legitimate zero values: the 443 rows without three-point attempts and the 865 rows without blocks. This was a likelihood artifact, not a set of real roles.
- **Regularized fits.** With `reg_covar` set to 0.01 or 0.1, no component collapsed, and the BIC was lowest at k = 5 under both settings.
- **Selected setting.** Under 0.01, the BIC was 155,866 at k = 5. k = 6 was 23 higher and k = 4 was 884 higher.
- **Membership certainty.** 77.1% of observations had a maximum membership probability of at least 0.9.

## 10. Robustness

**Question:** Is the result an accident of one initialization or of the participation threshold?

**Decision:** We treated the five-component solution as stable.

**Evidence:**
- **Initializations.** Across ten random initializations, the mean pairwise ARI was 0.978 (minimum 0.929), and at least 96.8% of observations kept their component.
- **Stricter threshold.** We refitted the full pipeline on the 10 games / 200 minutes sample (3,679 rows). The BIC again chose k = 5, and the ARI with the main model on the shared rows was 0.887.

## 11. Interpreting the roles

**Question:** Do the components have coherent basketball meaning?

**Decision:** We named the five roles **playmaking guards**, **low-post centers**, **low-usage forwards**, **perimeter shooters** and **mobile stretch bigs**. No component needed revision.

**Evidence:**
- Standardized and raw-unit component profiles.
- Three representative observations per component, chosen as those closest to the component mean by Mahalanobis distance.
- One multi-season example: Alberto Abalde's assignments changed after he moved from Valencia Basket to Real Madrid.

## 12. Comparing roles with traditional positions

**Question:** Do the roles reveal distinctions that the five traditional positions do not?

**Decision:** The roles add information beyond the positions. The evidence is the specific splits and merges below; low agreement on its own would not show this.

**Evidence:**
- Centers split into low-post centers (69%) and mobile stretch bigs (24%).
- Point Guards and Shooting Guards shared the same two roles in reversed proportions.
- Low-usage forwards and mobile stretch bigs each combined two positions.
- The ARI with the positions was 0.210.

## 13. Answering the research question

**Decision:**
- The roles are interpretable, data-driven patterns of play that complement traditional positions.
- Without an independent validation criterion, we make no claim that they are more accurate than positions.
- The limitations cover:
  - the participation threshold;
  - the feature and shrinkage choices;
  - the close k = 6 alternative;
  - undocumented shot coordinates;
  - overlapping roles;
  - repeated players;
  - imperfect position labels. 365scores and Wikipedia disagreed for 383 of 1,141 players.

## 14–15. Final review and HTML report

We did a full editorial and consistency review of the notebook. We then rendered it from its saved outputs to [`outputs/EuroLeague_Player_Roles_Project.html`](outputs/EuroLeague_Player_Roles_Project.html).

---

## 16. Recorded walkthrough (remaining)

A walkthrough of the final notebook, about 20 minutes long and recorded in Hebrew by Doron and Yuval. It should cover the research question and data, the sample and feature decisions, PCA, the K-Means and GMM comparison and the covariance-collapse finding, the roles and their comparison with positions, and the conclusions and limitations.

- [ ] Recorded
