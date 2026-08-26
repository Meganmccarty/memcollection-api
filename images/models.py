from django.core.exceptions import ValidationError
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

    class ImageType(models.TextChoices):
        SPECIMEN = "specimen", "Specimen Record"
        INSECT = "insect", "Insect"
        PLANT = "plant", "Plant"
        HABITAT = "habitat", "Habitat"

    alt_text = models.CharField(max_length=255, blank=True)
    date = models.DateField(help_text="Enter the date the image was taken")
    notes = RichTextField(blank=True)
    image_type = models.CharField(
        max_length=20,
        choices=ImageType.choices,
        help_text="Select the type of image",
        default=ImageType.SPECIMEN,
    )

    # Geography fields (for live images: insect, plant, habitat)
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="custom_images",
        help_text="Select the country in which the image was taken, if known",
    )
    state = models.ForeignKey(
        State,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="custom_images",
        help_text="Select the state in which the image was taken, if known",
    )
    county = models.ForeignKey(
        County,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="custom_images",
        help_text="Select the county in which the image was taken, if known",
    )
    locality = models.ForeignKey(
        Locality,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="custom_images",
        help_text="Select the locality at which the image was taken, if known",
    )
    gps = models.ForeignKey(
        GPS,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="custom_images",
        help_text="Select the GPS coordinates at which the image was taken, if known",
    )
    collecting_trip = models.ForeignKey(
        CollectingTrip,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="custom_images",
        help_text="Select the collecting trip during which the image was taken, if it was taken \
                   during one",
    )

    # Specimen-specific fields
    specimen_record = models.ForeignKey(
        SpecimenRecord,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="images",
        help_text="Select the specimen record to which this image belongs",
    )

    class Position(models.TextChoices):
        DORSAL = "dorsal", "Dorsal"
        VENTRAL = "ventral", "Ventral"
        LATERAL = "lateral", "Lateral"

    position = models.CharField(
        max_length=10,
        choices=Position.choices,
        blank=True,
        help_text="Select the position in which the specimen was taken",
    )

    # Insect-specific fields
    species = models.ForeignKey(
        Species,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="insect_images",
        help_text="Select the insect species in the image",
    )
    species_page = models.ForeignKey(
        SpeciesPage,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="insect_images",
        help_text="Select the insect species page to which this image should belong",
    )

    class Status(models.TextChoices):
        WILD = "wild", "Wild"
        REARED = "reared", "Reared"
        BRED = "bred", "Bred"

    sex = models.CharField(
        max_length=10,
        choices=Sex.choices,
        blank=True,
        help_text="Select the sex of the insect in the image, if known",
    )
    stage = models.CharField(
        max_length=10,
        choices=Stage.choices,
        blank=True,
        help_text="Select the stage of the insect in the image",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        blank=True,
        help_text="Select the status of the insect in the image",
    )

    # Plant-specific fields
    scientific_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Enter the scientific name of the plant in the image",
    )
    common_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Enter the common name of the plant in the imagee, if it has one",
    )
    plant_species_page = models.ManyToManyField(
        SpeciesPage,
        blank=True,
        related_name="plant_images",
        help_text="Select the insect species page(s) to which this plant image should belong",
    )

    # Habitat-specific fields
    habitat_species_page = models.ManyToManyField(
        SpeciesPage,
        blank=True,
        related_name="habitat_images",
        help_text="Select the insect species page(s) to which this habitat image should belong",
    )

    admin_form_fields = Image.admin_form_fields + (
        "alt_text",
        "date",
        "notes",
        "image_type",
        "specimen_record",
        "position",
        "species",
        "species_page",
        "sex",
        "stage",
        "status",
        "scientific_name",
        "common_name",
        "plant_species_page",
        "habitat_species_page",
        "country",
        "state",
        "county",
        "locality",
        "gps",
        "collecting_trip",
    )

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

    def clean(self):
        """Validate required fields based on image type."""
        super().clean()

        if self.image_type == self.ImageType.SPECIMEN:
            if not self.specimen_record:
                raise ValidationError(
                    {
                        "specimen_record": "Specimen record is required for specimen images."
                    }
                )
            if not self.position:
                raise ValidationError(
                    {"position": "Position is required for specimen images."}
                )

        elif self.image_type == self.ImageType.INSECT:
            if not self.species:
                raise ValidationError(
                    {"species": "Species is required for insect images."}
                )

        elif self.image_type == self.ImageType.PLANT:
            if not self.scientific_name:
                raise ValidationError("Scientific name is required for plant images.")

    def save(self, *args, **kwargs):
        """Clear fields not relevant to the current image type."""

        if self.image_type != self.ImageType.SPECIMEN:
            self.specimen_record = None
            self.position = ""

        if self.image_type != self.ImageType.INSECT:
            self.species = None
            self.species_page = None
            self.sex = Sex.UNKNOWN
            self.stage = Stage.ADULT
            self.status = self.Status.WILD

        if self.image_type != self.ImageType.PLANT:
            self.scientific_name = ""
            self.common_name = ""
            if self.pk:
                self.plant_species_page.clear()

        if self.image_type != self.ImageType.HABITAT:
            if self.pk:
                self.habitat_species_page.clear()

        if self.image_type == self.ImageType.SPECIMEN:
            self.country = None
            self.state = None
            self.county = None
            self.locality = None
            self.gps = None
            self.collecting_trip = None

        super().save(*args, **kwargs)


class CustomRendition(AbstractRendition, TimeStampMixin):
    """A model that represents a custom rendition object.

    Attributes:
        image (CustomImage): The image to which this rendition belongs.
    """

    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
