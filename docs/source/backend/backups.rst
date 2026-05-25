Backups
=======

.. note:: This doc really is solely for me, so that I can remember how to properly make backups AND
   restore from those backups.

Backing up data is super important for this project. The production database is currently hosted
on `Neon <https://neon.com/>`_, which is a managed, serverless postgres provider. (I used to use
an unmanaged Fly.io postgres database, but when their managed option released and started at
$35/month, I decided to find another database provider.)

Manual Backups
--------------

Backing up and restoring data is super easy thanks to ``pg_dump`` and ``pg_restore``. The process is
similar between local and prod databases, though prod takes a few more steps. These steps assume
you have created a folder in the project's root directory called ``db_backups``, and that you have
installed `postgresql client tools <https://www.postgresql.org/>`_ (so that ``pg_dump`` and
``pg_restore`` can be used outside the Docker containers).

Creating a Local Backup
***********************

To make a local backup of the complete database, run the following command:

.. code::

    make full-local-backup

This will create a ``.backup`` file within the ``db_backups/`` directory, formatted as
``YYYYMMDDHHMMSS_local.backup``.

You can verify that the backup was successfully created by running

.. code::

    make verify-backup filename=db_backups/<name-of-local-backup-file>

which should produce copious amounts of output in the terminal.

Troubleshooting
***************

I noticed that while attempting to make a local backup of my data, I got the following warning in my
terminal:

.. code::

    WARNING:  database "postgres" has a collation version mismatch
    DETAIL:  The database was created using collation version 2.36, but the operating system provides version 2.41.
    HINT:  Rebuild all objects in this database that use the default collation and run ALTER DATABASE postgres REFRESH COLLATION VERSION, or build PostgreSQL with the right library version.

To resolve this warning, I had to do the following:

1. Run ``docker exec -it <postgres-container-id> /bin/bash``
2. Once in the postgres container, run ``psql --username=<database-username>``
3. Once in the postgres instance, run ``ALTER DATABASE postgres REFRESH COLLATION VERSION;``
4. Next, run ``REINDEX DATABASE <database-name>;``
5. Exit out of the instance with ``\q``, followed by ``exit`` to leave the Docker container
6. Tear down the containers with ``make down`` and spin them back up with ``make mac-up``

Restoring a Local Backup
************************

To restore a local backup, run the following command:

.. code::

    make full-local-restore filename=db_backups/<name-of-local-backup-file>

This will wipe the contents of the current database and replace them with those from the backup.

Creating a Prod Backup
**********************

This section assumes you have a database deployed on Neon, so these steps are specific to that
platform. `Neon has an article on how to perform backups and restores <https://neon.com/docs/manage/backup-pg-dump>`_,
so my docs here will be more abbreviated than their instructions.

Before you can create a backup, you'll need your Neon connection string (remember to switch off
the connection pooling option). Once you've copied your connection string (including the single
quotes), paste it into the following command:

.. code::

    make full-prod-backup dbname=<paste-neon-connection-string-with-single-quotes-here>

Run that command, and a backup will be placed within the ``db_backups/`` folder, just like the local
backups. However, prod backups will have filenames formatted as ``YYYYMMDDHHMMSS_prod.backup``, to
distinguish them from local ones.

Like with local backups, you can verify that the prod backup is valid by running

.. code::

    make verify-backup filename=db_backups/<name-of-prod-backup-file>

Restoring a Prod Backup
***********************

This is where things get a little complex. Rather than restore a backup into the existing database,
Neon requires that you actually create a brand new database into which the restored data will go.

So, within Neon's dashboard, create a new database with the exact same name as the old one. Then,
grab the new database's connection string, and paste it into the following command (again,
remember to include the single quotes and switch off connection pooling):

.. code::

    make full-prod-restore dbname=<paste-neon-connection-string-for-new-db-here-with-single-quotes> filename=db_backups/<name-of-prod-backup-file>

This should successfully create a fresh copy of all your data in the new database. You can now
safely delete the old database.

Additionally, because we now have a new database, the app within Fly.io needs to be updated (since
it's still pointing to the old database). Inside ``.env.production``, update the ``DATABASE_URL``
variable to the new database connection string (no single quotes here, and connection pooling should
be switched on).

.. code::

    DATABASE_URL=paste-neon-connection-string-for-new-db-with-NO-single-quotes

When that's done, run ``make fly-secrets``. You may also have to log into the Fly.io dashboard,
navigate to the Secrets page, and click "Deploy Secrets" for the changes to take effect.

Automatic Backups
-----------------

.. note:: The 'automatic' part of these backups isn't currently working, as GitHub Actions doesn't
    seem to prioritize my my scheduled workflow. For now, the job can be executed manually within
    GitHub Actions. In the future, I plan to utilize `cron-job.org <https://cron-job.org/>`_ to
    ensure that backups are indeed automatic!

I've also set up a scheduled cron job in GitHub Actions that backs up the prod database in Neon
every night (using ``pg_dump``) and stores the file in a Backblaze B2 bucket (you can view the
`GitHub Action file over in GitHub <https://github.com/Meganmccarty/memcollection-api/blob/main/.github/workflows/nightly-db-backup.yaml>`_).
This assumes you've installed the `aws cli <https://aws.amazon.com/cli/>`_; you've created a
private, encrypted bucket (with object lock disabled) in the B2 console; you've created a new app
key and given it access only to the new bucket; and you've saved the app key credentials in both
GitHub Secrets and locally within an aws cli profile. You'll also want to make a note of the
bucket's region and endpoint url (again, for both GitHub Secrets and the aws cli).

In the event that you need to use one of these backups, you first have to download it from
Backblaze. First, log into Backblaze and navigate to the "Browse Files" link under "B2 Cloud
Storage" from the left-side navigation. Next, drill down into the database backups bucket, and find
the file you wish to use for the restore. Copy the file name.

Next, in your local terminal, you need to use the aws cli to download the file (Backblaze won't let
you download it otherwise, as it's encrypted). There's a Make command that uses the aws cli under
the hood. Run the following command to get the file from Backblaze, filling in the necessary
details you saved from earlier:

.. code::

    make get-b2-backup bucket-name=<bucket-name> filename=<path>/<to>/<file>/<filename> new-filename=<name-the-copy-whatever-you-want-here> url=<endpoint-url> region=<region-bucket-is-in> profile=<name-of-aws-profile>

This should make a copy of the file from Backblaze onto your local machine.

Then, to restore it into Neon, follow the steps above for restoring a prod backup, and you should
be set.

Old Way: Using ``dumpdata`` and ``loaddata``
--------------------------------------------

.. note:: Previously, I used Django's ``dumpdata`` and ``loaddata`` commands for backing
    up/restoring data, but there were limitations with this approach. For one, I couldn't back up
    all of the models from the database, as I ran into issues on restore. Even limiting the models
    to only those I created (not Django/Wagtail ones) still sometimes led to problems, so I
    restricted the backups to only include specimen, geography, and taxonomy models. Despite this,
    I'm keeping the old commands here in the docs as well as in the Makefile, as they may come in
    handy to quickly dump data from the database in JSON format. (Though I'm only retaining the
    local commands, as the old prod commands were specific to my unmanaged postgres database on
    Fly.io.)

Creating a Backup
*****************

To make a local backup, run the following command:

.. code::

    make local-backup

This will output a ``.json`` file within the root directory, formatted as
``backup_local_memcollection_<time-stamp>.json``. This file can then be used to restore data in
prod, or it can be moved someplace else (an external hard drive or a cloud drive).

Restoring a Backup
******************

Restoring data into the local database is super easy. First, make sure the backup file is located
in the project's root directory, then simply run:

.. code::

    make local-restore filename=backup_<env>_memcollection_<time-stamp>.json

Boom! Data should be loaded in.
