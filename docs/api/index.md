# API reference

POPS is implemented in two packages. This page summarizes the public surface of
each and links to the authoritative, auto-generated reference for full detail.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🐍 Python — `popsregression`
:link: https://tomswinburne.github.io/popsregression

scikit-learn-style API reference →
:::

:::{grid-item-card} 🟣 Julia — `POPSRegression.jl`
:link: https://pops-uq.github.io/POPSRegression.jl/

Documenter API reference →
:::

::::

## Python: `POPSRegression`

A scikit-learn estimator. Construct, `fit(X, y)`, then `predict(X, ...)`.

### Constructor parameters

```{list-table}
:header-rows: 1
:widths: 28 18 54

* - Parameter
  - Default
  - Description
* - `posterior`
  - `'hypercube'`
  - Posterior form: `'hypercube'` (PCA-aligned box) or `'ensemble'` (raw corrections)
* - `resampling_method`
  - `'uniform'`
  - Sampler: `'uniform'`, `'sobol'`, `'latin'`, `'halton'`
* - `resample_density`
  - `1.0`
  - Number of posterior samples per training point
* - `leverage_percentile`
  - `50.0`
  - Only use high-leverage training points for the POPS posterior
* - `mode_threshold`
  - `1e-8`
  - Eigenvalue threshold for hypercube dimensionality
* - `percentile_clipping`
  - `0.0`
  - Percentile to clip from hypercube bounds (0–50)
```

All `BayesianRidge` parameters (`max_iter`, `tol`, `alpha_1`, `alpha_2`,
`lambda_1`, `lambda_2`, `fit_intercept`, …) are also accepted.

### `predict` options

`predict(X, return_std=False, return_bounds=False, return_epistemic_std=False)`
returns the mean, optionally followed by, in order: the combined std, the
min/max bounds (`y_max, y_min`), and the epistemic-only std.

### Fitted attributes

```{list-table}
:header-rows: 1
:widths: 32 68

* - Attribute
  - Description
* - `coef_`
  - Regression coefficients (posterior mean)
* - `sigma_`
  - Epistemic variance–covariance matrix
* - `misspecification_sigma_`
  - Misspecification variance–covariance matrix from POPS
* - `posterior_samples_`
  - Samples from the POPS posterior
* - `alpha_`
  - Estimated noise precision (not used for prediction)
```

## Julia: `POPSRegression.jl`

Follows the [StatsAPI.jl](https://github.com/JuliaStats/StatsAPI.jl) interface.

### Fitting

```julia
fit(POPSModel, X, Y;
    prior_covariance,        # ridge / prior covariance
    leverage_percentile)     # fraction of (top-leverage) points to keep
```

### Prediction

```julia
predict(model, X_test;
    return_bounds=true,
    return_std=true,
    level=0.95,              # bound level; 1.0 for full min/max
    min_samples=5000,        # minimum posterior samples
    sampling_method=:sobol)  # :uniform / :sobol / :latin / :halton
```

returns a named tuple with fields `mean`, `std`, `lower`, `upper`.

### Sampling the posterior directly

```julia
sample(model, n_samples; sampling_method=:sobol)   # parameter samples
```

Useful for downstream uncertainty propagation — see the
[molecular dynamics example](../examples/julia-md.md).

```{admonition} Side-by-side mapping
:class: note

The two APIs use slightly different names for the same quantities. The
[Quick start](../quickstart.md#key-knobs) has a table mapping Python knobs to
their Julia equivalents.
```
