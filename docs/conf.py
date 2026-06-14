# Configuration file for the Sphinx documentation builder.
#
# Unified documentation for POPS-UQ: misspecification-aware Bayesian
# regression, with the Python and Julia implementations documented
# side by side.
#
# Full option list: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "POPS-UQ"
copyright = "2025, POPS-UQ contributors"
author = "POPS-UQ contributors"
release = "0.1"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
]

# MyST (Markdown) features used across the docs.
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "colon_fence",
    "deflist",
    "fieldlist",
    "substitution",
    "linkify",
]
myst_heading_anchors = 3

source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_title = "POPS-UQ"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "_static/logo.svg"
html_favicon = "_static/logo.svg"

# Brand accent: POPS deep indigo, consistent in light and dark mode.
_brand = {
    "color-brand-primary": "#4338ca",
    "color-brand-content": "#4338ca",
}

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "light_css_variables": dict(_brand),
    "dark_css_variables": {
        "color-brand-primary": "#a5b4fc",
        "color-brand-content": "#a5b4fc",
    },
    "source_repository": "https://github.com/POPS-UQ/.github/",
    "source_branch": "main",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/POPS-UQ",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0"
                     viewBox="0 0 16 16" width="1em" height="1em">
                  <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53
                  5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94
                  -.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58
                  1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89
                  -3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21
                  2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82
                  2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87
                  3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0
                  .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

html_domain_indices = False
html_use_index = True
html_copy_source = False
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

# Strip prompt characters when copying code blocks.
copybutton_prompt_text = r">>> |\.\.\. |\$ |julia> |In \[\d*\]: "
copybutton_prompt_is_regexp = True
