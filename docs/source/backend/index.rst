Backend
=======

The backend of the project uses `headless Wagtail <https://wagtail.org/headless/>`_, which is built
on top of the Python framework `Django <https://www.djangoproject.com/>`_. I use
`Docker Compose <https://docs.docker.com/compose/>`_ for developing locally, and it handles the
necessary dependencies (so you don't have to install Python, Django, or Wagtail). I also use
`Sphinx <https://www.sphinx-doc.org/en/master/>`_ for generating the docs for both the backend and
frontend (the actual docs are stored in the backend repo, as I wanted to take advantage of some
Sphinx features for auto-generating documentation from Python docstrings).

You can view the `backend repo on GitHub <https://github.com/Meganmccarty/memcollection-api>`_, and
you can visit the `Getting Started <https://docs.memcollection.com/backend/getting-started.html>`_
page to get a copy of the code running locally on your machine.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   developing
   cicd
   deploying
   backups
   qr-codes
   changelog
   reference/index