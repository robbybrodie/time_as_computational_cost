# Contributing Guide

Thank you for your interest in contributing to this project! This document outlines how to reproduce results, add new baselines, run evaluation scripts, file issues, propose adversarial tests, and the expected tone and scope for contributions.

---

## 1. How to Reproduce Results

- **Environment Setup:**  
  Ensure you have all dependencies installed. See `README.md` for environment setup instructions.
- **Data Preparation:**  
  Download and preprocess datasets as described in `experiments/README.md`.
- **Running Experiments:**  
  Use the provided scripts in the `experiments/` directory. All experiments are parameterized and can be run with fixed random seeds for reproducibility.
- **Reproducibility:**  
  All random seeds, data splits, and configuration files are logged and version-controlled. Output artifacts include logs for all relevant parameters.

---

## 2. How to Add Baselines

- **New Baseline Integration:**  
  - Add new baseline code in the appropriate subdirectory under `experiments/`.
  - Register the baseline in the experiment orchestration script.
  - Document the baseline’s configuration and any hyperparameters in `experiments/README.md`.
- **Testing:**  
  Ensure the baseline runs end-to-end and produces output in the standard format.
- **Evaluation:**  
  Run the evaluation scripts to generate metrics for the new baseline.

---

## 3. How to Run Evaluation Scripts

- **Location:**  
  Evaluation scripts are located in the project root and `experiments/` directories.
- **Usage:**  
  Scripts accept command-line arguments for input/output paths, model selection, and evaluation options.
- **Output:**  
  Metrics are written to disk in both human-readable and machine-readable (CSV/JSON) formats.
- **Reproducibility:**  
  All scripts log random seeds and configuration parameters.

---

## 4. How to File Issues and Propose Adversarial Tests

- **Filing Issues:**  
  - Use the GitHub Issues tab to report bugs, request features, or ask questions.
  - Include as much detail as possible: steps to reproduce, error messages, and environment information.
- **Proposing Adversarial Tests:**  
  - Clearly describe the adversarial scenario and its motivation.
  - Provide code snippets or data samples if possible.
  - Suggest expected outcomes and how the test challenges the current approach.

---

## 5. Tone and Scope Guidance

- **Tone:**  
  - Be constructive, humble, and precise.
  - Avoid triumphalist or overstated claims; focus on empirical evidence and limitations.
  - Cite relevant literature and prior work where appropriate.
- **Scope:**  
  - Contributions should be relevant to the project’s goals and scientific scope.
  - Proposals for major changes should be discussed in an issue before submitting a pull request.

---

For further questions or to discuss potential contributions, please open an issue or join the project discussion board.
