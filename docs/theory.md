# Misspecification-aware Bayesian regression

This page explains the problem POPS solves and what the algorithm actually
computes. It applies equally to the
[Python and Julia implementations](installation.md).

## The problem: uncertainty that vanishes when it shouldn't

Standard Bayesian linear regression (for example scikit-learn's
`BayesianRidge`) estimates two kinds of uncertainty:

- **Epistemic** uncertainty — encoded in the weight covariance `sigma_`. It
  reflects how little data we have and **decays towards zero as the dataset
  grows**.
- **Aleatoric** uncertainty — encoded in the noise precision `alpha_`. It
  reflects irreducible observation noise.

What this picture leaves out is **model misspecification**: the error that
arises because a finite model class cannot represent the target function
exactly. In the low-noise (weak-aleatoric, near-deterministic) limit, this is
the dominant source of error — and it is precisely the regime that standard
Bayesian regression handles worst:

- the weight uncertainty `sigma_` only captures epistemic uncertainty, so it is
  driven to near-zero by abundant data, **underestimating** the true
  uncertainty wherever the model is structurally wrong;
- any residual error is instead attributed to aleatoric noise `alpha_`, which
  is simply incorrect in a near-deterministic setting.

The result is a model that becomes *more* confident as you add data, even in
regions where it can never fit the truth.

```{admonition} Where this bites hardest
:class: tip

Surrogate models in computational science — interatomic potentials,
reduced-order models, learned closures — are misspecified **by construction**:
the optimal surrogate in the chosen model class is structurally unable to match
the target function exactly, and the underlying simulations are
near-deterministic. This is exactly the regime POPS was designed for.
```

## The idea: Pointwise Optimal Parameter Sets

POPS estimates **model misspecification uncertainty** directly. For each
training point it asks a simple question:

> What is the smallest parameter perturbation that would make the model fit
> *this* point exactly?

Each such perturbation defines a **Pointwise Optimal Parameter Set** — a
parameter vector that is optimal with respect to one observation. Collected
over the (high-leverage) training points, these perturbations span a region of
parameter space consistent with the data given the model's limited form.

Concretely, around the ridge/mean solution $\theta_0$ the implementations:

1. compute the **leverage** of each training point and keep the
   highest-leverage subset (`leverage_percentile`) — these constrain the fit
   the most;
2. find, for each retained point, the parameter correction that fits it
   exactly, giving a cloud of POPS corrections;
3. summarize that cloud as a posterior — either a PCA-aligned **hypercube**
   (the default) or the raw **ensemble** of corrections;
4. **sample** the posterior (`uniform` / `sobol` / `latin` / `halton`) to
   propagate parameter uncertainty to predictions.

## What you get out

For a test input, sampling the POPS posterior yields a distribution of
predictions whose spread reflects misspecification, not just data scarcity.
Both packages expose this as:

- a **mean** prediction (the ridge/posterior-mean fit);
- a **standard deviation** combining misspecification and epistemic
  contributions (the Python API can also return the epistemic-only part);
- **min–max bounds** — the envelope of predictions over the posterior, which
  empirically provide honest coverage of the true function.

Because the spread is anchored to where the model *can't* fit the data, the
bounds stay wide in misspecified regions even as the dataset grows — exactly
the behaviour standard Bayesian regression lacks.

## Propagating uncertainty downstream

The POPS posterior is a set of parameter samples, so any quantity computed from
the model can inherit its uncertainty. The
[molecular dynamics example](examples/julia-md.md) shows this in practice:
parameter samples are propagated to a thermodynamic observable (the radial
distribution function) by **Boltzmann reweighting** a single trajectory,
turning a posterior over potentials into an uncertainty band on a physical
property — without re-running the simulation for every sample.

## Reference

> T. D. Swinburne and D. Perez, *Parameter uncertainties for imperfect
> surrogate models in the low-noise regime*,
> [Machine Learning: Science and Technology (2025)](https://doi.org/10.1088/2632-2153/ad9fce).

```bibtex
@article{swinburne2025,
    author  = {Swinburne, Thomas and Perez, Danny},
    title   = {Parameter uncertainties for imperfect surrogate models in the low-noise regime},
    journal = {Machine Learning: Science and Technology},
    doi     = {10.1088/2632-2153/ad9fce},
    year    = {2025}
}
```
