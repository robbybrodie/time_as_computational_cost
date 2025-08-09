# Validation Plan

## Pre‑registered Hypotheses and Protocols

- All hypotheses, metrics, data splits, and seeds will be frozen before evaluation.
- No tuning or model selection after seeing held‑out results.

## Datasets and Benchmarks

- Selected GR benchmarks (Schwarzschild, PPN parameters, light deflection, Shapiro delay, perihelion precession, GW dispersion).
- Public datasets and scenario families.

## Train/Validation Splits

- k‑fold cross‑validation and/or held‑out scenario families.
- Splits and seeds pre‑registered and documented.

## Metrics

- MSE, MAE, RMSE, R² for fit quality.
- AIC/BIC with explicit parameter counts.
- Bootstrap confidence intervals for uncertainty.
- Cross‑validation protocol.

## Acceptance Criteria and Stopping Rules

- Pre‑specified thresholds for fit quality and model selection.
- No further tuning after evaluation begins.

## Hyperparameter Freeze Policy

- All hyperparameters and model choices frozen prior to evaluation.
- Any changes require new pre‑registration and justification.
