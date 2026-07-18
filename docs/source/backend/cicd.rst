CI/CD
=====

I have set up GitHub Actions to run the linting, formatting, and testing commands whenever code is
pushed to the ``develop`` and ``main`` branches. These commands will also run whenever a pull
request is opened for the ``develop`` and ``main`` branches. You can find the code that runs these
commands under ``.github/workflows/test.yaml``.

The linting and formatting commands are slightly different in the CI/CD compared to the ones you run
locally. With linting, the total number of issues found will be outputted in the terminal. With
formatting, Black will just check for issues, not automatically fix them. Any issues found would
need to be manually fixed, committed, and pushed, and GitHub Actions will rerun the commands.
