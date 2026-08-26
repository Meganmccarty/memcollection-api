from rest_framework import serializers

from images.models import CustomImage, CustomRendition


class RenditionsSerializer(serializers.ModelSerializer):
    """A serializer for the CustomRendition model."""

    class Meta:
        model = CustomRendition
        fields = (
            "id",
            "date_created",
            "date_modified",
            "filter_spec",
            "file",
            "width",
            "height",
            "focal_point_key",
            "image",
        )


class CustomImageSerializer(serializers.ModelSerializer):
    """A serializer for the CustomImage model."""

    x_large = RenditionsSerializer()
    large = RenditionsSerializer()
    medium = RenditionsSerializer()
    small = RenditionsSerializer()
    x_small = RenditionsSerializer()
    thumbnail = RenditionsSerializer()

    class Meta:
        model = CustomImage
        fields = "__all__"
