# Example: simple misspecified regression

<span class="lang-pill python">Python</span>

The clearest way to see what POPS does is to fit a model that *cannot* represent
the truth, and watch what happens to its uncertainty as data grows. Here we fit
a **quartic polynomial** (5 parameters) to a complex oscillatory function, using
increasingly many training points, and compare scikit-learn's `BayesianRidge`
with `POPSRegression`.

A runnable notebook version,
[`SimpleExample.ipynb`](https://github.com/POPS-UQ/popsregression/blob/main/SimpleExample.ipynb),
ships with the Python package.

## Setting up the problem

```python
import numpy as np
from sklearn.linear_model import BayesianRidge
from sklearn.preprocessing import PolynomialFeatures
from popsregression import POPSRegression

rng = np.random.default_rng(0)

# A target the quartic polynomial cannot fit exactly (misspecification).
def truth(x):
    return np.sin(3 * x) + 0.3 * np.cos(9 * x) + 0.5 * x

# Near-deterministic observations: tiny aleatoric noise.
NOISE = 1e-2

def make_data(n):
    x = np.sort(rng.uniform(-1.0, 1.0, size=n))
    y = truth(x) + NOISE * rng.standard_normal(n)
    return x, y

# Degree-4 polynomial design: P = 5 parameters.
poly = PolynomialFeatures(degree=4)
x_grid = np.linspace(-1.0, 1.0, 400)
X_grid = poly.fit_transform(x_grid[:, None])
```

## Fitting both models

```python
def fit_both(n):
    x, y = make_data(n)
    X = poly.transform(x[:, None])

    br = BayesianRidge().fit(X, y)
    br_mean, br_std = br.predict(X_grid, return_std=True)

    pops = POPSRegression(resampling_method="sobol").fit(X, y)
    pops_mean, pops_std, pops_hi, pops_lo = pops.predict(
        X_grid, return_std=True, return_bounds=True
    )
    return (x, y), (br_mean, br_std), (pops_mean, pops_std, pops_lo, pops_hi)

results = {n: fit_both(n) for n in (10, 50, 500)}
```

## What to look for

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(12, 6), sharex=True, sharey=True)
for col, n in enumerate((10, 50, 500)):
    (x, y), (br_mean, br_std), (p_mean, p_std, p_lo, p_hi) = results[n]

    # Top row: BayesianRidge — epistemic band shrinks as n grows.
    ax = axes[0, col]
    ax.plot(x_grid, truth(x_grid), "k--", lw=1, label="truth")
    ax.fill_between(x_grid, br_mean - 2 * br_std, br_mean + 2 * br_std,
                    alpha=0.3, color="tab:orange")
    ax.plot(x_grid, br_mean, color="tab:orange")
    ax.scatter(x, y, s=8, color="k", zorder=3)
    ax.set_title(f"BayesianRidge, N={n}")

    # Bottom row: POPS — bounds stay wide where the quartic is wrong.
    ax = axes[1, col]
    ax.plot(x_grid, truth(x_grid), "k--", lw=1)
    ax.fill_between(x_grid, p_lo, p_hi, alpha=0.3, color="tab:blue")
    ax.plot(x_grid, p_mean, color="tab:blue")
    ax.scatter(x, y, s=8, color="k", zorder=3)
    ax.set_title(f"POPS, N={n}")

fig.tight_layout()
fig.savefig("simple_example.png", dpi=150)
```

**The point of the figure**

- **Top row (`BayesianRidge`).** With `N = 10` the epistemic band is wide, but
  by `N = 500` it has collapsed almost to the mean line — including in regions
  where the quartic clearly misses the oscillatory truth. The model is now
  *confidently wrong*.
- **Bottom row (POPS).** The mean fit is the same ridge solution, but the
  min–max bounds remain wide exactly where the polynomial deviates from the
  truth, and do **not** collapse as `N` grows. This is the misspecification
  uncertainty that `BayesianRidge` cannot see.

## Recovering the uncertainty components

`predict` can also separate the epistemic-only contribution, which is useful for
diagnosing how much of the spread is data scarcity versus misspecification:

```python
pops = POPSRegression().fit(poly.transform(make_data(500)[0][:, None]),
                            make_data(500)[1])
y_pred, y_std, y_hi, y_lo, y_epi = pops.predict(
    X_grid, return_std=True, return_bounds=True, return_epistemic_std=True
)
# y_epi << y_std in misspecified regions: the extra width is misspecification.
```

See the [Quick start](../quickstart.md) for the full set of parameters and the
[background](../theory.md) for why this works.
