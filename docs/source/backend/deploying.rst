Deploying
=========

This project (along with its docs!) is deployed to `Fly.io <https://fly.io/>`_. GitHub Actions is
configured to deploy the project whenever changes are pushed to the main branch. (You can see how
the commands are configured under ``.github/workflows/fly.yaml`` and
``.github/workflows/fly-docs.yaml``.)

However, there are still some little quirks I have yet to work out. For example, the only way to
configure the prod environment variables is to do either one of the following:

1. Manually update them on the Fly.io Dashboard
2. Update them locally in a ``.env.production`` file and then run ``make fly-secrets``

I haven't figured out how to pass secrets from GitHub to GitHub Actions without having to manually
authenticate to Fly.io.

Manually Deploying
------------------

I also configured the project in such a way that I can deploy from my laptop. (Actually, I did that
first to see if it worked before trying to do so via GitHub Actions, and then I was too lazy to
remove this feature once I got GitHub Actions working.)

These steps below are more for me than for anyone else, as they assume you've completed the
following tasks:

* Set up hosting for media assets (using `Backblaze B2 Cloud Storage <https://www.backblaze.com/cloud-storage>`_)
* Set up hosting for the actual web app (using Fly.io)
* Set up a ``.env.production`` file for storing secrets used in the prod environment

Wagtail has a `nice guide for deploying to Fly.io <https://docs.wagtail.org/en/stable/deployment/flyio.html>`_,
which is what I used initially. However, I deviated from the instructions towards the end; after
running ``fly launch``, I chose to NOT overwrite my ``.dockerignore`` or my ``Dockerfile``, as doing
so led to deployment errors. I then found and used
`Tom Usher's blog series on deploying Wagtail to Fly.io <https://usher.dev/posts/2022-08-30-wagtail-on-flyio/part-1/>`_
to get me over the hump of deployment errors.

After the initial setup is done, you can run the following command to authenticate (if you aren't
currently authenticated)

.. code::

    make fly-auth

Once that's done, you can deploy by running

.. code::

    make fly-deploy
