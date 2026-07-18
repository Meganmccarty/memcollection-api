# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path
import django

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DJANGO_SETTINGS_MODULE"] = "memcollection.settings.dev"
django.setup()

project = "MEM Collection API"
copyright = "2026, Megan McCarty"
author = "Megan McCarty"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_wagtail_theme",
]

templates_path = ["_templates"]
exclude_patterns = []

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

footer_links = ",".join(
    [
        "Main Site|https://www.memcollection.com/",
        "Admin|https://api.memcollection.com/admin/",
        "GitHub|https://github.com/Meganmccarty/memcollection-api/",
    ]
)

html_theme = "sphinx_wagtail_theme"
html_theme_options = {
    "project_name": "MEM Collection API",
    "logo": "img/logo.svg",
    "github_url": "https://github.com/Meganmccarty/memcollection-api/",
    "footer_links": footer_links,
}
html_last_updated_fmt = "%b %d, %Y."
html_static_path = ["_static"]
