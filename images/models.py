from django.db import models
from wagtail.fields import RichTextField
from wagtail.images.models import AbstractImage, AbstractRendition, Image

from core.models import TimeStampMixin
from core.utils.insect_attributes import Sex, Stage
from geography.models import CollectingTrip, Country, County, GPS, Locality, State
from pages.models import SpeciesPage
from specimens.models import SpecimenRecord
from taxonomy.models import Species


class CustomImage(AbstractImage, TimeStampMixin):
    """A model that represents a custom image object.

    Because this model inherits from Wagtail's AbstractImage, it has additional fields (like
    title and description). For the purposes of this project, the title will be used as the
    image's name, and the description will be used like a caption field.

    Attributes:
        alt_text (str): The alternative text of the image.
        date (date): The date the image was taken.
        notes (str): Any additional notes that may be included with the image.
    """

    alt_text = models.CharField(max_length=255, blank=True)
    date = models.DateField(help_text="Enter the date the image was taken")
    notes = RichTextField(blank=True)

    admin_form_fields = Image.admin_form_fields + ("alt_text", "date", "notes")

    # The properties below are for creating image renditions (different sizes of the same image)
    # The original version of the image is already taken into account in the default image fields
    # above

    @property
    def x_large(self):
        """The largest version of an image (either a max of 2000px wide or 2000px tall)."""

        return self.get_rendition("max-2000x2000")

    @property
    def large(self):
        """A large version of an image (either a max of 1500px wide or 1500px tall)."""

        return self.get_rendition("max-1500x1500")

    @property
    def medium(self):
        """A medium version of an image (either a max of 1200px wide or 1200px tall)."""

        return self.get_rendition("max-1200x1200")

    @property
    def small(self):
        """A small version of an image (either a max of 900px wide or 900px tall)."""

        return self.get_rendition("max-900x900")

    @property
    def x_small(self):
        """An extra small version of an image (either a max of 600px wide or 600px tall)."""

        return self.get_rendition("max-600x600")

    @property
    def thumbnail(self):
        """A thumbnail version of an image (either a max of 300px wide or 300px tall)."""

        return self.get_rendition("max-300x300")


class CustomRendition(AbstractRendition, TimeStampMixin):
    """A model that represents a custom rendition object.

    Attributes:
        image (CustomImage): The image to which this rendition belongs.
    """

    image = models.ForeignKey(
        CustomImage, on_delete=models.RESTRICT, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class BaseLiveImage(CustomImage):
    """A model that represents a live subject (insect, plant, or habitat).

    It inherits from CustomImage, so it has all of the same attributes as that model (and more
    below).

    Attributes:
        country (Country): The country in which the image was taken.
        state (State): The state (or province) in which the image was taken.
        county (County): The county (or parish or census area) in which the image was taken.
        locality (Locality): The locality at which the image was taken.
        gps (GPS): The GPS coordinates at which the image was taken.
        collecting_trip (CollectingTrip): The collecting trip during which the image was taken.
    """

    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name="%(class)s",
        null=True,
        blank=True,
        help_text="Select the country in which the image was taken",
    )
    state = models.ForeignKey(
        State,
        on_delete=models.RESTRICT,
        related_name="%(class)s",
        null=True,
        blank=True,
        help_text="Select the state in which the image was taken",
    )
    county = models.ForeignKey(
        County,
        on_delete=models.RESTRICT,
        related_name="%(class)s",
        null=True,
        blank=True,
        help_text="Select the county in which the image was taken",
    )
    locality = models.ForeignKey(
        Locality,
        on_delete=models.RESTRICT,
        related_name="%(class)s",
        null=True,
        blank=True,
        help_text="Select the locality at which the image was taken",
    )
    gps = models.ForeignKey(
        GPS,
        on_delete=models.RESTRICT,
        related_name="%(class)s",
        null=True,
        blank=True,
        help_text="Select the GPS coordinates at which the image was taken",
    )
    collecting_trip = models.ForeignKey(
        CollectingTrip,
        on_delete=models.RESTRICT,
        related_name="%(class)s",
        null=True,
        blank=True,
        help_text="Select the collecting trip during which the image was taken",
    )


class SpecimenRecordImage(CustomImage):
    """A model that represents a specimen record image object.

    This image model is only for photographs of specimens in the collection, and not live insects.

    Attributes:
        usi (SpecimenRecord): The specimen record to which this image belongs.
        position (str): The position of the specimen in the image (dorsal, ventral, or lateral).
    """

    usi = models.ForeignKey(
        SpecimenRecord,
        on_delete=models.RESTRICT,
        related_name="specimen_images",
        help_text="Select the specimen in the image",
    )

    class Position(models.TextChoices):
        DORSAL = "dorsal", "dorsal"
        VENTRAL = "ventral", "ventral"
        LATERAL = "lateral", "lateral"

    position = models.CharField(
        max_length=10,
        choices=Position.choices,
        default=Position.DORSAL,
        help_text="Select the view of the specimen in the image",
    )


class InsectImage(BaseLiveImage):
    """A model that represents an insect image object.

    This image model is only for photographs of live insects (either in the wild or captivity) and
    not for specimens in the collection.

    Attributes:
        species (Species): The species of insect in the image (if known).
        species_page (SpeciesPage): The species page to which this image should be attached (if \
                                    the insect in the photo is identified).
        featured_family (bool): Indicates whether the image should be the one featured for the \
                                insect's family (if the insect is identified).
        featured_species (bool): Indicates whether the image should be the one featured for the \
                                 insect's species (if the insect is identified).
        sex (str): The sex of the insect in the image, if known.
        stage (str): The stage of the insect in the image.
        status (str): The status of the insect in the image (wild, reared, or bred).
    """

    species = models.ForeignKey(
        Species,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="insect_images",
        help_text="Select the species in the image, if it is identified",
    )
    species_page = models.ForeignKey(
        SpeciesPage,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="insect_images",
        help_text="Select the species page to which this image belongs, if the insect in the image \
                  is identified",
    )
    featured_family = models.BooleanField(
        default=False,
        help_text="Toggle to make this image represent the family to which the insect in the image \
                  belongs",
    )
    featured_species = models.BooleanField(
        default=False,
        help_text="Toggle to make this image represent the species to which the insect in the \
                  image belongs",
    )

    class Status(models.TextChoices):
        WILD = "wild", "wild"
        REARED = "reared", "reared"
        BRED = "bred", "bred"

    sex = models.CharField(
        max_length=10,
        choices=Sex.choices,
        default=Sex.UNKNOWN,
        help_text="Select the insect's sex",
    )
    stage = models.CharField(
        max_length=10,
        choices=Stage.choices,
        default=Stage.ADULT,
        help_text="Select the insect's stage",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.WILD,
        help_text="Select the status of the insect in the image",
    )

    @property
    def identified(self):
        """A boolean representing whether the insect in the image is identified to species."""

        if self.species and self.species_page:
            return True
        else:
            return False

    @property
    def family(self):
        """The name of the family to which the insect in the image belongs."""

        return self.species.genus.tribe.subfamily.family.name

    @property
    def species_binomial(self):
        """The binomial of the species to which the insect in the image belongs."""

        return self.species.binomial


class PlantImage(BaseLiveImage):
    """A model that represents a plant image object.

    Attributes:
        species_page (SpeciesPage): The species page(s) to which this image should be attached.
        scientific_name (str): The scientific name of the plant in the image, if known.
        common_name (str): The common name of the plant in the image, if known or if it has one.
    """

    species_page = models.ManyToManyField(
        SpeciesPage,
        related_name="plant_images",
        help_text="Select the species pages(s) to which this plant image should belong",
    )
    scientific_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Enter the scientific name of the plant, if known",
    )
    common_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Enter the common name of the plant, if known",
    )


class HabitatImage(BaseLiveImage):
    """A model that represents a habitat image object.

    Attributes:
        species_page (SpeciesPage): The species page(s) to which this image should be attached.
    """

    species_page = models.ManyToManyField(
        SpeciesPage,
        related_name="habitat_images",
        help_text="Select the species page(s) to which this habitat image should belong",
    )
