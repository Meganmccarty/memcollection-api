Models
======

.. autoclass:: geography.models.Country

    .. automethod:: __str__

.. autoclass:: geography.models.State

    .. automethod:: __str__

.. autoclass:: geography.models.County

    .. autoattribute:: abbr
    .. autoattribute:: county_line
    .. autoattribute:: full_name
    .. automethod:: __str__

.. autoclass:: geography.models.Locality

    .. automethod:: __str__
    .. automethod:: clean

.. autoclass:: geography.models.GPS

    .. automethod:: __str__
    .. autoattribute:: elevation_meters

.. autoclass:: geography.models.CollectingTrip

    .. automethod:: __str__
    .. autoattribute:: slug
