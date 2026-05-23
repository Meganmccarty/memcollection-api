from wagtail.api.v2.views import BaseAPIViewSet

from core.utils.helpers import get_fields
from geography.models import CollectingTrip, County, Country, GPS, Locality, State
from geography.serializers import (
    CollectingTripSerializer,
    CountySerializer,
    CountrySerializer,
    GPSSerializer,
    LocalitySerializer,
    NestedCountySerializer,
    NestedGPSSerializer,
    NestedLocalitySerializer,
    NestedStateSerializer,
    StateSerializer,
)


class CountriesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the Country model using the CountrySerializer."""

    base_serializer_class = CountrySerializer
    model = Country
    queryset = Country.objects.all()
    body_fields = get_fields(CountrySerializer)
    listing_default_fields = get_fields(CountrySerializer)


class StatesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the State model using the StateSerializer."""

    base_serializer_class = StateSerializer
    model = State
    queryset = State.objects.select_related("country").all()
    body_fields = get_fields(StateSerializer)
    listing_default_fields = get_fields(StateSerializer)


class CountiesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the County model using the CountySerializer."""

    base_serializer_class = CountySerializer
    model = County
    queryset = County.objects.select_related("state").select_related("country").all()
    body_fields = get_fields(CountySerializer)
    listing_default_fields = get_fields(CountySerializer)


class LocalitiesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the Locality model using the LocalitySerializer."""

    base_serializer_class = LocalitySerializer
    model = Locality
    queryset = (
        Locality.objects.select_related("county")
        .select_related("state")
        .select_related("country")
        .all()
    )
    body_fields = get_fields(LocalitySerializer)
    listing_default_fields = get_fields(LocalitySerializer)


class GPSAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the GPS model using the GPSSerializer."""

    base_serializer_class = GPSSerializer
    model = GPS
    queryset = (
        GPS.objects.select_related("locality")
        .select_related("county")
        .select_related("state")
        .select_related("country")
        .all()
    )
    body_fields = get_fields(GPSSerializer)
    listing_default_fields = get_fields(GPSSerializer)


class CollectingTripsAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the CollectingTrip model using the CollectingTripSerializer."""

    base_serializer_class = CollectingTripSerializer
    model = CollectingTrip
    queryset = CollectingTrip.objects.prefetch_related("states").all()
    body_fields = get_fields(CollectingTripSerializer)
    listing_default_fields = get_fields(CollectingTripSerializer)


class NestedStatesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the State model using the NestedStateSerializer."""

    base_serializer_class = NestedStateSerializer
    model = State
    queryset = State.objects.select_related("country").all()
    body_fields = get_fields(NestedStateSerializer)
    listing_default_fields = get_fields(NestedStateSerializer)


class NestedCountiesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the County model using the NestedCountySerializer."""

    base_serializer_class = NestedCountySerializer
    model = County
    queryset = County.objects.select_related("state").select_related("country").all()
    body_fields = get_fields(NestedCountySerializer)
    listing_default_fields = get_fields(NestedCountySerializer)


class NestedLocalitiesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the Locality model using the NestedLocalitySerializer."""

    base_serializer_class = NestedLocalitySerializer
    model = Locality
    queryset = (
        Locality.objects.select_related("county")
        .select_related("state")
        .select_related("country")
        .all()
    )
    body_fields = get_fields(NestedLocalitySerializer)
    listing_default_fields = get_fields(NestedLocalitySerializer)


class NestedGPSAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the GPS model using the NestedGPSSerializer."""

    base_serializer_class = NestedGPSSerializer
    model = GPS
    queryset = (
        GPS.objects.select_related("locality")
        .select_related("county")
        .select_related("state")
        .select_related("country")
        .all()
    )
    body_fields = get_fields(NestedGPSSerializer)
    listing_default_fields = get_fields(NestedGPSSerializer)
