Frontend
========

The frontend of my project is powered by `Eleventy.js <https://www.11ty.dev/>`_. You'll need to have
Node.js installed locally to run it (as the frontend is not currently utilizing Docker). In addition to
relying on my custom API, the frontend makes use of `Leaflet.js <https://leafletjs.com/>`_ for
displaying maps of where I have collected specimens. Lastly, most of the icons used on the site were
taken directly from (or slightly modified from) `UXWing <https://uxwing.com/>`_. All of their icons
that I used are located two directories: ``/src/public/uxwing`` and ``/src/partials/uxwing``. While their
`license <https://uxwing.com/license/>`_ says that no attribution is required, I feel it's important
to give credit where credit is due. :)

You can view the frontend repo on GitHub, and you can visit the Getting Started page to get a copy
of the code running locally on your machine.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   developing
   changelog