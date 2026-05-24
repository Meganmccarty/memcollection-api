Getting Started
===============

This project will likely be something no one else will want to play with, but the steps to getting a
local working copy up and running are below. (It's also good practice for me to thoroughly document
my code, as I am very liable to forget stuff.)

First, clone this repo from GitHub:

.. code::

    git clone git@github.com:Meganmccarty/memcollection-api.git

Environment Variables
---------------------

You'll need to create an ``.env`` file in the project's root directory. Both Django and Docker expect
a few environment variables to be present to properly run.

After creating the ``.env`` file, add the following variables to it:

.. code::

    DATABASE_NAME=postgres
    DATABASE_PASSWORD=postgres
    DATABASE_USER=postgres
    DJANGO_SETTINGS_MODULE=memcollection.settings.dev
    SECRET_KEY=Your Django Secret Key Here

You can use a `secret key generator <https://djecrety.ir/>`_ for the ``SECRET_KEY`` value.

Docker
------

This project uses `Docker Compose <https://docs.docker.com/compose/>`_ to manage containers (one for
the Wagtail web app, and another for the Postgres database). You'll need to install
`Docker Desktop <https://www.docker.com/products/docker-desktop/>`_ in order to start the
containers.

I have a Makefile set up for running all of the various commands referenced through these docs. If
you want a complete list of all the available commands and what they do, just run ``make help``.

Building/Starting Containers
****************************

To get the containers up and running, execute the following two commands in your terminal:

.. code::

    make build
    make up

After the containers are up, you should find that two services have been created: one for the
Wagtail app, and another for the Postgres database. You should be able to access the app at
http://localhost:8000/.

You may need to run migrations before anything else. To do so, run the following in a separate
terminal:

.. code::

    make migrations
    make migrate

You'll then need to create a user account to access the Wagtail admin. In the terminal, run:

.. code::

    make createsuperuser

You should then be prompted in the terminal for credentials. You can press enter to select the
defaults (user = 'wagtail', email = '') and input a password. Afterwards, use your newly-created
user account to log into the Wagtail admin at http://localhost:8000/admin.

Stopping/Destroying Containers
******************************

To stop the containers, press ``Ctrl+C`` in the terminal where your containers are running.

If you want to tear down the containers, simply run ``make down``. This command will NOT wipe out
the contents of your database, as they are stored on a volume (``/postgres-data``) within the
project directory.

.. danger::

    If you find you want to wipe out everything, simply run ``make prune``. Be careful with this
    command! This will prune your system, containers, images, and volumes. You WILL lose the
    contents of your database!

If, while developing, you find you need to rebuild an image without caching, there's a command for
that too: ``make build-no-cache``.

Macbooks with M Chips
*********************

When I first started this project on a newer Macbook with an M chip, I ran into some issues with
building and running a postgres Docker container, so I created a separate set of Mac-specific
Makefile commands and a separate Docker Compose file to get a postgres container up and running.
There are 3 Mac-specific commands:

.. code::

    make mac-build
    make mac-build-no-cache
    make mac-up

Somehow, the non-M chip commands started magically working on my M3 chip laptop (it may have been
when I upgraded the postgres image from 15 to 17 in the regular ``docker-compose.yaml`` file);
despite this, I'm keeping the separate set of Makefile commands and the separate Docker Compose
file in case they are needed on a different M chip Macbook.

Project Structure
-----------------

This project follows typical Django and Wagtail organizational patterns. Code that handles a
specific area is contained within its own "app". Some of the apps come by default with Wagtail, and
I haven't removed them or changed them (but keeping in case I end up utilizing them down the road).

.. code::

    memcollection-api/          Project root
    |--core/                    App containing shared utilities, models, and views
       |--templates/            Contains templates that override Wagtail's defaults (must be contained in an app)
    |--docs/                    Where these docs are located
    |--geography/               App for geography models, snippets, serializers, etc.
    |--home/                    Default Wagtail app (not currently used)
    |--images/                  App for image models, snippets, serializers, etc. This is NOT a default app (it is for my live insect photos)
    |--memcollection/           Default Django directory for things like settings and static files
       |--templates/            All other templates are here
    |--pages/                   App for page models, snippets, serializers, etc. This is NOT a default app (it is for my custom species pages)
    |--search/                  Default Wagtail app (not currently used)
    |--specimens/               App for specimen models, snippets, serializers, etc.
    |--taxonomy/                App for taxonomy models, snippets, serializers, etc.

Loading in Sample Data
----------------------

If you want to play around with some sample data, you can run the following command to seed some
fixture data into the database:

.. code::

    make load-fixtures

This will add data for the geography, taxonomy, and specimen apps. You can then run the following
command to create species pages for the species that were added from the fixtures:

.. code::

    make create-species-pages

Interacting with the Frontend
-----------------------------

This project only contains the backend of my application (as it is a headless CMS with an API),
though if you want to play with the frontend piece of my project, then you can `check out the
README for it on GitHub. <https://github.com/Meganmccarty/memcollection-site>`_
