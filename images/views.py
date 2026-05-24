from wagtail.api.v2.views import BaseAPIViewSet

from core.utils.helpers import get_fields
from images.models import HabitatImage, InsectImage, PlantImage, SpecimenRecordImage
from images.serializers import (
    HabitatImageSerializer,
    InsectImageSerializer,
    PlantImageSerializer,
    SpecimenRecordImageSerializer,
)


class SpecimenRecordImagesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the SpecimenRecordImage model using the \
       SpecimenRecordImageSerializer."""

    base_serializer_class = SpecimenRecordImageSerializer
    model = SpecimenRecordImage
    queryset = SpecimenRecordImage.objects.all()
    body_fields = get_fields(SpecimenRecordImageSerializer)
    listing_default_fields = get_fields(SpecimenRecordImageSerializer)


class InsectImagesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the InsectImage model using the InsectImageSerializer."""

    base_serializer_class = InsectImageSerializer
    model = InsectImage
    queryset = InsectImage.objects.all()
    body_fields = get_fields(InsectImageSerializer)
    listing_default_fields = get_fields(InsectImageSerializer)


class PlantImagesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the PlantImage model using the PlantImageSerializer."""

    base_serializer_class = PlantImageSerializer
    model = PlantImage
    queryset = PlantImage.objects.all()
    body_fields = get_fields(PlantImageSerializer)
    listing_default_fields = get_fields(PlantImageSerializer)


class HabitatImagesAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the HabitatImage model using the HabitatImageSerializer."""

    base_serializer_class = HabitatImageSerializer
    model = HabitatImage
    queryset = HabitatImage.objects.all()
    body_fields = get_fields(HabitatImageSerializer)
    listing_default_fields = get_fields(HabitatImageSerializer)
