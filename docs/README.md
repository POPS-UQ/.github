# POPS-UQ documentation

Source for the unified POPS-UQ documentation site, built with
[Sphinx](https://www.sphinx-doc.org) and the
[Furo](https://pradyunsg.me/furo/) theme. It documents the **Python**
(`popsregression`) and **Julia** (`POPSRegression.jl`) implementations side by
side.

This site is intended to grow into the org landing page at
<https://pops-uq.github.io/>, eventually subsuming the per-package docs sites.

## Build locally

```bash
pip install -r requirements.txt
sphinx-build -b html . _build/html
# then open _build/html/index.html
```

Or, with the Makefile:

```bash
make html
```

## Layout

```
docs/
├── conf.py            # Sphinx configuration (theme, extensions, branding)
├── requirements.txt   # build dependencies
├── index.md           # landing page
├── installation.md    # Python + Julia install
├── quickstart.md      # side-by-side fit/predict
├── theory.md          # misspecification-aware regression background
├── examples/          # worked examples (Python or Julia, tagged per page)
├── api/               # API reference for both implementations
└── _static/           # logo + custom CSS
```

## Adding an example

Create a Markdown page in `examples/`, tag it with a language pill
(`<span class="lang-pill python">Python</span>` or `...julia">Julia</span>`),
then link it from `examples/index.md` and add it to the `toctree` in
`index.md`.
