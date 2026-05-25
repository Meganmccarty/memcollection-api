.. MEM Collection API documentation master file, created by
   sphinx-quickstart on Fri May 23 22:49:12 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MEM Collection
==============

Welcome to the documentation for my project!

MEM Collection is a (perpetual work-in-progress) project where I manage my personal entomology
collection. It's currently a static website powered by a headless CMS and API.

The project started out as a way for me to manage the data associated with my specimens and expanded
into a label generator, a storage place for my collection of live insect photographs, and a platform
to view the data associated with each specimen (including maps pinpointing collection sites).

The backend is powered by `headless Wagtail <https://wagtail.org/headless/>`_, while the frontend
is built with `Eleventy.js <https://www.11ty.dev/>`_. While a static site generator may not be the best
choice for a website powered by an API, I got tired of working with client-side JavaScript
libraries/frameworks. And while many JS frameworks are now shifting to server-side rendering (e.g.,
Next.js), I just wanted something simple. Something fast. And Eleventy fit that perfectly for me.

The docs are split between the backend and frontend areas (with the backend being better documented
at the moment). If you want to try running this project locally, you'll need to clone both repos
for the optimal experience.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   backend/index
   frontend/index
