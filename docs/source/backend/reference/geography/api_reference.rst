API Reference
=============

The geography app contains a number of different models related to where a specimen was collected
(or, in the case of live insect photography, where an insect was photographed). There are five
different "levels" of locations, each one more granular than the previous. Included here is also the
endpoint for accessing specific collecting trips I've taken over the years.

Countries
---------

``api/v2/countries/``
*********************

This endpoint returns all of the countries in which I've collected.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/countries/

Response:

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
            ...
        ]
    }

States
------

``api/v2/states/``
******************

This endpoint returns all of the states in which I've collected.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/states/

Response:

.. code::

    {
        "meta": {
            "total_count": 29
        },
        "items": [
            {
                "id": 1,
                "name": "Indiana",
                "abbr": "IN",
                "date_created": "2024-11-12T02:09:06.119000Z",
                "date_modified": "2024-11-12T02:09:06.119000Z",
                "country": 1
            },
            ...
        ]
    }

``api/v2/nested-states/``
*************************

The regular ``api/v2/states/`` endpoint only returns the ``id`` for the ``country`` to which the
state belongs. With the ``api/v2/nested-states/`` endpoint, the entire ``country`` object is
returned instead of just the ``id``.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-states/

Response:

.. code::

    {
        "meta": {
            "total_count": 29
        },
        "items": [
            {
                "id": 1,
                "name": "Indiana",
                "abbr": "IN",
                "date_created": "2024-11-12T02:09:06.119000Z",
                "date_modified": "2024-11-12T02:09:06.119000Z",
                "country": {
                    "id": 1,
                    "name": "United States of America",
                    "abbr": "USA",
                    "date_created": "2024-11-11T16:38:33.295000Z",
                    "date_modified": "2024-11-11T16:38:33.295000Z"
                }
            },
            ...
        ]
    }


Counties
--------

``api/v2/counties/``
********************

This endpoint returns all of the counties (or boroughs/parishes, for states that don't have
counties) in which I've collected.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/counties/

Response:

.. code::

    {
        "meta": {
            "total_count": 93
        },
        "items": [
            {
                "id": 1,
                "name": "Clear Creek",
                "abbr": "Co.",
                "full_name": "Clear Creek Co.",
                "date_created": "2024-11-12T02:59:47.247000Z",
                "date_modified": "2024-11-12T02:59:47.247000Z",
                "state": 5
            },
            ...
        ]
    }

``api/v2/nested-counties/``
***************************

The regular ``api/v2/counties/`` endpoint only returns the ``id`` for the ``state`` to which the
county belongs. With the ``api/v2/nested-counties/`` endpoint, the entire ``state`` object (and the
entire ``country`` object to which that belongs) is returned.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-counties/

Response:

.. code::

    {
        "meta": {
            "total_count": 29
        },
        "items": [
            {
                "id": 1,
                "name": "Clear Creek",
                "abbr": "Co.",
                "full_name": "Clear Creek Co.",
                "date_created": "2024-11-12T02:59:47.247000Z",
                "date_modified": "2024-11-12T02:59:47.247000Z",
                "state": {
                    "id": 5,
                    "name": "Colorado",
                    "abbr": "CO",
                    "date_created": "2024-11-12T02:22:58.370000Z",
                    "date_modified": "2024-11-12T02:22:58.370000Z",
                    "country": {
                        "id": 1,
                        "name": "United States of America",
                        "abbr": "USA",
                        "date_created": "2024-11-11T16:38:33.295000Z",
                        "date_modified": "2024-11-11T16:38:33.295000Z"
                    }
                }
            },
            ...
        ]
    }

Localities
----------

``api/v2/localities/``
**********************

This endpoint returns all of the localities in which I've collected.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/localities/

Response:

.. code::

    {
        "meta": {
            "total_count": 266
        },
        "items": [
            ...,
            {
                "id": 4,
                "name": "Bonanza Creek Experimental Forest",
                "range": "23 km SW",
                "town": "Ester",
                "date_created": "2024-11-14T01:26:52.928000Z",
                "date_modified": "2024-11-14T01:26:52.928000Z",
                "country": null,
                "state": null,
                "county": 3
            },
            ...
        ]
    }

Note that a locality can only belong to one region (for example, a locality cannot belong to both a
state and a county). This is because the lower-level regions (counties and states) already belong to
higher-level regions (states and countries); for example, if a locality belongs to a county, that
county already belongs to a state, and that state already belongs to a country. Setting up the data
in this way was a personal preference of mine, as I wanted to preserve the relationship between the
different levels of regions.

``api/v2/nested-localities/``
*****************************

The regular ``api/v2/localities/`` endpoint only returns the ``id`` for the region to which the
locality belongs (which could either be a county, state, or country). With the
``api/v2/nested-localities/`` endpoint, the region's entire object is returned (and any nested
objects as well). For example, if the locality belongs to a county, that county's object, as well
as the county's state object and that state's country object, will all be returned in a nested
structure.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-localities/

Response:

.. code::

    {
        "meta": {
            "total_count": 29
        },
        "items": [
            ...
            {
                "id": 4,
                "name": "Bonanza Creek Experimental Forest",
                "range": "23 km SW",
                "town": "Ester",
                "date_created": "2024-11-14T01:26:52.928000Z",
                "date_modified": "2024-11-14T01:26:52.928000Z",
                "country": null,
                "state": null,
                "county": {
                    "id": 3,
                    "name": "Fairbanks N. Star",
                    "abbr": "Boro.",
                    "full_name": "Fairbanks N. Star Boro.",
                    "date_created": "2024-11-12T03:00:28.223000Z",
                    "date_modified": "2024-11-12T03:00:28.223000Z",
                    "state": {
                        "id": 2,
                        "name": "Alaska",
                        "abbr": "AK",
                        "date_created": "2024-11-12T02:22:20.633000Z",
                        "date_modified": "2024-11-12T02:22:20.633000Z",
                        "country": {
                            "id": 1,
                            "name": "United States of America",
                            "abbr": "USA",
                            "date_created": "2024-11-11T16:38:33.295000Z",
                            "date_modified": "2024-11-11T16:38:33.295000Z"
                        }
                    }
                }
            },
            ...
        ]
    }

GPS Coordinates
---------------

``api/v2/gps-coordinates/``
***************************

This endpoint returns all of the GPS coordinates documenting where specimens have been collected.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/gps-coordinates/

Response:

.. code::

    {
        "meta": {
            "total_count": 464
        },
        "items": [
            {
                "id": 1,
                "latitude": "38.849500",
                "longitude": "-84.866328",
                "elevation": "252",
                "elevation_meters": "252m",
                "date_created": "2024-11-15T01:58:01.174000Z",
                "date_modified": "2025-06-14T21:34:46.711000Z",
                "locality": 12
            },
            ...
        ]
    }

``api/v2/nested-gps-coordinates/``
**********************************

The regular ``api/v2/gps-coordinates/`` endpoint only returns the ``id`` for the locality to which a
pair of coordinates belongs. With the ``api/v2/nested-gps-coordinates/`` endpoint, the locality's
entire object is returned (and any nested objects as well).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-gps-coordinates/

Response:

.. code::

    {
        "meta": {
            "total_count": 464
        },
        "items": [
            {
                "id": 1,
                "latitude": "38.849500",
                "longitude": "-84.866328",
                "elevation": "252",
                "elevation_meters": "252m",
                "date_created": "2024-11-15T01:58:01.174000Z",
                "date_modified": "2025-06-14T21:34:46.711000Z",
                "locality": {
                    "id": 12,
                    "name": "Boone Robinson Rd",
                    "range": "4 km NW",
                    "town": "Patriot",
                    "date_created": "2024-11-15T01:57:47.058000Z",
                    "date_modified": "2024-11-15T01:57:47.058000Z",
                    "country": null,
                    "state": null,
                    "county": {
                        "id": 7,
                        "name": "Switzerland",
                        "abbr": "Co.",
                        "full_name": "Switzerland Co.",
                        "date_created": "2024-11-12T03:02:06.011000Z",
                        "date_modified": "2024-11-12T03:02:06.011000Z",
                        "state": {
                            "id": 1,
                            "name": "Indiana",
                            "abbr": "IN",
                            "date_created": "2024-11-12T02:09:06.119000Z",
                            "date_modified": "2024-11-12T02:09:06.119000Z",
                            "country": {
                                "id": 1,
                                "name": "United States of America",
                                "abbr": "USA",
                                "date_created": "2024-11-11T16:38:33.295000Z",
                                "date_modified": "2024-11-11T16:38:33.295000Z"
                            }
                        }
                    }
                }
            },
            ...
        ]
    }

Collecting Trips
----------------

``api/v2/collecting-trips/``
****************************

This endpoint returns all of the collecting trips I've taken over the years in pursuit of
butterflies and moths. There isn't another endpoint that contains nested data.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/collecting-trips/

Response:

.. code::

    {
        "meta": {
            "total_count": 20
        },
        "items": [
            {
                "id": 1,
                "name": "Alaska 2016 Trip",
                "slug": "alaska-2016-trip",
                "states": [
                    {
                        "id": 2,
                        "name": "Alaska",
                        "abbr": "AK",
                        "date_created": "2024-11-12T02:22:20.633000Z",
                        "date_modified": "2024-11-12T02:22:20.633000Z",
                        "country": 1
                    }
                ],
                "start_date": "2016-06-25",
                "end_date": "2016-06-26",
                "notes": "",
                "date_created": "2024-11-15T03:52:46.591000Z",
                "date_modified": "2024-11-15T03:52:46.591000Z"
            },
            ...
        ]
    }