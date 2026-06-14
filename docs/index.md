---
sd_hide_title: true
---

<div class="pops-hero">

# POPS-UQ

<p class="tagline">
Misspecification-aware Bayesian regression for low-noise data —
honest uncertainties even when your model class cannot fit the truth.
</p>

<p class="badges">
<a class="reference external" href="https://doi.org/10.1088/2632-2153/ad9fce">📄 Paper (MLST 2025)</a>
<a class="reference external" href="https://kermodegroup.github.io/demos/regression-demo.html">▶ Live demo</a>
<a class="reference external" href="https://github.com/POPS-UQ">★ GitHub</a>
</p>

</div>

**POPS** (Pointwise Optimal Parameter Sets) is an algorithm for estimating
**model misspecification uncertainty** in regression. Standard Bayesian
regression captures epistemic and aleatoric uncertainty but
[provably ignores misspecification](theory.md) — the error that remains because
a finite model class cannot represent the target function exactly. In the
low-noise, near-deterministic regime that dominates scientific surrogate
modelling (interatomic potentials, reduced-order models, …), this makes
standard uncertainties collapse to near-zero as data grows, even where the
model is badly wrong.

POPS instead finds, for each training point, the parameter perturbation that
would fit that point exactly. The resulting **Pointwise Optimal Parameter
Set** defines a posterior that yields wider, better-calibrated predictive
bounds that properly cover the true function.

This site documents the **Python** and **Julia** implementations side by side.

## Two implementations, one method

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🐍 Python — `popsregression`
A [scikit-learn](https://scikit-learn.org)-compatible estimator. Drop
`POPSRegression` into any pipeline or hyperparameter search.

+++
```bash
pip install popsregression
```
:::

:::{grid-item-card} 🟣 Julia — `POPSRegression.jl`
A [StatsAPI.jl](https://github.com/JuliaStats/StatsAPI.jl)-compliant
implementation built for performance on large linear models.

+++
```julia
Pkg.add(url="https://github.com/POPS-UQ/POPSRegression.jl")
```
:::

::::

## What you get

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card} Misspecification uncertainty
Predictive bounds that stay honest in the low-noise limit, where epistemic
uncertainty vanishes.
:::

:::{grid-item-card} Drop-in API
`fit` / `predict` with mean, standard deviation, and min–max bounds —
familiar in both ecosystems.
:::

:::{grid-item-card} Built for surrogates
Leverage-based filtering and hypercube sampling scale to large linear models
such as interatomic potentials.
:::

::::

## Quick start

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
from popsregression import POPSRegression

# X_train, y_train, X_test from your problem
model = POPSRegression()          # fit_intercept=False by default
model.fit(X_train, y_train)

# Mean prediction with combined misspecification + epistemic std
y_pred, y_std = model.predict(X_test, return_std=True)

# Also recover the min/max bounds over the POPS posterior
y_pred, y_std, y_max, y_min = model.predict(
    X_test, return_std=True, return_bounds=True
)
```
:::

:::{tab-item} Julia
:sync: julia

```julia
using POPSRegression, Random

rng = Xoshiro(0)
N, P, D = 200, 5, 2
X = randn(rng, N, P)
W_true = randn(rng, P, D)
Y = X * W_true .+ 0.01 .* randn(rng, N, D)

model = fit(POPSModel, X, Y; prior_covariance=1e-3, leverage_percentile=0.5)

X_test = randn(rng, 10, P)
pred = predict(model, X_test; return_bounds=true, return_std=true, level=0.95)

pred.mean   # mean predictions
pred.lower  # lower quantile
pred.upper  # upper quantile
pred.std    # empirical std
```
:::

::::

New here? Start with [Installation](installation.md), then the
[Quick start](quickstart.md). To understand *why* POPS works, read the
[background on misspecification-aware regression](theory.md). For worked
problems across domains, see the [Examples](examples/index.md).

## Citation

> T. D. Swinburne and D. Perez, *Parameter uncertainties for imperfect
> surrogate models in the low-noise regime*,
> [Machine Learning: Science and Technology (2025)](https://doi.org/10.1088/2632-2153/ad9fce).

```{toctree}
:hidden:
:caption: Getting started

installation
quickstart
```

```{toctree}
:hidden:
:caption: Background

theory
```

```{toctree}
:hidden:
:caption: Examples

examples/index
examples/python-simple
examples/julia-ace
examples/julia-md
```

```{toctree}
:hidden:
:caption: Reference

api/index
```
