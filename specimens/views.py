from wagtail.api.v2.views import BaseAPIViewSet

from core.utils.helpers import get_fields
from specimens.filters import SpecimenRecordFilter
from specimens.models import Person, SpecimenRecord
from specimens.serializers import PersonSerializer, SpecimenRecordSerializer


class PeopleAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the Person model using the PersonSerializer."""

    base_serializer_class = PersonSerializer
    model = Person
    queryset = Person.objects.all()
    body_fields = get_fields(PersonSerializer)
    listing_default_fields = get_fields(PersonSerializer)


class SpecimenRecordAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the SpecimenRecord model using the
    SpecimenRecordSerializer."""

    base_serializer_class = SpecimenRecordSerializer
    model = SpecimenRecord
    queryset = SpecimenRecord.objects.all()
    body_fields = get_fields(SpecimenRecordSerializer)
    listing_default_fields = get_fields(SpecimenRecordSerializer)
    filterset_class = SpecimenRecordFilter

    def check_query_parameters(self, query_params):
        """Disables Wagtail's strict query param validation so that
        custom django-filter parameters are allowed."""
        return

    def get_queryset(self):
        queryset = super().get_queryset()

        filterset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
            request=self.request,
        )

        if filterset.is_valid():
            return filterset.qs.distinct()

        return queryset
