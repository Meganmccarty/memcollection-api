from django.db import models
from wagtail.search import index

from core.models import TimeStampMixin


class TaxonomyBase(index.Indexed, models.Model):
    """An abstract model for a TaxonomyBase object. This model can be used as the foundation for all
    other taxonomy models.

    Attributes:
        name (str): The scientific name of the taxon.
        common_name (str): The common name of the taxon, if it has one.
        authority (str): The authority of the taxon.
    """

    name = models.CharField(
        max_length=100, help_text="Enter the taxon's scientific name"
    )
    common_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Enter the taxon's common name, if it has one",
    )
    authority = models.CharField(
        max_length=100, help_text="Enter the taxon's authority"
    )

    class Meta:
        abstract = True

    def __str__(self):
        """Returns a string representation of a TaxonomyBase object instance.

        Returns:
            A string that refers to a Taxonomy object instance.
        """

        return self.name

    search_fields = [
        index.AutocompleteField("name"),
        index.AutocompleteField("common_name"),
    ]


class Order(TimeStampMixin, TaxonomyBase):
    """A model that represents an Order object.

    Attributes:
        featured_image (CustomImage): The image to represent the order. Used for display on the \
                                      frontend.
        name (str): The scientific name of the taxon. Inherited from TaxonomyBase.
        common_name (str): The common name of the taxon, if it has one. Inherited from TaxonomyBase.
        authority (str): The authority of the taxon. Inherited from TaxonomyBase.
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    featured_image = models.OneToOneField(
        "images.CustomImage",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="+",
        help_text="Select an image to represent this order",
    )

    class Meta:
        ordering = ["name"]


class Family(TimeStampMixin, TaxonomyBase):
    """A model that represents a Family object.

    Attributes:
        order (Order): The order to which the family belongs.
        featured_image (InsectImage): The image to represent the family. Used for display on the \
                                      frontend.
        name (str): The scientific name of the taxon. Inherited from TaxonomyBase.
        common_name (str): The common name of the taxon, if it has one. Inherited from TaxonomyBase.
        authority (str): The authority of the taxon. Inherited from TaxonomyBase.
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        related_name="+",
        help_text="Select an order to which this family belongs",
    )
    featured_image = models.OneToOneField(
        "images.CustomImage",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="+",
        help_text="Select an image to represent this family",
    )

    class Meta:
        ordering = ["name", "order"]
        verbose_name_plural = "Families"


class Subfamily(TimeStampMixin, TaxonomyBase):
    """A model that represents a Subfamily object.

    Attributes:
        family (Family): The family to which the subfamily belongs.
        name (str): The scientific name of the taxon. Inherited from TaxonomyBase.
        common_name (str): The common name of the taxon, if it has one. Inherited from TaxonomyBase.
        authority (str): The authority of the taxon. Inherited from TaxonomyBase.
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    family = models.ForeignKey(
        Family,
        on_delete=models.RESTRICT,
        related_name="+",
        help_text="Select the family to which this subfamily belongs",
    )

    class Meta:
        ordering = ["name", "family"]
        verbose_name_plural = "Subfamilies"


class Tribe(TimeStampMixin, TaxonomyBase):
    """A model that represents a Tribe object.

    Attributes:
        subfamily (Subfamily): The subfamily to which the tribe belongs.
        name (str): The scientific name of the taxon. Inherited from TaxonomyBase.
        common_name (str): The common name of the taxon, if it has one. Inherited from TaxonomyBase.
        authority (str): The authority of the taxon. Inherited from TaxonomyBase.
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    subfamily = models.ForeignKey(
        Subfamily,
        on_delete=models.RESTRICT,
        related_name="+",
        help_text="Select the subfamily to which this tribe belongs",
    )

    class Meta:
        ordering = ["name", "subfamily"]


class Genus(TimeStampMixin, TaxonomyBase):
    """A model that represents a Genus object.

    Attributes:
        tribe (Tribe): The tribe to which the genus belongs.
        name (str): The scientific name of the taxon. Inherited from TaxonomyBase.
        common_name (str): The common name of the taxon, if it has one. Inherited from TaxonomyBase.
        authority (str): The authority of the taxon. Inherited from TaxonomyBase.
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    tribe = models.ForeignKey(
        Tribe,
        on_delete=models.RESTRICT,
        related_name="+",
        help_text="Select the tribe to which this genus belongs",
    )

    class Meta:
        ordering = ["name", "tribe"]
        verbose_name_plural = "Genera"


class Species(TimeStampMixin, TaxonomyBase):
    """A model that represents a Species object.

    Attributes:
        genus (Genus): The genus to which the species belongs.
        mona (str): The MONA (Hodges) number for the species (Lepidoptera only).
        p3 (str): The P3 (Pohl, Patterson, Pelham 2016) number for the species (Lepidoptera only).
        ps (str): The Phylogenetic Sequence (Pohl and Nanz, 2023) number for the species \
                  (Lepidoptera only).
        featured_image: The image to represent the species. Used for display on the frontend.
        name (str): The scientific name of the taxon. Inherited from TaxonomyBase.
        common_name (str): The common name of the taxon, if it has one. Inherited from TaxonomyBase.
        authority (str): The authority of the taxon. Inherited from TaxonomyBase.
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    genus = models.ForeignKey(
        Genus,
        on_delete=models.RESTRICT,
        related_name="+",
        help_text="Select the genus to which this species belongs",
    )
    mona = models.CharField(
        null=True,
        blank=True,
        verbose_name="MONA #",
        help_text="Enter the MONA (Hodges) number for the species (Lepidoptera only)",
    )
    p3 = models.CharField(
        null=True,
        blank=True,
        verbose_name="P3 #",
        help_text="Enter the P3 (Pohl, Patterson, Pelham 2016) number for the species (Lepidoptera \
            only)",
    )
    ps = models.CharField(
        null=True,
        blank=True,
        verbose_name="PS #",
        help_text="Enter the Phylogenetic Sequence (Pohl and Nanz, 2023) number for the species \
            (Lepidoptera only)",
    )
    featured_image = models.OneToOneField(
        "images.CustomImage",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="+",
        help_text="Select an image to represent this species",
    )

    class Meta:
        ordering = ["genus", "name"]
        verbose_name_plural = "Species"

    def __str__(self):
        """Returns a string representation of a Species object instance.

        Returns:
            A string that refers to a Species object instance.
        """

        return self.binomial

    @property
    def binomial(self):
        """The species' binomial (genus + species)."""

        return f"{self.genus.name} {self.name}"


class Subspecies(TimeStampMixin, TaxonomyBase):
    """A model that represents a Subspecies object.

    Attributes:
        species (Species): The species to which the subspecies belongs.
        mona (str): The MONA (Hodges) number for the subspecies (Lepidoptera only).
        p3 (str): The P3 (Pohl, Patterson, Pelham 2016) number for the subspecies (Lepidoptera \
                  only).
        ps (str): The Phylogenetic Sequence (Pohl and Nanz, 2023) number for the subspecies \
                  (Lepidoptera only).
        name (str): The scientific name of the taxon.
        common_name (str): The common name of the taxon, if it has one.
        authority (str): The authority of the taxon.
        date_created (datetime): The date when the object instance was created. Inherited from \
                                 TimeStampMixin.
        date_modified (datetime): The date when the object instance was last modified. Inherited \
                                  from TimeStampMixin.
    """

    species = models.ForeignKey(
        Species,
        on_delete=models.RESTRICT,
        related_name="subspecies",
        help_text="Select the species to which this subspecies belongs",
    )
    mona = models.CharField(
        null=True,
        blank=True,
        verbose_name="MONA #",
        help_text="Enter the MONA (Hodges) number for the subspecies (Lepidoptera only). If it \
            lacks its own MONA number, use the nominate species' number",
    )
    p3 = models.CharField(
        null=True,
        blank=True,
        verbose_name="P3 #",
        help_text="Enter the P3 (Pohl, Patterson, Pelham 2016) number for the subspecies \
            (Lepidoptera only). If it lacks its own P3 number, use the nominate species' number",
    )
    ps = models.CharField(
        null=True,
        blank=True,
        verbose_name="PS #",
        help_text="Enter the Phylogenetic Sequence (Pohl and Nanz, 2023) number for the subspecies \
            (Lepidoptera only). If it lacks its own Phylogenetic Sequence number, use the \
            nominate species' number",
    )

    class Meta:
        ordering = ["species", "name"]
        verbose_name_plural = "Subspecies"

    def __str__(self):
        """Returns a string representation of a Subspecies object instance.

        Returns:
            A string that refers to a Subspecies object instance.
        """

        return self.trinomial

    @property
    def trinomial(self):
        """The subspecies' trinomial (genus + species + subspecies)."""

        return f"{self.species} {self.name}"
