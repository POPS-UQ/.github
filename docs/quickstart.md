# Quick start

This page walks through a complete fit-and-predict cycle in both
implementations. The two APIs mirror each other deliberately, so you can read
them side by side.

## Fit and predict

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
from popsregression import POPSRegression

# X_train: (n_samples, n_features), y_train: (n_samples,)
model = POPSRegression()          # fit_intercept=False by default
model.fit(X_train, y_train)

# Combined misspecification + epistemic uncertainty
y_pred, y_std = model.predict(X_test, return_std=True)

# Add the min/max bounds over the POPS posterior
y_pred, y_std, y_max, y_min = model.predict(
    X_test, return_std=True, return_bounds=True
)

# Separate out the epistemic-only contribution
y_pred, y_std, y_max, y_min, y_epi = model.predict(
    X_test, return_std=True, return_bounds=True, return_epistemic_std=True
)
```
:::

:::{tab-item} Julia
:sync: julia

```julia
using POPSRegression

# X: (n_samples, n_features), Y: (n_samples, n_targets)
model = fit(POPSModel, X, Y;
    prior_covariance=1e-3,        # ridge / prior covariance
    leverage_percentile=0.5)      # keep the top-leverage points

pred = predict(model, X_test;
    return_bounds=true,
    return_std=true,
    level=0.95)

pred.mean    # mean predictions
pred.std     # empirical posterior std
pred.lower   # lower quantile of the bounds
pred.upper   # upper quantile of the bounds
```
:::

::::

## Use inside a pipeline (Python)

`POPSRegression` is a regular scikit-learn estimator, so it composes with
transformers and model selection:

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

pipe = make_pipeline(
    PolynomialFeatures(degree=4),
    POPSRegression(resampling_method="sobol"),
)
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
```

## Key knobs

These parameters control the POPS posterior. Names differ slightly between the
two packages but map onto the same quantities.

```{list-table}
:header-rows: 1
:widths: 30 30 40

* - Python
  - Julia
  - Meaning
* - `leverage_percentile`
  - `leverage_percentile`
  - Restrict the POPS posterior to high-leverage training points for efficiency
* - (ridge via `lambda_*`)
  - `prior_covariance`
  - Prior covariance / ridge regularization of the mean fit
* - `resampling_method`
  - `sampling_method`
  - Posterior sampler: `uniform` / `sobol` / `latin` / `halton`
* - `posterior`
  - (hypercube model)
  - Posterior form: PCA-aligned `hypercube` or raw `ensemble` corrections
* - `return_std`, `return_bounds`
  - `return_std`, `return_bounds`
  - What `predict` returns alongside the mean
```

For the Python estimator, all `BayesianRidge` parameters (`max_iter`, `tol`,
`alpha_1`, `alpha_2`, `lambda_1`, `lambda_2`, `fit_intercept`, …) are also
accepted. See the [API reference](api/index.md) for the full list and the
fitted attributes (`coef_`, `sigma_`, `misspecification_sigma_`,
`posterior_samples_`, …).

## Next steps

- [Background](theory.md) — why misspecification matters and what POPS computes.
- [Examples](examples/index.md) — worked problems in Python and Julia.
