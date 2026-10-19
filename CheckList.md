# EuroLeague Player Roles — Project Checklist

## Project Goal

Our goal is to use unsupervised machine learning to discover meaningful EuroLeague player roles based on how players actually play.

The model will not receive traditional position labels such as Guard, Forward, or Center. We will use these labels only after clustering, to examine whether the discovered roles provide a more detailed description of modern EuroLeague players.

The notebook should present the project as one continuous investigation. At every stage, we should explain:

- What we wanted to understand.
- Which method we used and why.
- What the results showed.
- Whether the results matched our expectations.
- What we decided to do because of those results.
- How that decision led to the next stage.

If an approach does not produce a useful result, we should show that honestly and explain why we tested a different approach.

The items below are the research decisions each stage has to settle, not a list of every possible diagnostic. We run a check, plot, or comparison only when it informs one of those decisions.

---

## 1. Understand and Examine the Data — Completed

- [x] Understand what one row represents in each dataset.
- [x] Identify the correct keys for connecting the datasets.
- [x] Check duplicate identifiers and key uniqueness.
- [x] Examine season coverage and determine whether entire periods are missing.
- [x] Examine missing values and determine what each type of missing value means.
- [x] Identify inconsistent or unreliable source columns.
- [x] Examine whether event types were recorded consistently across seasons.
- [x] Determine how mid-season team transfers should be represented.
- [x] Verify that joining the datasets does not duplicate or remove observations.
- [x] Interpret the shot-coordinate system and identify invalid coordinate placeholders.
- [x] Explain which data can be used and which data should not be used.

### Result of this stage

We determined that the appropriate unit of observation is one player-season-team. We also identified which source fields are reliable, how the datasets should be combined, and which missing values represent unavailable information rather than actual zero values.

---

## 2. Build the Player-Season-Team Feature Table — Completed

- [x] Use the season-level player statistics as the base table.
- [x] Add player biography information such as height and traditional position.
- [x] Calculate playing-style statistics from the season totals.
- [x] Calculate per-40-minute rates (one EuroLeague regulation game) instead of relying on inconsistent supplied per-game columns.
- [x] Add shooting-volume and shooting-selection features.
- [x] Aggregate shot-location information by player, season, and team.
- [x] Add coordinate and shot-zone features.
- [x] Add playmaking features such as assists and turnovers.
- [x] Add rebounding features.
- [x] Add defensive features such as steals and blocks, following the supervisor’s recommendation.
- [x] Keep traditional position outside the clustering features.
- [x] Preserve undefined or structurally missing values instead of filling them with invented behavior.
- [x] Produce one complete player-season-team feature table.

### Result of this stage

We produced a table containing 6,307 player-season-team observations and 76 columns. This table combines season statistics, per-40 rates, shooting behavior, shot-location information, biography data, and coverage indicators.

This is the complete feature table, but it is not yet the final modeling matrix.

---

## 3. Define the Eligible Modeling Sample — Completed

- [x] Examine the distributions of minutes played, games played, and shot attempts.
- [x] Determine how little playing time makes a player-season-team observation too unstable to represent a meaningful role.
- [x] Compare several reasonable participation thresholds.
- [x] Examine how each threshold changes the number of retained observations.
- [x] Check whether the retained sample still represents every EuroLeague season.
- [x] Check which kinds of players are removed by each possible threshold.
- [x] Select a final participation rule based on both statistical reliability and basketball logic.
- [x] Explain why the selected sample is appropriate for discovering player roles.
- [x] Keep the complete feature table unchanged and create an eligibility indicator for the modeling sample.

### Result of this stage

We compared four candidate rules (5 games/100 minutes, 10 games/200 minutes, 10 games/300 minutes, 15 games/400 minutes) and selected **5 games and 100 minutes**. It keeps 4,568 of the 6,307 player-season-team rows (72.4%), represents all 19 seasons with 196-273 eligible rows each, and every eligible row already has valid spatial data and at least one field-goal attempt. The stricter alternatives removed substantially more rows, including observations with meaningful minutes, shot attempts, and points, which would have biased the sample toward established rotation players.

The complete 6,307-row feature table is unchanged and now carries a boolean `eligible_for_modeling` column (`data/processed/player_season_team_features.csv`) rather than being replaced by a filtered copy. `10 games / 200 minutes` is kept in reserve as a sensitivity check for Stage 10, after clustering.

---

## 4. Handle Missing Values in the Eligible Sample — Completed

- [x] Recalculate missing-value counts after selecting the eligible sample.
- [x] Separate genuinely missing measurements from values that are undefined because a player had no relevant attempts.
- [x] Decide whether height should be included as a clustering feature.
- [x] If height is included, resolve missing height values without using traditional position (done by external verification of each player's height).
- [x] Do not use traditional position to estimate height or any other clustering feature.
- [x] Do not fill missing traditional positions, since position will only be used for later comparison.
- [x] Do not invent average shot-location behavior for players without valid spatial information.
- [x] Decide whether observations that still lack required modeling features should be excluded or handled differently.
- [x] Explain every imputation or exclusion according to what the missing value means in this project.

### Result of this stage

Recalculating missingness on the 4,568 eligible rows showed that the participation rule already eliminated every spatial location, spread, and shot-selection gap. Three genuine gaps remained: `height_cm` (31 rows), a structural-zero ambiguity in the shooting-percentage columns (`0.0` recorded for zero attempts, not a real 0% -- 443 rows for three-point percentage, 34 for free-throw percentage), and `position` (132 rows, comparison-only).

We decided both height and shooting efficiency belong in the clustering feature set. For height, since it's a fixed, look-up-able physical fact rather than a behavior to estimate, we manually verified the 11 missing players from external sources (cited in `data/processed/height_overrides.csv`) instead of imputing a statistic. For shooting efficiency, we first corrected the structural-zero ambiguity itself -- setting the percentage to a genuine missing value whenever attempts are zero, and adding `has_three_point_attempts`/`has_free_throw_attempts` flags so that behavior isn't lost -- then filled the resulting gaps with the median computed only from eligible rows that did attempt that shot type, never from position, keeping every row in the modeling sample without inventing a specific skill level. `position` was left exactly as it was: it's comparison-only, so a missing value there doesn't block anything and was never a candidate for filling.

The eligible sample now has zero missing values across every candidate clustering feature.

A later data-quality check found that `players_bio.csv` uses `0`, not only `NaN`, as a missing-height sentinel for some players -- a distinct condition the original `height_cm` gap analysis above did not catch. 51 additional players carrying this `0` sentinel (167 eligible rows) were identified inside the eligible sample and externally verified the same way as the original 11 (365Scores preferred, Wikipedia fallback), and added to `data/processed/height_overrides.csv` (11 -> 62 rows). These are verified physical measurements, not imputed values, and the override is restricted to verified `player_id`s, replacing only `NaN` or `0`. The eligible sample remains 4,568 rows. Detailed provenance: `data/processed/zero_height_player_research.csv`.

---

## 5. Select the Final Features That Define a Player Role — Completed

- [x] Review the available feature groups:
  - scoring volume;
  - two-point, three-point, and free-throw usage;
  - shooting efficiency;
  - shot selection and court location;
  - assists and turnovers;
  - offensive and defensive rebounding;
  - steals and blocks;
  - fouls;
  - height.
- [x] Decide which features describe playing style rather than general player quality.
- [x] Keep identifiers, names, seasons, and teams outside the clustering input.
- [x] Keep traditional position outside the clustering input.
- [x] Exclude `valuation` and `plus_minus` unless there is a clear reason to treat them as role features.
- [x] Examine feature distributions.
- [x] Examine correlations between candidate features.
- [x] Identify features that repeat nearly the same information.
- [x] Avoid including several mathematical versions of the same behavior without justification.
- [x] Decide whether shooting percentages should define the clusters or only describe them afterwards.
- [x] Decide whether height should influence the discovered roles or be reserved for interpretation.
- [x] Compare important alternative feature sets when the correct choice is unclear.
- [x] Define and explain the final set of clustering features.

### Decision required from this stage

We need to decide what we mean by a “player role” in numerical terms.

The final feature set should capture how a player contributes and behaves on the court. It should not allow general player quality, playing time, or traditional position labels to dominate the discovered groups.

### Result of this stage

The final clustering feature set has 17 features, with every rate expressed per 40 minutes (one EuroLeague regulation game): two- and three-point attempts per 40; two-point, three-point, and free-throw percentage; assists and turnovers per 40; offensive and defensive rebounds per 40; steals, blocks, and fouls committed per 40; fouls received per 40; `height_cm`; and the shot-location profile `median_raw_shot_distance`, `raw_shot_distance_std`, and `lateral_shot_position_std`. The ordered list is `FINAL_CLUSTERING_FEATURES` in the notebook; every column's decision is recorded in `outputs/tables/final_clustering_feature_decisions.csv` and in the feature dictionary.

- The A-J zone shares are descriptive/QA only: an initial 17-variable spatial PCA showed a component separating E2007-E2008 from later seasons, and the undocumented zone letters mark different court areas in those seasons. No historical zone relabelling is applied.
- A PCA of the seven coordinate summaries (three components, 93.6% of their variance) was tested and not used: one component was only court side, and seven variables did not justify abstract components. Three original summaries were selected from their correlations instead.
- Both foul measures are kept: they are nearly uncorrelated (r = 0.010). Fouls committed per 40 correlates -0.57 with minutes per game, which we accept as a moderate, non-duplicating relationship.
- Excluded: points per 40 (outcome of volume and efficiency), free-throw attempts per 40 and free-throw attempt rate (overlap with fouls received), season and event attempt shares, raw totals, playing-time and coverage fields, `valuation`, `plus_minus`, identifiers, and all position columns.
- The strongest correlation among the final features is 0.826 (median shot distance with lateral spread); no near-duplicate remains.

---

## 6. Transform and Scale the Modeling Data — Completed

- [x] Stabilize shooting percentages that rest on very few attempts, so they do not become extreme modeling values.
- [x] Standardize the final features so that variables with larger numerical scales do not dominate the distance-based clustering algorithms.
- [x] Keep the other selected feature representations; transform a feature or remove an observation only for a substantive basketball or data reason, not because a distribution is skewed or a player is unusual.
- [x] Create the final modeling matrix, keeping the observation identifiers alongside it so later results can be mapped back to players.

### Result of this stage

The three shooting percentages are replaced in the modeling matrix by an attempt-weighted shrinkage estimate, `(makes + 10 * prior_mean) / (attempts + 10)`, with the prior the eligible-sample attempt-weighted percentage (0.531 2P%, 0.363 3P%, 0.764 FT%). Before the adjustment, 25 of 26 extreme 3P% values and 25 of 33 extreme FT% values (|z| > 3) came from 1-9 attempts; afterwards only one extreme value across the three features does. This supersedes the Stage 4 median fill for modeling; zero-attempt rows receive the prior mean. The feature table keeps its Stage 4 percentage representation, while the modeling matrix uses the Stage 6 shrinkage-adjusted estimates.

The 17 features in `FINAL_CLUSTERING_FEATURES` are then standardized with `StandardScaler`, fitted on the 4,568 eligible rows, into a 4,568 × 17 matrix (`X_scaled`, kept in notebook state with the feature-table index; identifiers in `modeling_metadata`). The other 14 features are not transformed: the skewed rates such as `blocks_per_40` and `assists_per_40` reflect distinctive roles that the clustering should be able to find.

---

## 7. Explore the Data Using PCA — Completed

- [x] Apply PCA to the scaled modeling matrix and examine how much variance the first components explain.
- [x] Interpret the main component loadings: which combinations of playing-style features drive the largest differences between players.
- [x] Create a two-dimensional PCA projection and describe whether it shows separated groups, overlapping groups, or gradual transitions.
- [x] Decide whether PCA is used only for exploration and visualization or also as the clustering representation, and explain why.

The two-dimensional projection simplifies a 17-dimensional dataset. It helps us understand and present the structure, but it does not by itself determine how many roles exist.

### Result of this stage

PCA of `X_scaled` gives PC1 38.1%, PC2 13.3%, and PC3 7.2% of the variance (51.5% for two components, 58.7% for three); PC4-PC10 each explain 3.1-6.1%, and eight components are needed to pass 80%. PC1 is an interior-to-perimeter axis (rebounds, height, blocks, two-point attempts against three-point attempts, shot distance, and lateral spread); PC2 is on-ball offensive involvement (turnovers, fouls received, assists, two-point attempts); PC3 is a weaker contrast of three-point and free-throw percentage against fouls committed and steals. The PC1-PC2 plane keeps little of three-point percentage (0.04), steals (0.10), fouls committed (0.18), and two-point and free-throw percentage (0.28 each).

The PC1-PC2 projection shows overlapping regions of uneven density along a continuous spectrum, not separated groups. We decided to use PCA only for exploration and visualization: K-Means and GMM use the 17 standardized features, because no small number of components captures most of the variance and the discarded directions carry selected role features.

---

## 8. Establish a K-Means Baseline — Completed

- [x] Run K-Means over a reasonable range of cluster counts.
- [x] Use the elbow curve and/or silhouette scores as evidence for sensible cluster counts.
- [x] Inspect cluster sizes to rule out obviously poor solutions.
- [x] Choose a K-Means baseline to compare with GMM.

K-Means is a simple baseline for the model comparison. Detailed cluster profiles are interpreted only for the final model (Stage 11).

### Result of this stage

K-Means on `X_scaled` for k = 2-12 (20 initializations each). Inertia gains drop sharply after k = 4 (6,490 for the third cluster, 3,856 for the fourth, 1,746 for the fifth, then 1,468 down to 595). Silhouette (all 4,568 rows) is highest at k = 2 (0.299) and declines steadily (0.148 at k = 4, 0.081-0.098 from k = 7), confirming overlapping rather than separated groups. Cluster sizes were checked only for degenerate or suspiciously small clusters, not as a preference for balance; none was found (smallest at k = 12: 300 rows). k = 2 is valid but mainly captures the broad interior-perimeter split along PC1, so it is of little use as a baseline. The selected practical baseline is **k = 4** (silhouette 0.148, where inertia gains flatten); the support is weak and k = 5 is a similarly reasonable alternative. The baseline is a reference for the model comparison, not an estimate of the number of roles; the final model and number of clusters are chosen in Stage 9 on their own evidence.

---

## 9. Fit Gaussian Mixture Models and Select the Final Model

- [ ] Fit GMMs over a justified range of cluster counts, without assuming the preliminary eight-cluster result.
- [ ] Use BIC as the main criterion for the number of components; add AIC only if it adds useful evidence.
- [ ] Check the cluster sizes of the leading solutions for very small or degenerate clusters.
- [ ] Summarize membership certainty if it helps the model choice.
- [ ] Compare the leading GMM solution with the K-Means baseline.
- [ ] Select the preferred model and number of clusters, based on the statistical evidence, cluster sizes, and whether the clusters are interpretable.

---

## 10. Check the Robustness of the Result

- [ ] Repeat the preferred clustering with different random initializations and check that observations stay grouped together.
- [ ] Rerun it on the stricter `10 games / 200 minutes` sample reserved in Stage 3 and check whether the main role structure holds.
- [ ] Run at most one further sensitivity comparison, only if the final model leaves a concrete methodological uncertainty (for example a feature group or the recording period that appears to drive a cluster).

The goal is to show that the main result is not an accident of one initialization or one arbitrary choice. If an alternative setup changes the result, we report it and explain which solution better answers the research question.

---

## 11. Interpret the Discovered Roles

- [ ] Summarize each cluster's profile in original units and/or standardized values, and identify the features that most distinguish it.
- [ ] Inspect representative players from each cluster (for example those closest to the center or with the highest membership probability).
- [ ] Assign each interpretable cluster a basketball role name supported by both its numerical profile and its player examples.
- [ ] Use a multi-season or team-change example only when it genuinely helps illustrate a role or role change.
- [ ] Revise the model only if a cluster is genuinely incoherent.

Role names are not chosen in advance; they must follow from the final cluster profiles. Player examples support the numerical profile rather than replace it.

---

## 12. Compare the Discovered Roles with Traditional Positions

- [ ] Show how the discovered roles are distributed across the traditional positions, using both the 3-category `position` and the 5-category `position_reconciled`.
- [ ] Examine whether players with the same position are split into meaningfully different roles, and whether players from different positions are combined when they play alike.
- [ ] Decide whether the discovered roles add useful information beyond the position labels.
- [ ] State how many observations lack a position label, and treat it further only if it affects the interpretation.

The goal is not to predict the position labels but to see whether the discovered roles reveal distinctions the labels do not show. Position is used here only after clustering, never as a clustering input.

---

## 13. Answer the Research Question

- [ ] Summarize the final roles.
- [ ] Explain why the model and number of clusters were selected.
- [ ] State whether the result was reasonably robust.
- [ ] Explain whether the roles are meaningful in basketball terms and whether they add information beyond traditional positions.
- [ ] Discuss the main limitations, separating strong conclusions from tentative ones.

### Limitations to consider

- The participation threshold that defines the modeling sample.
- The discovered roles depend on the chosen 17-feature representation and preprocessing decisions.
- Event types and zone letters are not recorded consistently across seasons, so dunks, layups, and shot zones could not be used.
- Shot distances are in undocumented raw coordinate units.
- Possible historical changes in EuroLeague playing style across the 19 seasons.
- The assumptions of K-Means and GMM.
- Player-season-team observations allow the same player to appear more than once.
- Position labels are missing for some eligible observations, which limits the position comparison.

---

## 14. Final Notebook Review

- [ ] Do one complete editorial and consistency read of the notebook, removing redundancy and making sure every conclusion follows visible evidence.
- [ ] Make sure the notebook reads naturally in first-person plural as Doron and Yuval and ends with the conclusions and limitations.
- [ ] Render the notebook as HTML and inspect the final HTML.

---

## 15. Prepare the Hebrew Presentation

- [ ] Build the presentation only after the notebook results are final, from its strongest results.
- [ ] Present the research question, data, key preparation decisions, and how the sample and features were chosen.
- [ ] Explain the PCA view, the K-Means/GMM comparison, and how the number of clusters was chosen.
- [ ] Present the discovered roles with representative players and the comparison with traditional positions.
- [ ] Include a methodological change or unexpected result only where it helps tell the research story.
- [ ] Present the conclusions and limitations.
- [ ] Divide the presentation between Doron and Yuval, make sure both can explain every major decision, and rehearse a talk of about 40 minutes.
- [ ] Record the presentation if required.

---

## Final Project Acceptance Check

- [ ] The notebook runs top to bottom and renders correctly as HTML.
- [ ] Traditional position was never used as a clustering input.
- [ ] The final model and number of clusters are justified.
- [ ] The discovered roles are interpretable and supported by data and player examples.
- [ ] The comparison with traditional positions answers the research question.
- [ ] The presentation accurately reflects the final notebook.
