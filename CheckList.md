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
- [x] Calculate per-36-minute rates instead of relying on inconsistent supplied per-game columns.
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

We produced a table containing 6,307 player-season-team observations and 76 columns. This table combines season statistics, per-36 rates, shooting behavior, shot-location information, biography data, and coverage indicators.

This is the complete feature table, but it is not yet the final modeling matrix.

---

## 3. Define the Eligible Modeling Sample

- [ ] Examine the distributions of minutes played, games played, and shot attempts.
- [ ] Determine how little playing time makes a player-season-team observation too unstable to represent a meaningful role.
- [ ] Compare several reasonable participation thresholds.
- [ ] Examine how each threshold changes the number of retained observations.
- [ ] Check whether the retained sample still represents every EuroLeague season.
- [ ] Check which kinds of players are removed by each possible threshold.
- [ ] Select a final participation rule based on both statistical reliability and basketball logic.
- [ ] Explain why the selected sample is appropriate for discovering player roles.
- [ ] Keep the complete feature table unchanged and create an eligibility indicator for the modeling sample.

### Decision required from this stage

We need to decide which player-season-team observations contain enough playing time and activity to represent a reliable playing role.

The decision should not be based only on choosing a convenient number. We should show how different thresholds affect the data and explain why the selected threshold gives the best balance between reliability and sample coverage.

---

## 4. Handle Missing Values in the Eligible Sample

- [ ] Recalculate missing-value counts after selecting the eligible sample.
- [ ] Separate genuinely missing measurements from values that are undefined because a player had no relevant attempts.
- [ ] Decide whether height should be included as a clustering feature.
- [ ] If height is included, fill missing height values using a method calculated only from the eligible sample.
- [ ] Do not use traditional position to estimate height or any other clustering feature.
- [ ] Do not fill missing traditional positions, since position will only be used for later comparison.
- [ ] Do not invent average shot-location behavior for players without valid spatial information.
- [ ] Decide whether observations that still lack required modeling features should be excluded or handled differently.
- [ ] Explain every imputation or exclusion according to what the missing value means in this project.

### Decision required from this stage

We need to create a modeling dataset without treating every missing value as the same problem. Any value we fill must have a reasonable interpretation, and we must avoid creating artificial playing behavior that was not observed.

---

## 5. Select the Final Features That Define a Player Role

- [ ] Review the available feature groups:
  - scoring volume;
  - two-point, three-point, and free-throw usage;
  - shooting efficiency;
  - shot selection and court location;
  - assists and turnovers;
  - offensive and defensive rebounding;
  - steals and blocks;
  - fouls;
  - height.
- [ ] Decide which features describe playing style rather than general player quality.
- [ ] Keep identifiers, names, seasons, and teams outside the clustering input.
- [ ] Keep traditional position outside the clustering input.
- [ ] Exclude `valuation` and `plus_minus` unless there is a clear reason to treat them as role features.
- [ ] Examine feature distributions.
- [ ] Examine correlations between candidate features.
- [ ] Identify features that repeat nearly the same information.
- [ ] Avoid including several mathematical versions of the same behavior without justification.
- [ ] Decide whether shooting percentages should define the clusters or only describe them afterwards.
- [ ] Decide whether height should influence the discovered roles or be reserved for interpretation.
- [ ] Compare important alternative feature sets when the correct choice is unclear.
- [ ] Define and explain the final set of clustering features.

### Decision required from this stage

We need to decide what we mean by a “player role” in numerical terms.

The final feature set should capture how a player contributes and behaves on the court. It should not allow general player quality, playing time, or traditional position labels to dominate the discovered groups.

---

## 6. Transform and Scale the Modeling Data

- [ ] Examine whether some selected features have strongly skewed distributions.
- [ ] Identify extreme values and determine whether they are data problems or legitimate unusual player styles.
- [ ] Test appropriate transformations where needed.
- [ ] Compare transformed and untransformed distributions when the benefit is uncertain.
- [ ] Avoid removing unusual players only because they are different from the majority.
- [ ] Standardize the final features so that variables with larger numerical scales do not dominate the clustering algorithms.
- [ ] Create the final modeling matrix.
- [ ] Record the final ordered feature list and the preprocessing applied to each feature.

### Result expected from this stage

We will have a numerical matrix in which every row represents an eligible player-season-team observation and every column represents a justified aspect of playing style.

---

## 7. Explore the Data Using PCA

- [ ] Apply PCA to the scaled modeling features.
- [ ] Examine the cumulative explained variance.
- [ ] Determine how much of the original information is represented by the first principal components.
- [ ] Examine the component loadings.
- [ ] Explain which combinations of playing-style features drive the main differences between players.
- [ ] Create a two-dimensional PCA scatter plot.
- [ ] Use the PCA plot to examine whether the data appears to contain separated groups, overlapping groups, or gradual transitions.
- [ ] Decide whether PCA will be used only for visualization or also as an input representation for clustering.
- [ ] Explain the reasoning behind that decision.

### Important interpretation

The two-dimensional PCA plot is a simplified projection of a higher-dimensional dataset. It can help us understand and present the structure, but it does not by itself determine how many player roles exist.

---

## 8. Establish a K-Means Clustering Baseline

- [ ] Apply K-Means to a reasonable range of possible cluster counts.
- [ ] Examine the elbow curve.
- [ ] Calculate silhouette scores.
- [ ] Examine the size of the clusters produced by each candidate solution.
- [ ] Create a PCA visualization colored by the K-Means clusters.
- [ ] Examine whether the resulting groups appear meaningfully separated.
- [ ] Analyze the average feature profile of the K-Means clusters.
- [ ] Determine whether the K-Means assumptions produce a useful representation of the player roles.

### Purpose of this stage

K-Means provides a simple and interpretable clustering baseline. We will use it to understand the structure of the data and later compare it with Gaussian Mixture Models.

If K-Means produces groups that are difficult to interpret or that appear artificially rigid, we should explain this and examine whether GMM provides a better description.

---

## 9. Apply Gaussian Mixture Models

- [ ] Apply Gaussian Mixture Models to a justified range of possible cluster counts.
- [ ] Calculate BIC for every candidate number of clusters.
- [ ] Use BIC as the primary data-driven method for comparing the GMM solutions, as proposed in the original project.
- [ ] Examine AIC as supporting information if it adds useful evidence.
- [ ] Do not automatically assume that the preliminary result of eight clusters is still optimal.
- [ ] Examine cluster sizes for every leading solution.
- [ ] Check whether any solution creates extremely small or difficult-to-explain clusters.
- [ ] Examine the membership probabilities produced by GMM.
- [ ] Identify players with high-confidence membership.
- [ ] Identify players whose behavior lies between multiple roles.
- [ ] Create a PCA visualization colored by the GMM clusters.
- [ ] Compare the GMM solution with the K-Means baseline.
- [ ] Select the preferred model and number of clusters.

### Decision required from this stage

The final model should be selected using a combination of:

- BIC and other relevant statistical evidence;
- cluster sizes;
- stability;
- visual structure;
- clarity of the cluster profiles;
- basketball interpretability.

The preliminary eight-cluster result is important evidence of feasibility, but the final result must be recalculated using the expanded feature set and the complete modeling process.

---

## 10. Check the Stability of the Clustering Result

- [ ] Repeat the preferred clustering with different random initializations.
- [ ] Check whether similar observations remain grouped together across runs.
- [ ] Examine whether a small change in the participation threshold changes the main result.
- [ ] Compare important alternative feature sets, such as:
  - with and without height;
  - with and without shooting efficiency;
  - full feature space versus a PCA-based representation.
- [ ] Examine whether clusters are dominated by particular seasons or historical periods.
- [ ] Determine which discovered patterns remain stable across reasonable methodological choices.
- [ ] Explain which findings are robust and which depend on a particular decision.

### Purpose of this stage

We need to show that the discovered roles are not only the result of one random initialization or one arbitrary preprocessing choice.

If an alternative setup produces a different result, we should not hide it. We should explain what changed, why it changed, and which solution better answers the research question.

---

## 11. Analyze and Interpret the Discovered Clusters

- [ ] Calculate the average original-unit feature values for every cluster.
- [ ] Calculate standardized cluster profiles.
- [ ] Create visual comparisons of the cluster profiles.
- [ ] Identify the features that most strongly distinguish every cluster.
- [ ] Examine representative players from every cluster.
- [ ] Examine players closest to each cluster center or with the highest GMM membership probability.
- [ ] Examine unusual members and boundary cases.
- [ ] Determine the main basketball behavior represented by each cluster.
- [ ] Assign a meaningful basketball role name to every interpretable cluster.
- [ ] Support every role name using the numerical profile and representative players.
- [ ] Explain how each discovered role differs from the other roles.
- [ ] Reconsider the feature set, model, or number of clusters if a group cannot be interpreted coherently.

### Result expected from this stage

The output should no longer be a list of numbered clusters. Each cluster should become an understandable basketball role supported by statistics and player examples, such as a creator, interior finisher, perimeter scorer, rebound-focused big, or another role that is genuinely supported by the results.

We should not choose the role names in advance. The names must follow from the final cluster profiles.

---

## 12. Compare the Discovered Roles with Traditional Positions

- [ ] Use traditional position labels only after the clustering is complete.
- [ ] Create a comparison between cluster membership and traditional positions.
- [ ] Show the position distribution inside every discovered role.
- [ ] Examine whether some roles contain players from several traditional positions.
- [ ] Identify players whose discovered role provides more specific information than their listed position.
- [ ] Examine whether players listed at the same traditional position are divided into different playing roles.
- [ ] Handle players with missing position labels transparently.
- [ ] Explain whether the discovered roles add useful information beyond traditional position labels.

### Main research interpretation

This comparison should help answer the central research question: whether unsupervised learning can identify meaningful player roles that describe modern EuroLeague players better than broad traditional position categories.

The goal is not to predict the traditional labels. The goal is to determine whether the discovered roles reveal distinctions that the traditional labels do not show.

---

## 13. Examine Player and Season Examples

- [ ] Examine players who appear in several seasons.
- [ ] Determine whether the model captures plausible changes in their playing roles over time.
- [ ] Examine players who changed teams during a season.
- [ ] Determine whether their player-season-team observations reflect different team roles when appropriate.
- [ ] Use selected examples to make the cluster interpretation more concrete.
- [ ] Avoid using a small number of convenient examples as proof for the entire model.

### Purpose of this stage

Examples of real players can make the discovered roles understandable, but they must support the numerical analysis rather than replace it.

---

## 14. Answer the Research Question

- [ ] Summarize the final discovered roles.
- [ ] Explain why the selected model and cluster count were chosen.
- [ ] Explain whether the roles are statistically stable.
- [ ] Explain whether the roles are meaningful from a basketball perspective.
- [ ] Explain how they compare with traditional positions.
- [ ] State whether the project supports the idea that modern EuroLeague players can be described using more detailed roles.
- [ ] Separate strong conclusions from tentative interpretations.
- [ ] Discuss the main limitations of the data and methodology.

### Limitations to consider

- The participation threshold used to define the modeling sample.
- Missing biography information.
- Players without enough valid shot-location data.
- Differences in event recording across seasons.
- The uncertain physical scale of the coordinate system.
- The selected feature set.
- The assumptions of K-Means and GMM.
- The use of player-season-team observations, which allows the same player to appear more than once.
- The possibility that historical changes in EuroLeague playing style influence some clusters.

---

## 15. Complete the Final Notebook Story

- [ ] Read the complete notebook from beginning to end as one continuous investigation.
- [ ] Make sure every section follows naturally from the previous result.
- [ ] Explain each important method before its implementation.
- [ ] Explain each important result after it appears.
- [ ] State the decision that followed from each important result.
- [ ] Include alternative approaches when they affected the final decision.
- [ ] Preserve unsuccessful experiments when they genuinely explain why we changed direction.
- [ ] Remove redundant tests that do not affect a decision or conclusion.
- [ ] Keep the writing in first-person plural as Doron and Yuval explaining their own project.
- [ ] Make sure every numerical claim is supported by visible notebook output.
- [ ] Keep all notebook text, code, comments, chart labels, and tables in English.
- [ ] End with the project conclusions and limitations.
- [ ] Render the completed notebook as HTML.
- [ ] Inspect the final HTML from beginning to end.

---

## 16. Prepare the Hebrew Presentation

- [ ] Build the presentation only after the notebook results are final.
- [ ] Present the research question and motivation.
- [ ] Explain the datasets and the information they provide.
- [ ] Summarize the important data-quality and preparation decisions.
- [ ] Explain how the final modeling sample and features were selected.
- [ ] Explain PCA and what its visualization shows.
- [ ] Explain the comparison between K-Means and GMM.
- [ ] Show how BIC was used to select the GMM cluster count.
- [ ] Present the final discovered player roles.
- [ ] Use representative player examples.
- [ ] Compare the discovered roles with traditional positions.
- [ ] Explain at least one important case where a result did not match our expectation and caused us to change the method or decision.
- [ ] Present the main conclusions and limitations.
- [ ] Select only figures and tables that contribute to the presentation story.
- [ ] Divide the presentation clearly between Doron and Yuval.
- [ ] Rehearse a complete presentation of approximately 40 minutes.
- [ ] Make sure both presenters can explain every important methodological decision.
- [ ] Record the final presentation if required.

---

## Final Project Acceptance Check

- [ ] The notebook presents one continuous data-science investigation.
- [ ] The reasoning behind every major methodological decision is explained.
- [ ] The expanded feature set includes scoring, shooting, playmaking, rebounding, and defensive behavior.
- [ ] Traditional position is never used as a clustering input.
- [ ] PCA provides a clear two-dimensional visualization of the players and clusters.
- [ ] K-Means provides a useful baseline for comparison.
- [ ] GMM and BIC are used as proposed to evaluate the number of clusters.
- [ ] The final cluster count is supported by the complete analysis rather than assumed from the preliminary result.
- [ ] Every final cluster has a statistically supported and understandable basketball interpretation.
- [ ] Representative players support the interpretation of each role.
- [ ] The comparison with traditional positions answers the research question.
- [ ] Unexpected or unsuccessful results are reported honestly and used to explain changes in the analysis.
- [ ] The final conclusions are supported by visible code outputs, tables, and figures.
- [ ] The final English notebook is rendered correctly as HTML.
- [ ] The Hebrew presentation accurately represents the results of the notebook.