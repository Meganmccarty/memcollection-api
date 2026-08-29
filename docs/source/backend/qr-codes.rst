QR Codes
========

When working in my collection, it's sometimes helpful to access a specimen's record on my web app
to view additional information not present on the label. Rather than have to type in the specimen's
unique identifier into the URL, I decided to generate QR codes to print alongside the labels that,
when scanned with a smart phone, will take me directly to that specimen's page on my site.

Creating the Short Codes
------------------------

There is a read-only field on the ``SpecimenRecord`` model called ``short_code``. This ``short_code``
is just the unique specimen identifier (``usi``) but without the letters and hyphen (so
``MEM-000001`` becomes ``000001``). This short code is used to generate a shortened URL, as shorter
URLs make it easier to generate a smaller QR code that is still scannable.

This field gets populated whenever a ``SpecimenRecord`` is saved. However, there are also a couple
of management commands that can be run to generate the short codes (these really shouldn't need to
be used, except for the very first case of me implementing this feature and having some specimens
without the short code).

To generate short codes for only specimens that lack them, run the following command:

.. code::

    make generate-short-codes

To generaet short codes for all specimens (whether or not they already have them), run the following
command:

.. code::

    make generate-short-codes --all

.. note:: You'll likely be running these commands in prod, rather than locally (though if your
    local database is just a copy of prod, you can run them locally instead and get the same
    results). To run the commands in prod, you'll first have to run ``make fly-auth`` followed by
    ``make fly-run-command command="python manage.py generate_short_codes"``.

Exporting QR Codes for Printing
-------------------------------

In the Wagtail admin, there's a link in the main left navigation, "Export QR Codes"
(``/admin/export-qr-codes/``). This takes you to a form where you can enter a range of specimens for
which you want to generate QR codes. Submitting the form generates a PDF with the QR codes that's
downloaded to your machine. If you don't provide a range of specimens, then QR codes are generated
for all specimens in the database.

How the QR Codes Work
---------------------

Because I needed the QR codes to be small enough to fit on a specimen label, I needed to shorten the
URLs encoded while still taking the user to the correct specimen page on the frontend when scanned.
The URLs encoded in the QR codes are in the following format:
``www.memcollection.com/s/{short_code}``. Navigating to a URL like this will redirect the user to
the corresponding URL: ``https://www.memcollection.com/specimens/{full_usi}``.

The actual redirect lives in a ``.htaccess`` file within the Eleventy frontend. Because it's just a
static file hosted alongside my frontend, if my backend server were to go down, the QR codes will
still work (so long as my frontend remains live!).
