import datetime
import qrcode

from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from io import BytesIO
from wagtail.fields import RichTextField
from wagtail.search import index

from core.models import TimeStampMixin
from core.utils.insect_attributes import Sex, Stage
from geography.models import CollectingTrip, Country, County, GPS, Locality, State
from taxonomy.models import Genus, Family, Order, Species, Subfamily, Subspecies, Tribe


class Person(index.Indexed, TimeStampMixin):
    """A model that represents a Person object.

    Attributes:
        first_name (str): The person's first name.
        middle_initial (str): The person's middle initial.
        last_name (str): The person's last name.
        suffix (str): The person's suffix (if they have one).
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    first_name = models.CharField(
        max_length=50,
        help_text="Enter the person's first name (or first initial if their full first name is \
            unknown)",
    )
    middle_initial = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        help_text="Enter the person's middle initial, if they have one or if it is known",
    )
    last_name = models.CharField(
        max_length=50, help_text="Enter the person's last name"
    )
    suffix = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        help_text="Enter the person's suffix, if they have one",
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name_plural = "People"

    def __str__(self):
        """Returns a string representation of a Person object instance.

        Returns:
            A string that refers to a Person object instance.
        """

        return self.full_name

    @property
    def collector_name(self):
        """A person's name formatted for a specimen label.

        The format is a person's first initial, middle initial (if they have one), last name, and
        suffix (if they have one).
        """

        first_initial = self.first_name[0]
        middle_initial = f"{self.middle_initial}." if self.middle_initial else ""
        suffix = f" {self.suffix}" if self.suffix else ""
        return f"{first_initial}.{middle_initial} {self.last_name}{suffix}"

    @property
    def full_name(self):
        """A person's full name.

        The format is a person's first name, middle initial (if one is provided), last name, and
        suffix (if they have one).
        """

        middle_initial = f" {self.middle_initial}." if self.middle_initial else ""
        suffix = f", {self.suffix}" if self.suffix else ""
        return f"{self.first_name}{middle_initial} {self.last_name}{suffix}"

    search_fields = [
        index.AutocompleteField("__str__"),
    ]


class SpecimenRecord(TimeStampMixin):
    """A model for a SpecimenRecord object.

    This model has a TON of fields on it, as it's important to have detailed data for specimens in
    a collection. These details include the specimen's taxonomy, its preparation, its locality, and
    the conditions under which it was captured.

    Attributes:
        usi (str): The Unique Specimen Identifier (USI) number. I am setting it as my initials \
                   followed by a dash and a number (which I increment with each specimen added to \
                   the collection).
        order (Order): The order to which the specimen belongs.
        family (Family): The family to which the specimen belongs.
        subfamily (Subfamily): The subfamily to which the specimen belongs.
        tribe (Tribe): The tribe to which the specimen belongs.
        genus (Genus): The genus to which the specimen belongs.
        species (Species): The species to which the specimen belongs.
        subspecies (Subspecies): The subspecies to which the specimen belongs, if the species has \
                                 one.
        determiner (Person): The person who determined (identified) the specimen.
        determined_year (int): The year the determination was made.
        sex (str): The sex of the specimen.
        stage (str): The stage of the specimen.
        preparer (Person): The person who prepared the specimen.
        preparation (str): The preparation type of the specimen.
        preparation_date (date): The date the specimen was prepared.
        labels_printed (bool): Whether labels have been printed for the specimen.
        labeled (bool): Whether the specimen has been labeled.
        photographed (bool): Whether the specimen has been photographed.
        collecting_trip (CollectingTrip): The collecting trip on which the specimen was collected.
        country (Country): The country in which the specimen was collected.
        state (State): The state in which the specimen was collected.
        county (County): The county in which the specimen was collected.
        locality (Locality): The locality at which the specimen was collected.
        gps (GPS): The GPS coordinates at which the specimen was collected.
        day (int): The day on which the specimen was collected.
        month (str): The month in which the specimen was collected.
        year (int): The year in which the specimen was collected.
        collector (Person): The collector(s) who collected the specimen.
        method (str): The method used to collect the specimen.
        weather (str): A brief description of the weather conditions during the specimen's capture.
        temperature (str): The outdoor temperature (in Fahrenheit) during the specimen's capture. \
                           It is a string rather than a float so that I have control on whether or \
                           not a decimal point on the field is serialized.
        time_of_day (str): The time of day (or night) the specimen was captured.
        habitat (str): The habitat details of where the specimen was captured.
        notes (str): Any additional notes about the specimen.
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    # MEM number
    usi = models.CharField(
        max_length=15,
        verbose_name="Unique Specimen Identifier",
        help_text="Enter the specimen's unique identifier number",
        unique=True,
    )

    # Taxonomy fields
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        help_text="Select the specimen's order (if known)",
    )
    family = models.ForeignKey(
        Family,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        help_text="Select the specimen's family (if known)",
    )
    subfamily = models.ForeignKey(
        Subfamily,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        help_text="Select the specimen's subfamily (if known)",
    )
    tribe = models.ForeignKey(
        Tribe,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        help_text="Select the specimen's tribe (if known)",
    )
    genus = models.ForeignKey(
        Genus,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        help_text="Select the specimen's genus (if known)",
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        help_text="Select the specimen's species (if known)",
    )
    subspecies = models.ForeignKey(
        Subspecies,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        help_text="Select the specimen's subspecies (if known)",
    )

    # Specimen details
    class PreparationType(models.TextChoices):
        SPREAD = "spread", "spread"
        PINNED = "pinned", "pinned"
        MINUTEN = "minuten", "minuten"
        POINTED = "pointed", "pointed"
        ENVELOPE = "envelope", "envelope"
        CONTAINER = "container", "container"
        ALCOHOL = "alcohol", "alcohol"

    # Specimen fields
    determiner = models.ForeignKey(
        Person,
        on_delete=models.RESTRICT,
        related_name="specimen_determiners",
        null=True,
        blank=True,
        help_text="Select the person who determined the specimen",
    )
    determined_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(2005), MaxValueValidator(2100)],
        help_text="Enter the year the determination was made",
    )
    sex = models.CharField(
        max_length=10,
        choices=Sex.choices,
        default=Sex.UNKNOWN,
        help_text="Select the specimen's sex",
    )
    stage = models.CharField(
        max_length=10,
        choices=Stage.choices,
        default=Stage.ADULT,
        help_text="Select the specimen's stage",
    )
    preparer = models.ForeignKey(
        Person,
        on_delete=models.RESTRICT,
        related_name="specimen_preparers",
        null=True,
        help_text="Select the person who prepared the specimen",
    )
    preparation = models.CharField(
        max_length=15,
        choices=PreparationType.choices,
        default=PreparationType.SPREAD,
        help_text="Select the specimen's preparation type",
    )
    preparation_date = models.DateField(
        null=True, blank=True, help_text="Enter the preparation date"
    )
    labels_printed = models.BooleanField(
        null=True, help_text="Are labels printed for the specimen?"
    )
    labeled = models.BooleanField(null=True, help_text="Is the specimen labeled?")
    photographed = models.BooleanField(
        null=True, help_text="Is the specimen photographed?"
    )

    # Geography fields
    collecting_trip = models.ForeignKey(
        CollectingTrip,
        on_delete=models.RESTRICT,
        related_name="specimen_records",
        null=True,
        blank=True,
        help_text="Select the collecting trip on which the specimen was collected",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name="specimen_records",
        null=True,
        blank=True,
        help_text="Select the country in which the specimen was collected",
    )
    state = models.ForeignKey(
        State,
        on_delete=models.RESTRICT,
        related_name="specimen_records",
        null=True,
        blank=True,
        help_text="Select the state in which the specimen was collected",
    )
    county = models.ForeignKey(
        County,
        on_delete=models.RESTRICT,
        related_name="specimen_records",
        null=True,
        blank=True,
        help_text="Select the county in which the specimen was collected",
    )
    locality = models.ForeignKey(
        Locality,
        on_delete=models.RESTRICT,
        related_name="specimen_records",
        null=True,
        blank=True,
        help_text="Select the locality at which the specimen was collected",
    )
    gps = models.ForeignKey(
        GPS,
        on_delete=models.RESTRICT,
        related_name="specimen_records",
        null=True,
        blank=True,
        help_text="Select the GPS coordinates at which the specimen was collected",
    )

    # Other fields
    class Month(models.TextChoices):
        JAN = "January", "January"
        FEB = "February", "February"
        MAR = "March", "March"
        APR = "April", "April"
        MAY = "May", "May"
        JUN = "June", "June"
        JUL = "July", "July"
        AUG = "August", "August"
        SEP = "September", "September"
        OCT = "October", "October"
        NOV = "November", "November"
        DEC = "December", "December"

    class Method(models.TextChoices):
        NET = "Net", "Net"
        REARED = "Reared", "Reared"
        TRAP = "Trap", "Trap"
        UV_TRAP = "UV trap", "UV trap"
        LIGHT = "Light", "Light"
        LED_LIGHT = "LED light", "LED light"
        LED_LIGHT_SHEET = "LED light sheet", "LED light sheet"
        MV_LIGHT = "MV light", "MV light"
        MV_LIGHT_SHEET = "MV light sheet", "MV light sheet"
        UV_LIGHT = "UV light", "UV light"
        UV_LIGHT_SHEET = "UV light sheet", "UV light sheet"
        UV_MV_LIGHT_SHEET = "UV/MV light sheet", "UV/MV light sheet"
        UV_MV_LED_LIGHT_SHEET = "UV/MV/LED light sheet", "UV/MV/LED light sheet"
        BAIT = "Bait", "Bait"
        BY_HAND = "By hand", "By hand"
        SWEEP = "Sweep", "Sweep"

    day = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        help_text="Enter the day the specimen was collected, if known",
    )
    month = models.CharField(
        max_length=10,
        choices=Month.choices,
        default="",
        blank=True,
        help_text="Select the month the specimen was collected, if known",
    )
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(2005), MaxValueValidator(2100)],
        help_text="Enter the year the specimen was collected, if known",
    )
    collector = models.ManyToManyField(
        Person,
        verbose_name="Collector(s)",
        related_name="specimen_collectors",
        help_text="Select the specimen's collector(s)",
    )
    method = models.CharField(
        max_length=50,
        choices=Method.choices,
        default="",
        blank=True,
        help_text="Select the method used to collected the specimen",
    )
    weather = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Enter the weather conditions during the specimen's collection",
    )
    temperature = models.CharField(
        max_length=10,
        default="",
        blank=True,
        help_text="Enter the temperature (F) during the specimen's collection if outdoors",
    )
    time_of_day = models.CharField(
        max_length=50,
        default="",
        blank=True,
        help_text="Enter the approximate time of the specimen's collection",
    )
    habitat = RichTextField(
        default="",
        blank=True,
        help_text="Enter habitat details where the specimen was collected",
    )
    notes = RichTextField(
        default="", blank=True, help_text="Enter any other notes about the specimen"
    )

    # QR code fields for barcoding and data preservation
    short_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    class Meta:
        ordering = ["usi"]

    def __str__(self):
        """Returns a string representation of a SpecimenRecord object instance.

        Returns:
            A string that refers to a SpecimenRecord object instance.
        """
        return self.usi

    def generate_short_code(self):
        """Generates a short code for a specimen that can be used in a shortened URL.

        Example: MEM-000001 -> mem000001
        """

        self.short_code = self.usi.lower().replace("-", "")

    def generate_qr_code(self):
        """Generates a QR code for a specimen that, when scanned with a smart phone's camera,
        will take the user to the frontend page for that specimen."""

        self.generate_short_code()

        short_url = f"api.memcollection.com/{self.short_code}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(short_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_io = BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)

        filename = f"qr_{self.usi.lower()}.png"
        self.qr_code.save(filename, ContentFile(img_io.read()), save=False)

    @property
    def identified(self):
        """A boolean representing whether or not a specimen is identified to species."""

        if self.species:
            return True
        else:
            return False

    @property
    def collected_date(self):
        """The collected date used for specimen labels.

        Because the day, month, and year fields are optional, these fields must be checked. Fields
        with non-null values are used to construct the final formatted date.

        Examples of possible dates include "1-Jan-2000", "Jan 2000", and "2000".
        """

        if self.day:
            return f"{self.day}-{self.month[0:3]}-{self.year}"
        elif self.month:
            return f"{self.month[0:3]} {self.year}"
        else:
            return f"{self.year}"

    @property
    def full_date(self):
        """The full date on which a specimen was collected.

        Because the day, month, and year fields are optional, these fields must be checked. Fields
        with non-null values are used to construct the final formatted date.

        Examples of possible dates include "1 January 2000", "January 2000", and "2000".
        """

        if self.day:
            return f"{self.day} {self.month} {self.year}"
        elif self.month:
            return f"{self.month} {self.year}"
        else:
            return f"{self.year}"

    @property
    def num_date(self):
        """The date on which a specimen was collected, formatted as YYYY-MM-DD.

        Because the day, month, and year fields are optional, these fields must be checked. Fields
        with non-null values are used to construct the final numerical date.
        """

        month = self.month

        # If the month field is not empty, convert it to a number
        if month:
            datetime_object = datetime.datetime.strptime(month, "%B")
            if datetime_object.month < 10:
                month = f"0{datetime_object.month}"
            else:
                month = f"{datetime_object.month}"

        if self.day:
            # If the day field is not empty, add a leading zero if the day is 0-9
            if self.day < 10:
                return f"{self.year}-{month}-0{self.day}"
            else:
                return f"{self.year}-{month}-{self.day}"
        elif month:
            return f"{self.year}-{month}"
        else:
            return f"{self.year}"

    @property
    def collectors(self):
        """All collector names for a given specimen joined into a string."""

        return ", ".join(
            [str(collector.collector_name) for collector in self.collector.all()]
        )

    DEGREE_SIGN = "\N{DEGREE SIGN}"

    @property
    def temp_F(self):
        """Temperature with "F" (Fahrenheit) appended to the end."""

        if self.temperature:
            # When putting the initial temperature in as Fahrenheit, I don't usually put a decimal,
            # but converting to a float will automatically add a decimal to a number (which throws
            # off the significant digits). So, after converting the temperature to a float, we need
            # to check and see if the last digit is a non-zero. If it is, it's significant, but if
            # it's not, then we need to drop it.
            temp_float = float(self.temperature)
            temp_float_to_string = str(temp_float)
            last_digit_string = temp_float_to_string.split(".")[1]
            last_digit = int(last_digit_string)
            if last_digit == 0:
                temp_float = int(temp_float_to_string.split(".")[0])
            return f"{round(temp_float, 1)}{self.DEGREE_SIGN}F"
        else:
            return ""

    @property
    def temp_C(self):
        """Temperature with "C" (Celsius) appended to the end."""

        if self.temperature:
            temp_float = float(self.temperature)
            celsius = (temp_float - 32) * 5 / 9
            return f"{round(celsius, 1)}{self.DEGREE_SIGN}C"
        else:
            return ""
