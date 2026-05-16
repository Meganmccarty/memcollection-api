from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from wagtail.fields import RichTextField
from wagtail.search import index

from mixins.models import TimeStampMixin


class Country(index.Indexed, TimeStampMixin):
    """A model that represents a Country object.

    Attributes:
        name (str): The full name of the country.
        abbr (str): The country's 3-letter abbreviation.
        date_created (datetime): The date when the object instance was created. Inherited from \
            TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
            from TimeStampMixin.
    """

    name = models.CharField(max_length=50, help_text="Enter the name of the country")
    abbr = models.CharField(
        max_length=3, help_text="Enter the country's 3-letter abbreviation"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Countries"

    def __str__(self):
        """Returns a string representation of a Country object instance.

        Returns:
            A string that refers to a Country object instance.
        """
        return f"{self.name}"

    search_fields = [
        index.AutocompleteField("name"),
        index.AutocompleteField("abbr"),
    ]


class State(index.Indexed, TimeStampMixin):
    """A model that represents a State object.

    Attributes:
        country (Country): The country to which the state belongs.
        name (str): The full name of the state.
        abbr (str): The state's abbreviation (should be 2 letters).
        date_created (datetime): The date when the object instance was created. Inherited from \
            TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
            from TimeStampMixin.
    """

    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name="+",
        help_text="Select the state's country",
    )
    name = models.CharField(
        max_length=50, help_text="Enter the name of the state (or province)"
    )
    abbr = models.CharField(
        max_length=10,
        help_text="Enter the state's (or province's) abbreviation (should be 2 letters)",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """Returns a string representation of a State object instance.

        Returns:
            A string that refers to a State object instance.
        """
        return f"{self.name}"

    search_fields = [
        index.AutocompleteField("name"),
        index.AutocompleteField("abbr"),
    ]


class County(index.Indexed, TimeStampMixin):
    """A model that represents a County object.

    Attributes:
        state (State): The state to which the county belongs.
        name (str): The full name of the county.
        date_created (datetime): The date when the object instance was created. Inherited from \
            TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
            from TimeStampMixin.
    """

    state = models.ForeignKey(
        State,
        on_delete=models.RESTRICT,
        related_name="+",
        help_text="Select the state to which this county (or parish) belongs",
    )
    name = models.CharField(
        max_length=50, help_text="Enter the name of the county (or parish)"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Counties"

    def __str__(self):
        """Returns a string representation of a County object instance.

        It uses both a property of the County object (full_name) as well as the state abbreviation
        to which this County object instance belongs (state.abbr). For example, if the county is
        Switzerland and the state is Indiana, __str__() will return "Switzerland Co., IN".

        Returns:
            A string that refers to a County object instance.
        """
        return f"{self.full_name}, {self.state.abbr}"

    @property
    def abbr(self):
        """The county's abbreviation ('Co.', 'Par.', or 'Boro.').

        Most states in the US are broken up into smaller units called counties, but some states
        call their smaller divisions parishes (Louisiana) or boroughs (Alaska).

        For the purposes of this application, all of the smaller units, regardless of state, will be
        classified as County objects. If the instance of a County object belongs to either the state
        of Louisiana or Alaska, then the correct abbreviation ('Par.' or 'Boro.') will be used
        instead of the default 'Co.'.

        Note: Some Alaskan areas are subdivided into census areas instead of boroughs. For those
        units, no abbreviation will be generated.
        """

        county_abbr = ""

        # Check to see what abbreviation is needed (based on state)
        if self.state.name == "Alaska" and "Census" not in self.name:
            county_abbr = "Boro."
        elif self.state.name == "Alaska" and "Census" in self.name:
            county_abbr = ""
        elif self.state.name == "Louisiana":
            county_abbr = "Par."
        else:
            county_abbr = "Co."

        return county_abbr

    @property
    def county_line(self):
        """The county's border (if two counties are listed within the name field).

        There are cases when a specimen may have been collected on the border between two counties
        (on the county line). This needs to be included on the specimen label by indicating the word
        'line'.
        """

        # If there are two counties listed as one in the name, return the word "line"
        if "/" in self.name:
            return "line"
        else:
            return ""

    @property
    def full_name(self):
        """A county's full name.

        It is formatted as the county's name, abbreviation (if it has one), and the word "line" (if
        there are two counties listed in the name).
        """

        abbr = " " + self.abbr if self.abbr else ""
        line = " " + self.county_line if self.county_line else ""

        return "{}{}{}".format(self.name, abbr, line)

    search_fields = [
        index.AutocompleteField("__str__"),
    ]


class Locality(index.Indexed, TimeStampMixin):
    """A model that represents a Locality object.

    This class contains validation in the Wagtail admin to prevent a user from adding multiple
    regions to the locality. This is a personal preference for how I want the data to be
    structured.

    For example, a locality can belong to a county but not to both a county and a state (because
    the county already belongs to a state). Likewise, a locality can belong to a state (if the
    county is unknown) but not to both a state and a country (because the state already belongs to
    a country).

    Note: All of the fields are optional, as every location will not make use of every field
    available.

    Attributes:
        country (Country): The country to which the locality belongs.
        state (State): The state to which the locality belongs.
        county (County): The county to which the locality belongs.
        name (str): The name of the locality.
        range (str): The distance and direction of the locality from the nearest town.
        town (str): The nearest town to the locality.
        date_created (datetime): The date when the object instance was created. Inherited from \
            TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
            from TimeStampMixin.
    """

    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.RESTRICT, related_name="+"
    )
    state = models.ForeignKey(
        State, null=True, blank=True, on_delete=models.RESTRICT, related_name="+"
    )
    county = models.ForeignKey(
        County, null=True, blank=True, on_delete=models.RESTRICT, related_name="+"
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Enter a locality's name, if it has one",
    )
    range = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Enter the distance and direction of this locality from the nearest town (e.g., \
            2 km NW), if known",
    )
    town = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Enter the nearest town, if known",
    )

    class Meta:
        ordering = ["name", "town"]
        verbose_name_plural = "Localities"

    def __str__(self):
        """Returns a string representation of a Locality object instance.

        Because each field for a Locality object instance is optional, each field must be first
        checked to see if it is null. If not null, then it is included as part of the string
        returned. Else, an empty string is returned in the empty field's place.

        The way this string representation is structured may be a little complex, but it is my
        personal preference to have as much detail as possible when looking through a list of
        localities. I want to be able to see the main fields (name, range, and town) if they are
        not null, and I'd also like to see to which county, state, or country the locality belongs.

        Returns:
            A string that refers to a Locality object instance.
        """

        name = self.name + ", " if self.name else ""
        range = self.range + " " if self.range else ""
        town = self.town + ", " if self.town else ""

        region = ""

        if self.county:
            region = self.county.full_name
        elif self.state:
            region = self.state.abbr
        else:
            region = self.country.abbr

        return "{}{}{}{}".format(name, range, town, region)

    def clean(self):
        """Modifies the default Django clean() method to include some custom validation.

        Because I don't want a locality to belong to more than one region (whether that be county,
        state, or country), a ValidationError will be raised if two or more regions are selected
        for a given Locality object instance.

        Raises:
            Either 2 or 3 validation errors for the county, state, and country fields.
        """

        super().clean()

        errors = {}

        if self.county and self.state and self.country:
            error_text = "You cannot select a county, state, and country together"
            errors["county"] = error_text
            errors["state"] = error_text
            errors["country"] = error_text
        elif self.county and self.state:
            error_text = "You cannot select both a county and a state"
            errors["county"] = error_text
            errors["state"] = error_text
        elif self.county and self.country:
            error_text = "You cannot select both a county and a country"
            errors["county"] = error_text
            errors["country"] = error_text
        elif self.state and self.country:
            error_text = "You cannot select both a state and a country"
            errors["state"] = error_text
            errors["country"] = error_text

        raise ValidationError(errors)

    search_fields = [
        index.AutocompleteField("__str__"),
    ]


class GPS(index.Indexed, TimeStampMixin):
    """A model that represents a GPS object.

    Note: The latitude and longitude fields are optional, as there are cases where elevation or a
    range of elevations are known, but GPS coordinates were not taken.

    Attributes:
        locality (Locality): The locality to which the GPS object instance belongs.
        latitude (str): The latitude part of the GPS coordinates. It is a string rather than a \
            float so that I have control on the exact number of decimal points when the field is \
            serialized.
        longitude (str): The longitude part of the GPS coordinates. It is a string rather than a \
            float so that I have control on the exact number of decimal points when the field is \
            serialized.
        elevation (str): The elevation of the GPS coordinates. It is a string rather than an \
            integer because there are some cases where a range of elevations are provided.
        date_created (datetime): The date when the object instance was created. Inherited from \
            TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
            from TimeStampMixin.
    """

    locality = models.ForeignKey(
        Locality,
        on_delete=models.RESTRICT,
        related_name="+",
        help_text="Select the locality for this set of coordinates",
    )
    latitude = models.CharField(
        null=True,
        blank=True,
        help_text="Enter the latitude in decimal degrees",
    )
    longitude = models.CharField(
        null=True,
        blank=True,
        help_text="Enter the longitude in decimal degrees",
    )
    elevation = models.CharField(
        max_length=15, help_text="Enter the elevation in meters"
    )

    class Meta:
        ordering = ["latitude", "longitude"]
        verbose_name_plural = "GPS coordinates"

    def __str__(self):
        """Returns a string representation of a GPS object instance.

        Because the latitude and longitude fields are optional, each must be checked to see if
        it is null. If not null, then it is included as part of the string returned. Else, an empty
        string is returned in the empty field's place.

        Also included are the GPS object instance's elevation and its locality for easier selection
        in the Wagtail admin.

        Returns:
            A string that refers to a GPS object instance.
        """

        latitude = f"{self.latitude} " if self.latitude else ""
        longitude = f"{self.longitude} " if self.longitude else ""

        return "{}{}{}, {}".format(
            latitude, longitude, self.elevation_meters, self.locality
        )

    @property
    def gps_coordinates(self):
        """A string combining both latitude and longitude."""

        return f"{self.latitude} {self.longitude}"

    @property
    def elevation_meters(self):
        """Adds an "m" (meters) at the end of the elevation field."""

        return f"{self.elevation}m"

    search_fields = [
        index.AutocompleteField("__str__"),
    ]


class CollectingTrip(index.Indexed, TimeStampMixin):
    """A model that represents a CollectingTrip object.

    Attributes:
        name (str): The name of the collecting trip.
        states (State[]): A list of State object instances to which the collecting trip belongs.
        start_date (date): The start date of the trip.
        end_date (date): The end date of the trip.
        notes (str): A rich text field for documenting trip notes.
        date_created (datetime): The date when the object instance was created. Inherited from \
            TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
            from TimeStampMixin.
    """

    name = models.CharField(max_length=50, help_text="Enter a name for the trip")
    states = models.ManyToManyField(
        State,
        related_name="collecting_trips",
        help_text="Select the state(s) visited during the trip (hold down Command to select \
            multiple states)",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    notes = RichTextField(null=True, blank=True, help_text="Enter notes about the trip")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """Returns a string representation of a CollectingTrip object instance.

        Returns:
            A string that refers to a CollectingTrip object instance.
        """
        return self.name

    @property
    def slug(self):
        """Slugifies the name of a CollectingTrip object instance."""

        return slugify(self.name)

    @property
    def joined_states(self):
        """A string representing all of the states collected in during a trip."""

        return ", ".join([str(state) for state in self.states.all()])

    search_fields = [
        index.AutocompleteField("name"),
    ]
