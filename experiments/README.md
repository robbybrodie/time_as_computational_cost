# Time as Computational Cost - Experiments

This directory contains computational experiments to test the theoretical framework described in the paper "Capacity-Limited Unification of SR and GR".

## Overview

The experiments explore how degrees of freedom (DoF) in a vibrating network substrate change with motion and curvature, testing 8 different mechanisms proposed to derive the constitutive relation B(N) from first principles.

## Experiment Structure

### Core Framework
- `framework/` - Base classes and utilities for substrate simulation
- `mechanisms/` - Implementation of the 8 DoF mechanisms
- `validation/` - Tests against known SR/GR results

### Mechanisms Tested

1. **Causal Diamond Throttling** - Finite horizon reduces accessible modes
2. **Tension-Induced Bandgaps** - Load creates frequency gaps that freeze modes
3. **Mode Crowding via Redshift** - Frequencies slide out of resolvable window
4. **Entanglement Compression** - Correlations make modes redundant
5. **Connectivity Pruning** - Graph sparsification under load
6. **Unruh/Thermalization Windowing** - Effective temperature reduces coherent DoF
7. **Boundary-Condition Locking** - Changed BCs eliminate eigenmodes
8. **Spectral-Dimension Flow** - Effective dimension drops with load

### Google Colab Integration

Each experiment is designed to run in Google Colab with:
- Minimal dependencies (numpy, matplotlib, scipy)
- Clear visualization of results
- Interactive parameter exploration
- Comparison with GR predictions

## Key Questions to Answer

1. Which mechanism(s) naturally produce the observed B(N) behavior?
2. Can we derive time dilation without curve-fitting to GR?
3. What are the falsifiable predictions that differ from GR?
4. How do thermodynamic and string theory interpretations connect?

## Usage

1. Upload notebooks to Google Colab
2. Run the framework setup cells
3. Choose a mechanism to test
4. Compare results with theoretical predictions
5. Explore parameter space for novel predictions

## Reproducibility and Evaluation Outputs

- **Random Seeds & Data Splits:**  
  All experiments use fixed random seeds and deterministic data splits to ensure reproducibility. Seeds and splits are logged with each run.

- **Evaluation Metrics:**  
  Once implemented, evaluation metrics (e.g., MSE, AIC/BIC, cross-validation results) will be automatically written to disk in both human-readable and machine-readable (CSV/JSON) formats. Output files will be located in the experiment's results directory, with filenames including the seed and configuration hash for traceability.

- **Best Practices:**  
  For new experiments or baselines, ensure that all scripts log the random seed, data split, and output metric file location.
