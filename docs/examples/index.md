# Examples

Worked problems using POPS. Examples may be written in **Python** or **Julia** —
the method is the same, and each page is tagged with the language it uses. More
examples across diverse domains (and potentially more languages) will be added
over time.

<div class="grid cards" markdown>

-   **Simple regression** · :material-language-python: Python

    ---

    Fit a quartic polynomial to an oscillatory target and watch POPS keep honest
    uncertainty where `BayesianRidge` collapses. The canonical "what does
    misspecification look like?" example.

    [:octicons-arrow-right-24: Read](python-simple.md)

-   **ACE interatomic potential** · :simple-julia: Julia

    ---

    Attach predictive uncertainties to energies, forces and virials of a linear
    Atomic Cluster Expansion potential on a silicon dataset.

    [:octicons-arrow-right-24: Read](julia-ace.md)

-   **Uncertainty in molecular dynamics** · :simple-julia: Julia

    ---

    Propagate POPS parameter uncertainty to a thermodynamic observable — the
    radial distribution function — by Boltzmann-reweighting a single MD
    trajectory.

    [:octicons-arrow-right-24: Read](julia-md.md)

</div>

!!! note "Contributing an example"

    Have a POPS use case in another domain or language? Examples are plain
    Markdown pages in `docs/examples/`. Add a page, tag it with the language,
    link it from this grid, and add it to the `nav` in `mkdocs.yml`.
