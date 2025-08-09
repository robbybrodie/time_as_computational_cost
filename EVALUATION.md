# Evaluation Metrics and Methodology

This document defines the evaluation metrics, statistical criteria, and procedures used to assess model performance in this project. It also details the rules for parameter counting, cross-validation setup, and uncertainty estimation.

---

## 1. Metric Definitions

- **Mean Squared Error (MSE):**
  \[
  \mathrm{MSE} = \frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2
  \]
  Where \( y_i \) is the true value and \( \hat{y}_i \) is the predicted value.

- **Mean Absolute Error (MAE):**
  \[
  \mathrm{MAE} = \frac{1}{N} \sum_{i=1}^N |y_i - \hat{y}_i|
  \]

- **Coefficient of Determination (\( R^2 \)):**
  \[
  R^2 = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - \bar{y})^2}
  \]
  Where \( \bar{y} \) is the mean of the observed data.

- **Log-Likelihood (LL):**
  For probabilistic models, the log-likelihood of the observed data under the model.

---

## 2. Model Selection Criteria

### Akaike Information Criterion (AIC)

\[
\mathrm{AIC} = 2k - 2\ln(\hat{L})
\]
- \( k \): Number of free parameters in the model.
- \( \hat{L} \): Maximum value of the likelihood function for the model.

### Bayesian Information Criterion (BIC)

\[
\mathrm{BIC} = k \ln(N) - 2\ln(\hat{L})
\]
- \( N \): Number of data points.

#### Parameter Counting Rules

- Each independently fitted scalar parameter counts as one.
- Hyperparameters selected via cross-validation are not counted as free parameters.
- For regularized models, only non-zero parameters are counted if using L0/L1 sparsity.

---

## 3. Cross-Validation (CV) Setup

- **K-Fold Cross-Validation:** Default is 5-fold unless otherwise specified.
- **Random Seed:** All splits are performed with a fixed random seed for reproducibility.
- **Stratification:** For classification tasks, stratified splits are used.
- **Reporting:** All metrics are reported as mean ± standard deviation across folds.

---

## 4. Uncertainty Estimation

- **Bootstrap Resampling:** For each metric, 1000 bootstrap samples are drawn to estimate confidence intervals.
- **Reporting:** 95% confidence intervals are reported for all primary metrics.
- **Model Uncertainty:** Where applicable, Bayesian posterior predictive intervals are reported.

---

## 5. Reproducibility

- All evaluation scripts are version-controlled and parameterized.
- Random seeds and data splits are logged and included in output artifacts.
- Metric outputs are written to disk in both human-readable and machine-readable (CSV/JSON) formats.

---

For further details or to propose changes to the evaluation methodology, please file an issue or submit a pull request.
