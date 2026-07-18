API Reference
=============

The specimens app contains two endpoints related to individual specimens: the specimen records
themselves, as well as an endpoint for the people involved in the collection of my specimens.

People
------

``api/v2/people/``
******************

This endpoint returns all of the people who have collected, determined, and/or prepared specimens
in my collection.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/people/

Response:

.. code::

    {
        "meta": {
            "total_count": 18
        },
        "items": [
            {
                "id": 1,
                "first_name": "Megan",
                "middle_initial": "E",
                "last_name": "McCarty",
                "suffix": null,
                "collector_name": "M. McCarty",
                "full_name": "Megan E. McCarty",
                "date_created": "2024-11-24T18:31:41.519000Z",
                "date_modified": "2024-11-24T18:31:41.519000Z"
            },
            ...
        ]
    }

Specimen Records
----------------

``api/v2/specimen-records/``
****************************

The most important API endpoint!!! This endpoint returns all of the specimen records in my
collection (and every single field associated with the SpecimenRecord model). It's quite a bit of
data.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/specimen-records/

Response:

.. code::

    {
        "meta": {
            "total_count": 4
        },
        "items": [
            {
                "id": 1,
                "usi": "MEM-000001",
                "order": {
                    "id": 1,
                    "name": "Lepidoptera",
                    "common_name": "Butterflies and Moths",
                    "authority": "Linnaeus, 1758",
                    "date_created": "2024-11-17T00:37:27.071000Z",
                    "date_modified": "2024-11-17T00:37:27.071000Z"
                },
                "family": {
                    "id": 1,
                    "name": "Papilionidae",
                    "common_name": "Swallowtails and Parnassians",
                    "authority": "Latreille, [1802]",
                    "date_created": "2024-11-17T00:37:47.482000Z",
                    "date_modified": "2025-07-20T04:56:11.176000Z",
                    "order": 1
                },
                "subfamily": {
                    "id": 2,
                    "name": "Papilioninae",
                    "common_name": "Swallowtails",
                    "authority": "Latreille, [1802]",
                    "date_created": "2024-11-17T18:41:30.119000Z",
                    "date_modified": "2025-07-20T04:56:14.052000Z",
                    "family": 1
                },
                "tribe": {
                    "id": 2,
                    "name": "Papilionini",
                    "common_name": "Swallowtails",
                    "authority": "Latreille, [1802]",
                    "date_created": "2024-11-17T18:42:29.528000Z",
                    "date_modified": "2025-07-20T04:56:17.421000Z",
                    "subfamily": 2
                },
                "genus": {
                    "id": 2,
                    "name": "Papilio",
                    "common_name": "Swallowtails",
                    "authority": "Linnaeus, 1758",
                    "date_created": "2024-11-17T18:43:10.815000Z",
                    "date_modified": "2025-07-20T04:56:26.544000Z",
                    "tribe": 2
                },
                "species": {
                    "id": 3,
                    "name": "polyxenes",
                    "binomial": "Papilio polyxenes",
                    "common_name": "Black Swallowtail",
                    "authority": "Fabricius, 1775",
                    "mona": "4159",
                    "p3": null,
                    "ps": "77a0366",
                    "date_created": "2024-11-17T18:51:41.837000Z",
                    "date_modified": "2025-07-20T05:06:02.461000Z",
                    "genus": 2
                },
                "subspecies": null,
                "taxon": {
                    "id": 3,
                    "name": "polyxenes",
                    "binomial": "Papilio polyxenes",
                    "common_name": "Black Swallowtail",
                    "authority": "Fabricius, 1775",
                    "mona": "4159",
                    "p3": null,
                    "ps": "77a0366",
                    "date_created": "2024-11-17T18:51:41.837000Z",
                    "date_modified": "2025-07-20T05:06:02.461000Z",
                    "genus": 2
                },
                "determiner": {
                    "id": 1,
                    "first_name": "Megan",
                    "middle_initial": "E",
                    "last_name": "McCarty",
                    "suffix": null,
                    "collector_name": "M. McCarty",
                    "full_name": "Megan E. McCarty",
                    "date_created": "2024-11-24T18:31:41.519000Z",
                    "date_modified": "2024-11-24T18:31:41.519000Z"
                },
                "determined_year": 2024,
                "sex": "male",
                "stage": "adult",
                "preparer": {
                    "id": 1,
                    "first_name": "Megan",
                    "middle_initial": "E",
                    "last_name": "McCarty",
                    "suffix": null,
                    "collector_name": "M. McCarty",
                    "full_name": "Megan E. McCarty",
                    "date_created": "2024-11-24T18:31:41.519000Z",
                    "date_modified": "2024-11-24T18:31:41.519000Z"
                },
                "preparation": "spread",
                "preparation_date": null,
                "labels_printed": false,
                "labeled": false,
                "photographed": true,
                "identified": true,
                "collecting_trip": null,
                "country": {
                    "id": 1,
                    "name": "United States of America",
                    "abbr": "USA",
                    "date_created": "2024-11-11T16:38:33.295000Z",
                    "date_modified": "2024-11-11T16:38:33.295000Z"
                },
                "state": {
                    "id": 1,
                    "name": "Indiana",
                    "abbr": "IN",
                    "date_created": "2024-11-12T02:09:06.119000Z",
                    "date_modified": "2024-11-12T02:09:06.119000Z",
                    "country": 1
                },
                "county": {
                    "id": 7,
                    "name": "Switzerland",
                    "abbr": "Co.",
                    "full_name": "Switzerland Co.",
                    "date_created": "2024-11-12T03:02:06.011000Z",
                    "date_modified": "2024-11-12T03:02:06.011000Z",
                    "state": 1
                },
                "locality": {
                    "id": 12,
                    "name": "Boone Robinson Rd",
                    "range": "4 km NW",
                    "town": "Patriot",
                    "date_created": "2024-11-15T01:57:47.058000Z",
                    "date_modified": "2024-11-15T01:57:47.058000Z",
                    "country": null,
                    "state": null,
                    "county": 7
                },
                "gps": {
                    "id": 1,
                    "latitude": "38.849500",
                    "longitude": "-84.866328",
                    "elevation": "252",
                    "elevation_meters": "252m",
                    "date_created": "2024-11-15T01:58:01.174000Z",
                    "date_modified": "2025-06-14T21:34:46.711000Z",
                    "locality": 12
                },
                "day": 26,
                "month": "June",
                "year": 2006,
                "collected_date": "26-Jun-2006",
                "full_date": "26 June 2006",
                "num_date": "2006-06-26",
                "collector": [
                    {
                        "id": 1,
                        "first_name": "Megan",
                        "middle_initial": "E",
                        "last_name": "McCarty",
                        "suffix": null,
                        "collector_name": "M. McCarty",
                        "full_name": "Megan E. McCarty",
                        "date_created": "2024-11-24T18:31:41.519000Z",
                        "date_modified": "2024-11-24T18:31:41.519000Z"
                    }
                ],
                "collectors": "M. McCarty",
                "method": "Net",
                "weather": "",
                "temperature": "76",
                "temp_F": "76°F",
                "temp_C": "24.4°C",
                "time_of_day": "12:39 PM",
                "habitat": "<p data-block-key=\"7fd8k\">Nectaring on Trifolium pratense</p>",
                "notes": "",
                "date_created": "2025-01-08T01:45:12.578000Z",
                "date_modified": "2025-07-31T20:38:59.389018Z"
            },
            ...
        ]
    }