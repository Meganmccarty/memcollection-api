from rest_framework import serializers

from images.serializers import CustomImageSerializer
from taxonomy.models import Order, Family, Subfamily, Tribe, Genus, Species, Subspecies


class OrderSerializer(serializers.ModelSerializer):
    """A serializer for the Order model.

    It serializes all of the fields on the Order model, including those inherited from the
    TimeStampMixin."""

    featured_image = CustomImageSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "common_name",
            "authority",
            "date_created",
            "date_modified",
            "featured_image",
        )


class FamilySerializer(serializers.ModelSerializer):
    """A serializer for the Family model.

    It serializes all of the fields on the Family model, including those inherited from the
    TimeStampMixin."""

    featured_image = CustomImageSerializer()

    class Meta:
        model = Family
        fields = (
            "id",
            "name",
            "common_name",
            "authority",
            "date_created",
            "date_modified",
            "order",
            "featured_image",
        )


class SubfamilySerializer(serializers.ModelSerializer):
    """A serializer for the Subfamily model.

    It serializes all of the fields from the Subfamily model, including those inherited from the
    TimeStampMixin."""

    class Meta:
        model = Subfamily
        fields = (
            "id",
            "name",
            "common_name",
            "authority",
            "date_created",
            "date_modified",
            "family",
        )


class TribeSerializer(serializers.ModelSerializer):
    """A serializer for the Tribe model.

    It serializes all of the fields from the Tribe model, including those inherited from the
    TimeStampMixin."""

    class Meta:
        model = Tribe
        fields = (
            "id",
            "name",
            "common_name",
            "authority",
            "date_created",
            "date_modified",
            "subfamily",
        )


class GenusSerializer(serializers.ModelSerializer):
    """A serializer for the Genus model.

    It serializes all of the fields from the Genus model, including those inherited from the
    TimeStampMixin."""

    class Meta:
        model = Genus
        fields = (
            "id",
            "name",
            "common_name",
            "authority",
            "date_created",
            "date_modified",
            "tribe",
        )


class SpeciesSerializer(serializers.ModelSerializer):
    """A serializer for the Species model.

    It serializes all of the fields from the Species model, including those inherited from the
    TimeStampMixin."""

    binomial = serializers.CharField()
    featured_image = CustomImageSerializer()

    class Meta:
        model = Species
        fields = (
            "id",
            "name",
            "binomial",
            "common_name",
            "authority",
            "mona",
            "p3",
            "ps",
            "date_created",
            "date_modified",
            "genus",
            "featured_image",
        )


class SubspeciesSerializer(serializers.ModelSerializer):
    """A serializer for the Subspecies model.

    It serializes all of the fields from the Genus model, including those inherited from the
    TimeStampMixin."""

    trinomial = serializers.CharField()

    class Meta:
        model = Subspecies
        fields = (
            "id",
            "name",
            "trinomial",
            "common_name",
            "authority",
            "mona",
            "p3",
            "ps",
            "date_created",
            "date_modified",
            "species",
        )


class NestedFamilySerializer(FamilySerializer):
    """A serializer for the Family model that includes nested data.

    It extends the FamilySerializer and includes all of the data within the order field using
    the OrderSerializer."""

    order = OrderSerializer()


class NestedSubfamilySerializer(SubfamilySerializer):
    """A serializer for the Subfamily model that includes nested data.

    It extends the SubfamilySerializer and includes all of the data within the family field using
    the NestedFamilySerializer."""

    family = NestedFamilySerializer()


class NestedTribeSerializer(TribeSerializer):
    """A serializer for the Tribe model that includes nested data.

    It extends the TribeSerializer and includes all of the data within the subfamily field using the
    NestedSubfamilySerializer."""

    subfamily = NestedSubfamilySerializer()


class NestedGenusSerializer(GenusSerializer):
    """A serializer for the Genus model that include nested data.

    It extends the GenusSerializer and includes all of the data within the tribe field using the
    NestedTribeSerializer."""

    tribe = NestedTribeSerializer()


class NestedSpeciesSerializer(SpeciesSerializer):
    """A serializer for the Species model that includes nested data.

    It extends the SpeciesSerializer and includes all of the data within the genus field using the
    NestedGenusSerializer"""

    genus = NestedGenusSerializer()


class NestedSubspeciesSerializer(SubspeciesSerializer):
    """A serializer for the Subspecies model that includes nested data.

    It extends the SubspeciesSerializer and includes all of the data within the species field using
    the NestedSpeciesSerializer."""

    species = NestedSpeciesSerializer()
