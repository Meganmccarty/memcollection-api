Reference
=========

I decided to create a reference of my app's models and API endpoints. It seemed pretty cool to have
Sphinx auto-generate documentation from my models' docstrings, even if doing so isn't all that
useful. I left out auto-generating documentation for things like viewsets, serializers, and Wagtail
hooks, as they're all more or less the same.

The API for MEMCollection is built around REST principles (using Wagtail API, which is built on top
of the Django REST Framework). It can be accessed by navigating to `<https://api.memcollection.com/>`_.
All of the various API endpoints are prepended with ``api/v2/`` (there isn't an actual page if you
navigate directly to this URL).

The data is returned as a JSON object containing two keys. The first one is the ``meta`` key, which
points to another object containing metadata (for example, there is a ``total_count`` object
telling you how many items are returned). The second one is an ``items`` key, which points to an
array of objects that represent certain pieces of data.

For example, navigating to ``api/v2/countries/`` will return the following data:

.. code::

   {
      "meta": {
         "total_count": 3
      },
      "items": [
         {
               "id": 1,
               "name": "United States of America",
               "abbr": "USA",
               "date_created": "2024-11-11T16:38:33.295000Z",
               "date_modified": "2024-11-11T16:38:33.295000Z"
         },
         {
               "id": 2,
               "name": "Mexico",
               "abbr": "MEX",
               "date_created": "2024-11-11T23:58:48.707000Z",
               "date_modified": "2024-11-11T23:58:48.707000Z"
         },
         {
               "id": 3,
               "name": "Canada",
               "abbr": "CAN",
               "date_created": "2024-11-11T23:58:56.579000Z",
               "date_modified": "2024-11-11T23:58:56.579000Z"
         }
      ]
   }

By default, the Wagtail API returns up to 20 items for a given query. I don't like this one bit, so,
to change this, simply append ``?limit=<PUT-ANY-NUMBER-HERE>`` to the endpoint you're using.

Note that there is no API key or access token needed to access this data. Data returned by the
Wagtail API is read-only (anything other than GET is not allowed). Thus, the data in my collection
is publicly available.

For specific endpoint references, use the table of contents below to see specific examples for
different parts of the app.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   core/index
   geography/index
   images/index
   pages/index
   specimens/index
   taxonomy/index
