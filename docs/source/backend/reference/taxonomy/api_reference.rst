API Reference
=============

The taxonomy app contains a number of different models related to the scientific names of organisms.
I've created models for the following taxonomic levels: order, family, subfamily, tribe, genus,
species, and subspecies. 

Orders
------

``api/v2/orders/``
******************

This endpoint returns all of the orders for which I have representatives in the collection (whether
dead specimens or live insect photographs).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/orders/

Response:

.. code::

    {
        "meta": {
            "total_count": 15
        },
        "items": [
            {
                "id": 1,
                "name": "Lepidoptera",
                "common_name": "Butterflies and Moths",
                "authority": "Linnaeus, 1758",
                "date_created": "2024-11-17T00:37:27.071000Z",
                "date_modified": "2024-11-17T00:37:27.071000Z"
            },
            ...
        ]
    }

Families
--------

``api/v2/families/``
********************

This endpoint returns all of the families for which I have representatives in the collection
(whether dead specimens or live insect photographs).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/families/

Response:

.. code::

    {
        "meta": {
            "total_count": 66
        },
        "items": [
            {
                "id": 1,
                "name": "Papilionidae",
                "common_name": "Swallowtails and Parnassians",
                "authority": "Latreille, [1802]",
                "date_created": "2024-11-17T00:37:47.482000Z",
                "date_modified": "2025-07-20T04:56:11.176000Z",
                "order": 1
            },
            ...
        ]
    }

``api/v2/nested-families/``
***************************

The regular ``api/v2/families/`` endpoint only returns the ``id`` for the ``order`` to which the
family belongs. With the ``api/v2/nested-families/`` endpoint, the entire ``order`` object is
returned instead of just the ``id``.

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-families/

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


Subfamilies
-----------

``api/v2/subfamilies/``
***********************

This endpoint returns all of the subfamilies for which I have representatives in the collection
(whether dead specimens or live insect photographs).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/subfamilies/

Response:

.. code::

    {
        "meta": {
            "total_count": 119
        },
        "items": [
            {
                "id": 1,
                "name": "Parnassiinae",
                "common_name": "Parnassians and Apollos",
                "authority": "Duponchel, [1835]",
                "date_created": "2024-11-17T01:09:17.669000Z",
                "date_modified": "2025-07-20T05:11:21.364000Z",
                "family": 1
            },
            ...
        ]
    }

``api/v2/nested-subfamilies/``
******************************

The regular ``api/v2/subfamilies/`` endpoint only returns the ``id`` for the ``family`` to which the
subfamily belongs. With the ``api/v2/nested-subfamilies/`` endpoint, all of the higher-level taxon
objects are returned as well (for subfamilies, this includes both the family and order objects).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-subfamilies/

Response:

.. code::

    {
        "meta": {
            "total_count": 119
        },
        "items": [
            {
                "id": 1,
                "name": "Parnassiinae",
                "common_name": "Parnassians and Apollos",
                "authority": "Duponchel, [1835]",
                "date_created": "2024-11-17T01:09:17.669000Z",
                "date_modified": "2025-07-20T05:11:21.364000Z",
                "family": {
                    "id": 1,
                    "name": "Papilionidae",
                    "common_name": "Swallowtails and Parnassians",
                    "authority": "Latreille, [1802]",
                    "date_created": "2024-11-17T00:37:47.482000Z",
                    "date_modified": "2025-07-20T04:56:11.176000Z",
                    "order": {
                        "id": 1,
                        "name": "Lepidoptera",
                        "common_name": "Butterflies and Moths",
                        "authority": "Linnaeus, 1758",
                        "date_created": "2024-11-17T00:37:27.071000Z",
                        "date_modified": "2024-11-17T00:37:27.071000Z"
                    }
                }
            },
            ...
        ]
    }

Tribes
------

``api/v2/tribes/``
******************

This endpoint returns all of the tribes for which I have representatives in the collection
(whether dead specimens or live insect photographs).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/tribes/

Response:

.. code::

    {
        "meta": {
            "total_count": 168
        },
        "items": [
            {
                "id": 1,
                "name": "Parnassiini",
                "common_name": "Parnassians",
                "authority": "Duponchel, [1835]",
                "date_created": "2024-11-17T02:50:05.119000Z",
                "date_modified": "2025-07-20T05:11:23.848000Z",
                "subfamily": 1
            },
            ...
        ]
    }

``api/v2/nested-tribes/``
*************************

The regular ``api/v2/tribes/`` endpoint only returns the ``id`` for the ``subfamily`` to which the
subfamily belongs. With the ``api/v2/nested-tribes/`` endpoint, all of the higher-level taxon
objects are returned as well (for tribes, this includes the subfamily, family, and order
objects).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-tribes/

Response:

.. code::

    {
        "meta": {
            "total_count": 168
        },
        "items": [
            {
                "id": 1,
                "name": "Parnassiini",
                "common_name": "Parnassians",
                "authority": "Duponchel, [1835]",
                "date_created": "2024-11-17T02:50:05.119000Z",
                "date_modified": "2025-07-20T05:11:23.848000Z",
                "subfamily": {
                    "id": 1,
                    "name": "Parnassiinae",
                    "common_name": "Parnassians and Apollos",
                    "authority": "Duponchel, [1835]",
                    "date_created": "2024-11-17T01:09:17.669000Z",
                    "date_modified": "2025-07-20T05:11:21.364000Z",
                    "family": {
                        "id": 1,
                        "name": "Papilionidae",
                        "common_name": "Swallowtails and Parnassians",
                        "authority": "Latreille, [1802]",
                        "date_created": "2024-11-17T00:37:47.482000Z",
                        "date_modified": "2025-07-20T04:56:11.176000Z",
                        "order": {
                            "id": 1,
                            "name": "Lepidoptera",
                            "common_name": "Butterflies and Moths",
                            "authority": "Linnaeus, 1758",
                            "date_created": "2024-11-17T00:37:27.071000Z",
                            "date_modified": "2024-11-17T00:37:27.071000Z"
                        }
                    }
                }
            },
            ...
        ]
    }

Genera
------

``api/v2/genera/``
******************

This endpoint returns all of the genera for which I have representatives in the collection
(whether dead specimens or live insect photographs).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/genera/

Response:

.. code::

    {
        "meta": {
            "total_count": 341
        },
        "items": [
            {
                "id": 1,
                "name": "Parnassius",
                "common_name": "Parnassians",
                "authority": "Latreille, 1804",
                "date_created": "2024-11-17T15:39:09.086000Z",
                "date_modified": "2025-07-20T05:11:33.574000Z",
                "tribe": 1
            },
            ...
        ]
    }

``api/v2/nested-genera/``
*************************

The regular ``api/v2/genera/`` endpoint only returns the ``id`` for the ``tribe`` to which the genus
belongs. With the ``api/v2/nested-genera/`` endpoint, all of the higher-level taxon objects are
returned as well (for genera, this includes the tribe, subfamily, family, and order
objects).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-genera/

Response:

.. code::

    {
        "meta": {
            "total_count": 341
        },
        "items": [
            {
                "id": 1,
                "name": "Parnassius",
                "common_name": "Parnassians",
                "authority": "Latreille, 1804",
                "date_created": "2024-11-17T15:39:09.086000Z",
                "date_modified": "2025-07-20T05:11:33.574000Z",
                "tribe": {
                    "id": 1,
                    "name": "Parnassiini",
                    "common_name": "Parnassians",
                    "authority": "Duponchel, [1835]",
                    "date_created": "2024-11-17T02:50:05.119000Z",
                    "date_modified": "2025-07-20T05:11:23.848000Z",
                    "subfamily": {
                        "id": 1,
                        "name": "Parnassiinae",
                        "common_name": "Parnassians and Apollos",
                        "authority": "Duponchel, [1835]",
                        "date_created": "2024-11-17T01:09:17.669000Z",
                        "date_modified": "2025-07-20T05:11:21.364000Z",
                        "family": {
                            "id": 1,
                            "name": "Papilionidae",
                            "common_name": "Swallowtails and Parnassians",
                            "authority": "Latreille, [1802]",
                            "date_created": "2024-11-17T00:37:47.482000Z",
                            "date_modified": "2025-07-20T04:56:11.176000Z",
                            "order": {
                                "id": 1,
                                "name": "Lepidoptera",
                                "common_name": "Butterflies and Moths",
                                "authority": "Linnaeus, 1758",
                                "date_created": "2024-11-17T00:37:27.071000Z",
                                "date_modified": "2024-11-17T00:37:27.071000Z"
                            }
                        }
                    }
                }
            },
            ...
        ]
    }

Species
-------

``api/v2/species/``
*******************

This endpoint returns all of the species for which I have representatives in the collection
(whether dead specimens or live insect photographs).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/species/

Response:

.. code::

    {
        "meta": {
            "total_count": 314
        },
        "items": [
            {
                "id": 2,
                "name": "smintheus",
                "binomial": "Parnassius smintheus",
                "common_name": "Rocky Mountain Parnassian",
                "authority": "Doubleday, 1847",
                "mona": "4155.2",
                "p3": null,
                "ps": "77a0351",
                "date_created": "2024-11-17T18:50:47.233000Z",
                "date_modified": "2025-07-20T05:13:25.764000Z",
                "genus": 1
            },
            ...
        ]
    }

``api/v2/nested-species/``
**************************

The regular ``api/v2/species/`` endpoint only returns the ``id`` for the ``genus`` to which the
species belongs. With the ``api/v2/nested-species/`` endpoint, all of the higher-level taxon objects
are returned as well (for species, this includes the genus, tribe, subfamily, family, and order
objects).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-species/

Response:

.. code::

    {
        "meta": {
            "total_count": 314
        },
        "items": [
            {
                "id": 2,
                "name": "smintheus",
                "binomial": "Parnassius smintheus",
                "common_name": "Rocky Mountain Parnassian",
                "authority": "Doubleday, 1847",
                "mona": "4155.2",
                "p3": null,
                "ps": "77a0351",
                "date_created": "2024-11-17T18:50:47.233000Z",
                "date_modified": "2025-07-20T05:13:25.764000Z",
                "genus": {
                    "id": 1,
                    "name": "Parnassius",
                    "common_name": "Parnassians",
                    "authority": "Latreille, 1804",
                    "date_created": "2024-11-17T15:39:09.086000Z",
                    "date_modified": "2025-07-20T05:11:33.574000Z",
                    "tribe": {
                        "id": 1,
                        "name": "Parnassiini",
                        "common_name": "Parnassians",
                        "authority": "Duponchel, [1835]",
                        "date_created": "2024-11-17T02:50:05.119000Z",
                        "date_modified": "2025-07-20T05:11:23.848000Z",
                        "subfamily": {
                            "id": 1,
                            "name": "Parnassiinae",
                            "common_name": "Parnassians and Apollos",
                            "authority": "Duponchel, [1835]",
                            "date_created": "2024-11-17T01:09:17.669000Z",
                            "date_modified": "2025-07-20T05:11:21.364000Z",
                            "family": {
                                "id": 1,
                                "name": "Papilionidae",
                                "common_name": "Swallowtails and Parnassians",
                                "authority": "Latreille, [1802]",
                                "date_created": "2024-11-17T00:37:47.482000Z",
                                "date_modified": "2025-07-20T04:56:11.176000Z",
                                "order": {
                                    "id": 1,
                                    "name": "Lepidoptera",
                                    "common_name": "Butterflies and Moths",
                                    "authority": "Linnaeus, 1758",
                                    "date_created": "2024-11-17T00:37:27.071000Z",
                                    "date_modified": "2024-11-17T00:37:27.071000Z"
                                }
                            }
                        }
                    }
                }
            },
            ...
        ]
    }

Subspecies
----------

``api/v2/subspecies/``
**********************

This endpoint returns all of the subspecies for which I have representatives in the collection
(whether dead specimens or live insect photographs).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/subspecies/

Response:

.. code::

    {
        "meta": {
            "total_count": 3
        },
        "items": [
            {
                "id": 1,
                "name": "rudkini",
                "trinomial": "Papilio polyxenes rudkini",
                "common_name": "Desert Black Swallowtail",
                "authority": "Comstock, 1935",
                "mona": "4161",
                "p3": "770301",
                "ps": "77a0366",
                "date_created": "2024-11-23T22:18:38.449000Z",
                "date_modified": "2025-01-14T01:45:46.802000Z",
                "species": 3
            },
            ...
        ]
    }

``api/v2/nested-subspecies/``
*****************************

The regular ``api/v2/subspecies/`` endpoint only returns the ``id`` for the ``species`` to which
the subspecies belongs. With the ``api/v2/nested-subspecies/`` endpoint, all of the higher-level
taxon objects are returned as well (for subspecies, this includes the species, genus, tribe,
subfamily, family, and order objects).

Example GET request (using ``curl``):

.. code::

    curl https://api.memcollection.com/api/v2/nested-subspecies/

Response:

.. code::

    {
        "meta": {
            "total_count": 3
        },
        "items": [
            {
                "id": 1,
                "name": "rudkini",
                "trinomial": "Papilio polyxenes rudkini",
                "common_name": "Desert Black Swallowtail",
                "authority": "Comstock, 1935",
                "mona": "4161",
                "p3": "770301",
                "ps": "77a0366",
                "date_created": "2024-11-23T22:18:38.449000Z",
                "date_modified": "2025-01-14T01:45:46.802000Z",
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
                    "genus": {
                        "id": 2,
                        "name": "Papilio",
                        "common_name": "Swallowtails",
                        "authority": "Linnaeus, 1758",
                        "date_created": "2024-11-17T18:43:10.815000Z",
                        "date_modified": "2025-07-20T04:56:26.544000Z",
                        "tribe": {
                            "id": 2,
                            "name": "Papilionini",
                            "common_name": "Swallowtails",
                            "authority": "Latreille, [1802]",
                            "date_created": "2024-11-17T18:42:29.528000Z",
                            "date_modified": "2025-07-20T04:56:17.421000Z",
                            "subfamily": {
                                "id": 2,
                                "name": "Papilioninae",
                                "common_name": "Swallowtails",
                                "authority": "Latreille, [1802]",
                                "date_created": "2024-11-17T18:41:30.119000Z",
                                "date_modified": "2025-07-20T04:56:14.052000Z",
                                "family": {
                                    "id": 1,
                                    "name": "Papilionidae",
                                    "common_name": "Swallowtails and Parnassians",
                                    "authority": "Latreille, [1802]",
                                    "date_created": "2024-11-17T00:37:47.482000Z",
                                    "date_modified": "2025-07-20T04:56:11.176000Z",
                                    "order": {
                                        "id": 1,
                                        "name": "Lepidoptera",
                                        "common_name": "Butterflies and Moths",
                                        "authority": "Linnaeus, 1758",
                                        "date_created": "2024-11-17T00:37:27.071000Z",
                                        "date_modified": "2024-11-17T00:37:27.071000Z"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            ...
        ]
    }