Developing - Frontend
=====================

The ``package.json`` file has a variety of different commands to make developing easier. I chose to
use TypeScript and Sass, so there are commands that are used directly within the ``npm run start``
and ``npm run build`` commands to ensure everything is correctly transpiled. Running
``npm run lint`` will lint the HTML, SCSS, and TypeScript using pally-ci, stylelint, and eslint,
respectively. I've also set up unit and integration testing with Jest and Cypress, and you can run
the test suites with ``npm run test``. All of these tools should be ready to use as-is (no
additional configuration is required).

``git-flow``
------------

I am using git-flow to manage changes in this project.

Feature Branches
****************

You can create a new feature branch off of ``develop`` by running

.. code::

    git flow feature start NAME-OF-YOUR-FEATURE-BRANCH-HERE

After commiting your changes, you can publish the feature branch on GitHub by
running

.. code::

    git flow feature publish NAME-OF-YOUR-FEATURE-BRANCH-HERE

Open a PR on GitHub; this will lint, format, and test the code before it is merged back into
``develop``. If the tests pass, you can merge your feature branch by running

.. code::

    git flow feature finish NAME-OF-YOUR-FEATURE-BRANCH-HERE

Make sure to push your changes after merging.

Release Branches
****************

.. note::

    The release process for the frontend will also require a separate backend release in order to
    update the docs. I know it's confusing, but that's what I get for wanting to keep all of my docs
    within the backend repo...

Frontend
########

Starting with the FRONTEND repo, you can start a release by running

.. code::

    git flow release start x.y.z

Make sure to update the version number in ``package.json`` and commit those changes:

.. code::

    git add .
    git commit -m "Bump version in package.json"

Then, publish the release branch by running

.. code::

    git flow release publish x.y.z

Open a PR on GitHub to merge the release into ``main``. Again, the code will be linted, formatted,
and tested.

If all tests pass, go ahead and run

.. code::

    git flow release finish x.y.z

Follow the prompts in the terminal when merging the release back into both the ``develop`` and ``main``
branches. For the commit message for the tag, just use the version number (x.y.z) as the message.

Make sure to push your changes after merging:

.. code::

    git push origin develop main --no-verify --tags

Backend
#######

Next in the BACKEND repo, go ahead and also start a release

.. code::

    git flow release start x.y.z

Make sure to update the version number in ``memcollection/settings/base.py`` and ``package.json``
and commit those changes:

.. code::

    git add .
    git commit -m "Bump version in memcollection/settings/base.py and package.json"

Then, back in the FRONTEND repo, update the changelog by running

.. code::

    npm run changelog

The changelog output will be placed in the BACKEND's docs directory. Navigate back to the BACKEND.
Make any necessary changes/adjustments to the auto-generated output, then commit those changes:

.. code::

    git add .
    git commit -m "Update changelog"

Follow the same steps above used for the frontend repo for publishing a feature branch, opening a
PR, merging the PR (after linting/tests pass), and pushing the changes post-merge.