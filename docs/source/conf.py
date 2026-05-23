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
release = "0.11.1"

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

footer_links = ",".join([
    "Main Site|https://www.memcollection.com/",
    "Admin|https://api.memcollection.com/admin/",
    "GitHub|https://github.com/Meganmccarty/memcollection-api/",
])

# html_theme = "furo"
html_theme = "sphinx_wagtail_theme"
html_theme_options = {
    "project_name": "MEM Collection API",
    "logo": "img/logo-white.png",
    # "light_logo": "img/logo-black.png",
    # "dark_logo": "img/logo-white.png",
    # "footer_icons": [
    #     {
    #         "name": "GitHub",
    #         "url": "https://github.com/Meganmccarty/memcollection-api",
    #         "html": """
    #             <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
    #                 <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 \
    #                     7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.\
    #                     09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 \
    #                     1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 \
    #                     0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 \
    #                     1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 \
    #                     1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.\
    #                     54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 \
    #                     8c0-4.42-3.58-8-8-8z"></path>
    #             </svg>
    #         """,
    #         "class": "",
    #     },
    # ],
    # "source_repository": "https://github.com/Meganmccarty/memcollection-api/",
    "github_url": "https://github.com/Meganmccarty/memcollection-api/",
    "footer_links": footer_links,

    # "source_branch": "main",
    # "source_directory": "docs/",
}
html_last_updated_fmt = "%b %d, %Y."
html_static_path = ["_static"]
