# Task Queue (Tier 1)

## Next task
- [ ] Run app and tests in a clean Python 3.10+ environment; fix integration issues.

## Data and model
- [ ] Select pilot geography and document dataset source/license.
- [ ] Validate coordinates, timestamps, duplicates, and missingness.
- [ ] Construct road-segment/time-window observations including non-accident exposure.
- [ ] Prevent target leakage; use time and geographic holdouts.
- [ ] Compare logistic regression, random forest, and gradient boosting.
- [ ] Report PR-AUC/ROC-AUC, recall, calibration, and prevalence honestly.
- [ ] Connect model only when deployment features match training features.

## Product
- [ ] Render historical hotspots on map.
- [ ] Show provider status and freshness in UI.
- [ ] Add integration/accessibility tests and CI.
- [ ] Add deployment guide.
