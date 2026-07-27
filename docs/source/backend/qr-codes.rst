QR Codes
========

When working in my collection, it's sometimes helpful to access a specimen's record on my web app
to view additional information not present on the label. Rather than have to type in the specimen's
unique identifier into the URL, I decided to generate QR codes to print alongside the labels that,
when scanned with a smart phone, will take me directly to that specimen's page on my site.

Generating the QR codes is a two-step process, broken down in the sections below.

Creating the Short Code and QR Code
-----------------------------------

There are two fields on the ``SpecimenRecord`` model that can be viewed in the Wagtail admin but are
not meant to be edited manually: ``short_code`` and ``qr_code``.

The ``short_code`` is just the unique specimen identifier (``usi``) lowercased and without the
hyphen (so ``MEM-000001`` becomes ``000001``). This short code is used to generate a shortened
URL, as shorter URLs make it easier to generate a smaller QR code that is still scannable.

The ``qr_code`` field is an ``ImageField`` that stores the generated QR code image. You are not
meant to manually upload your own QR code image, as it is created when running a command (more
on that below).

Commands for QR Code Generation
*******************************

Generating QR codes is done via a custom Django management command. There are 4 variants of the
command, all of which are included in the Makefile.

To generate QR codes for all specimens that do not currently have any, run the following command:

.. code::

    make generate-qr-codes

This command will NOT overwrite any existing QR codes, though it may take some time to run in prod
(as it will scan through every specimen checking if it has a QR code or not).

If you want to generate QR codes for all specimens (overwriting any existing ones), run the
following command:

.. code::

    make generate-qr-codes-all

Again, this command will likely take quite a bit of time in prod (and you'll likely have to keep
the app instance running by interacting with it while the command is running).

If you want to create a QR code for a specific specimen, you can run the following command

.. code::

    make generate-qr-code usi=<specimen-usi>

replacing ``<specimen-usi>`` with the unique specimen identifier of the specimen you want a QR code
for. This will overwrite any existing QR code for that specimen.

Lastly, if you have added a bunch of new specimens to the database, you can generate QR codes for
them by entering a range of unique specimen identifiers:

.. code::

    make generate-qr-codes-range start=<start-specimen-usi> end=<end-specimen-usi>

Again, you'd replace the ``<start-specimen-usi>`` and ``<end-specimen-usi>`` with the unique
specimen identifiers of the specimens you need QR codes for. And just like the previous two
commands, running this command will overwrite any existing QR codes for specimens within the range.

After the QR codes are generated, you can view each one from within the ``SpecimenRecord`` in the
admin. They're stored within the Backblaze B2 bucket alongside other uploaded media files.

.. note:: You'll likely be running these commands in prod, rather than locally (though if your
    local database is just a copy of prod, you can run them locally instead and get the same
    results). To run the commands in prod, you'll first have to run ``make fly-auth`` followed by
    ``make fly-run-command command="python manage.py generate_qr_codes"``. You can pass in one of
    the following flags: ``--all``, ``--usi`` (requires supplying a single unique specimen
    identifier), or ``--range`` (requires passing in a starting USI and an ending USI).

Exporting QR Codes for Printing
-------------------------------

Once the QR codes have been generated, you can export them to a PDF for printing. There currently
isn't a command for doing so; rather, you can visit the following URL in your browser, which will
generate the PDF and download it to your computer:

``https://api.memcollection.com/admin/export-qr-codes/``

The URL is present in the Wagtail admin as a main menu item (located in the left-hand navigation
menu). You must be logged in to access the URL, as it is part of the admin interface (copy/pasting
it in your browser will NOT work unless you're already logged in). It may take a few seconds for the
page to load, as generating QR codes for every specimen in the database takes a bit of time.

How the QR Codes Work
---------------------

Because I needed the QR codes to be small enough to fit on a specimen label, I needed to shorten the
URLs encoded while still taking the user to the correct specimen page on the frontend when scanned.
The URLs encoded in the QR codes are in the following format:
``www.memcollection.com/s/{short_code}``. Navigating to a URL like this will redirect the user to
the corresponding URL: ``https://www.memcollection.com/specimens/{full_usi}``.

The actual redirect lives in a ``.htaccess`` file within the Eleventy frontend. Because it's just a
static file, if my backend server were to go down, the QR codes will still work.
