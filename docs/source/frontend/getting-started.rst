Getting Started - Frontend
==========================

Given that this site relies on my custom API, this repo will probably be of limited use to everyone
except me. However, if you are interested in playing around with the code, you can clone the repo
from GitHub.

.. code::

    git clone git@github.com:Meganmccarty/memcollection-site.git

You'll need to have `Node.js <https://nodejs.org/en>`_ installed on your local machine in order to
run the project. Using the latest version is probably best, though I am currently using Node
v22.17.1 and npm version 10.9.2.

Once you have a copy of the repo, just run ``npm install`` followed by ``npm run start`` to get a
server up and running. The site should be available under ``http://localhost:8080/``. Eleventy will
automatically watch for any file changes and update the browser accordingly (though it may take a
moment for Eleventy to rebuild the HTML files).

Connecting to the Custom API
----------------------------

Note that, because this project relies on my custom API, you may want to also clone it and spin up
the necessary Docker containers on your machine (otherwise, you'll have a very empty Eleventy
project!). You can `read the docs on how to get started with my
API <https://docs.memcollection.com/backend/getting-started.html>`_.

If you do end up using my custom API (and populate it with sample data, whether your own or from
the fixtures present in the backend repo), you'll then need to create a ``.env.development`` file in
the project's root directory and add the following variable:

.. code::

    API_BASE_URL=http://localhost:8000/api/v2

This will enable Eleventy to fetch data from the API. It'll cache the data in a ``.cache/`` folder,
so once you have the data, you don't need to keep the backend Docker containers running (unless you
make changes to the data stored in the database that you'd like to see on frontend, in which case,
you'd delete the cache files from Eleventy and rebuild the site).

Project Structure
-----------------

This project is structured a little confusingly -- or at least, every time I come back to it after
not touching it for months, I have a hard time finding what I need. So, this is more a reminder for
my future self than anything else.

.. code::

    memcollection-site/         Project root, contains all of the various config files (so many)
    |--.cache/                  EleventyFetch API caches (NOT COMMITTED). Delete these files if you want Eleventy to pull fresh data from the API
    |--cypress/                 Where the end-to-end tests are located
       |--e2e/                  Actual end-to-end tests
       |--support/              There's a custom function in here to output a11y violations into the terminal (because I do love verbosity)
    |--dist/                    The compiled/transpiled code (NOT COMMITTED)
    |--src/                     Where everything lives
        |--js/                  Home of the TypeScript files. Most files and their associated test files live directly in this directory
            |--fixtures/        Data for testing
            |--labels/          Additional functions for the label generator
            |--navigation/      Additional functions for the nav bar
            |--type/            Misleadingly, only interfaces are in here right now
            |--utilities/       Extra random functions live here
        |--pages/               Includes whole pages, sitemaps, and extra JavaScript we fetch from ourselves
            |--_data/           Where EleventyFetch API calls are made
                |--fixtures/    JSON files with fake data for testing
        |--partials/            Partial pages + the base layout template
            |--uxwing/          Nunjucks files containing SVG icons from UXWing
        |--public/              Just a bunch of icons
            |--uxwing/          Actual SVG files from UXWing (they will likely be converted to Nunjucks files down the road)
        |--scss/                All the SASS
