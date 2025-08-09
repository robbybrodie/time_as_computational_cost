# Time as Computational Cost — Exploratory Computational Models

## Status

- This repository contains exploratory computational models and curve‑fitting experiments against selected General Relativity (GR) benchmarks.
- Results are preliminary fits with multiple free parameters; they do not demonstrate a derivation of GR or physical discovery.
- Nothing here is peer‑reviewed or independently validated. All claims are tentative and subject to falsification by forthcoming, pre‑registered validation.

## Current exploratory results (curve‑fitting)

- We evaluated several simple mechanisms within a discrete substrate and fitted parameters to approximate aspects of Schwarzschild benchmarks.

- Example fit quality on selected targets (MSE; subject to overfitting):

  - Tension bandgaps (exponential scaling): ~2.918
  - Causal diamond (exponential scaling): ~5.570
  - Mode crowding (exponential scaling): ~7.432 (normalization pending)

- These are in‑framework fits, not out‑of‑sample predictions. Baselines and model‑selection penalties will be added (AIC/BIC, cross‑validation).

## Repository contents

- Theory manuscripts: time_as_computational_cost.tex / .md
- Experimental framework: experiments/framework and experiments/mechanisms
- Notebooks: experiments/notebooks
- Results and analysis: PRELIMINARY_RESULTS.md, experimental_results_analysis.md
- Roadmap: research_roadmap.md

## Limitations (see LIMITATIONS.md for details)

- Curve‑fitting risk; parameter flexibility; limited scenario diversity.
- Dependence on discretization/connectivity; lack of independent validation.
- Single‑metric focus to date; no baselines or model complexity penalties reported.

## Validation plan (summary; see VALIDATION_PLAN.md)

- Add simple baselines (polynomial, exponential, power‑law, logistic, Yukawa) and report AIC/BIC with parameter counts.
- Use k‑fold CV / held‑out scenario families; pre‑register hypotheses and splits.
- Run ablations, sensitivity analyses, and robustness to discretization/connectivity.
- Attempt mapping to effective metric components and estimate PPN parameters with uncertainties; compare to GR.

## Reproducibility

- See colab_links.md for Colab; local: pip install -r experiments/requirements.txt then run experiments per docs.
- Deterministic seeds and environment details will be documented as part of the evaluation pipeline.

## How to critique or contribute

- See CONTRIBUTING.md for baselines, evaluation, and critique guidance. Adversarial tests are welcome.

## License

- CC BY‑NC 4.0
