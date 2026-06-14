# Installation

POPS has two reference implementations that share the same method but follow
the conventions of their host ecosystem. Install whichever matches your stack —
the [Quick start](quickstart.md) shows equivalent code for both.

## Python — `popsregression`

The Python package is [scikit-learn](https://scikit-learn.org) compatible and
published on PyPI.

```bash
pip install popsregression
```

**Dependencies:** scikit-learn ≥ 1.6.1, scipy ≥ 1.6.0, numpy ≥ 1.20.0.

For a development checkout:

```bash
git clone https://github.com/POPS-UQ/popsregression
cd popsregression
pip install -e .
pytest -vsl popsregression      # run the test suite
```

## Julia — `POPSRegression.jl`

The Julia package follows the [StatsAPI.jl](https://github.com/JuliaStats/StatsAPI.jl)
interface. Until it is registered in the General registry, install it directly
from GitHub:

```julia
using Pkg
Pkg.add(url="https://github.com/POPS-UQ/POPSRegression.jl")
```

To run the test suite, from the package root launch `julia --project=.` and in
the REPL:

```julia
]
test
```

### Example environments

The Julia [examples](examples/index.md) (ACE, molecular dynamics) each ship
their own project environment under `examples/`. Instantiate one before running
its script — for the molecular dynamics example:

```bash
julia --project=examples/md -e "using Pkg; Pkg.instantiate()"
julia --project=examples/md -t $(nproc) examples/md/pops_rdf.jl
```

The same pattern applies to `examples/ace/`.

## Which one should I use?

```{list-table}
:header-rows: 1
:widths: 25 75

* - If you…
  - Reach for
* - work in a scikit-learn / NumPy workflow, or want pipelines and grid search
  - **Python** (`popsregression`)
* - fit large linear models (e.g. ACE interatomic potentials) and want raw speed
  - **Julia** (`POPSRegression.jl`)
* - are exploring the method interactively or teaching it
  - either — try the [live demo](https://kermodegroup.github.io/demos/regression-demo.html)
```

Both implementations are validated against each other: the Julia test suite
includes cross-checks against the scikit-learn results.
