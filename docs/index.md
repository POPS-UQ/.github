# POPS-UQ

**Misspecification-aware uncertainty quantification (the UQ that Bayes ignores).**

**POPS** (Pointwise Optimal Parameter Sets) estimates the predictive
uncertainty that standard Bayesian regression
[provably misses](theory.md) — the error that remains because a finite model
class cannot represent the target function exactly. In the low-noise,
near-deterministic regime typical of scientific surrogate models (interatomic
potentials, reduced-order models, learned closures), this misspecification is
the dominant source of error, yet standard uncertainties collapse to near-zero
as data grows.

POPS finds, for each training point, the parameter perturbation that would fit
that point exactly. The resulting posterior gives wider, better-calibrated
bounds that cover the true function even where the model is structurally wrong.

This site documents the **Python** and **Julia** implementations together.

<div class="grid cards" markdown>

-   :material-language-python: **Python — `popsregression`**

    ---

    A [scikit-learn](https://scikit-learn.org)-compatible estimator. Drop
    `POPSRegression` into any pipeline or hyperparameter search.

    ```bash
    pip install popsregression
    ```

-   :simple-julia: **Julia — `POPSRegression.jl`**

    ---

    A [StatsAPI.jl](https://github.com/JuliaStats/StatsAPI.jl)-compliant
    implementation built for performance on large linear models.

    ```julia
    Pkg.add(url="https://github.com/POPS-UQ/POPSRegression.jl")
    ```

</div>

## Quick start

=== "Python"

    ```python
    from popsregression import POPSRegression

    model = POPSRegression()          # fit_intercept=False by default
    model.fit(X_train, y_train)

    # Combined misspecification + epistemic std
    y_pred, y_std = model.predict(X_test, return_std=True)

    # Add the min/max bounds over the POPS posterior
    y_pred, y_std, y_max, y_min = model.predict(
        X_test, return_std=True, return_bounds=True
    )
    ```

=== "Julia"

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

## Next steps

- [Installation](installation.md) — Python and Julia.
- [Quick start](quickstart.md) — fit and predict, side by side.
- [Background](theory.md) — why misspecification matters and what POPS computes.
- [Examples](examples/index.md) — worked problems in either language.

Try the [live demo](https://kermodegroup.github.io/demos/regression-demo.html)
comparing POPS against other regression schemes, or read the paper:

> T. D. Swinburne and D. Perez, *Parameter uncertainties for imperfect
> surrogate models in the low-noise regime*,
> [Machine Learning: Science and Technology (2025)](https://doi.org/10.1088/2632-2153/ad9fce).
