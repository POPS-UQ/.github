# Examples

Worked problems using POPS. Examples may be written in **Python** or **Julia** —
the method is the same, and each page is tagged with the language it uses. We
will add more examples across diverse domains (and potentially more languages)
over time.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Simple regression
:link: python-simple
:link-type: doc

<span class="lang-pill python">Python</span>

Fit a quartic polynomial to an oscillatory target and watch POPS keep honest
uncertainty where `BayesianRidge` collapses. The canonical "what does
misspecification look like?" example.
:::

:::{grid-item-card} ACE interatomic potential
:link: julia-ace
:link-type: doc

<span class="lang-pill julia">Julia</span>

Attach predictive uncertainties to energies, forces and virials of a linear
Atomic Cluster Expansion potential on a silicon dataset.
:::

:::{grid-item-card} Uncertainty in molecular dynamics
:link: julia-md
:link-type: doc

<span class="lang-pill julia">Julia</span>

Propagate POPS parameter uncertainty to a thermodynamic observable — the radial
distribution function — by Boltzmann-reweighting a single MD trajectory.
:::

::::

```{admonition} Contributing an example
:class: note

Have a POPS use case in another domain or language? Examples are plain
Markdown pages in `docs/examples/`. Add a page, tag it with a language pill,
and link it from this grid and the site navigation.
```
