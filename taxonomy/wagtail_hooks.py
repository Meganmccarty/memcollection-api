from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.views.snippets import SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

from core.views import SnippetWithCustomDeleteViewSet
from taxonomy.models import Family, Genus, Order, Species, Subfamily, Subspecies, Tribe


class OrderSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the Order model."""

    model = Order
    menu_icon = "list-ul"
    menu_label = "Orders"
    menu_name = "orders"
    list_display = ["name", "common_name", "authority", UpdatedAtColumn()]
    list_filter = ["name", "common_name", "authority"]
    list_per_page = 50


class FamilySnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the family model."""

    model = Family
    menu_icon = "list-ul"
    menu_label = "Families"
    menu_name = "families"
    list_display = ["name", "common_name", "authority", "order", UpdatedAtColumn()]
    list_filter = ["name", "common_name", "authority", "order"]
    list_per_page = 100


class SubfamilySnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the subfamily model."""

    model = Subfamily
    menu_icon = "list-ul"
    menu_label = "Subfamilies"
    menu_name = "subfamilies"
    list_display = ["name", "common_name", "authority", "family", UpdatedAtColumn()]
    list_filter = ["name", "common_name", "authority", "family"]
    list_per_page = 100


class TribeSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the tribe model."""

    model = Tribe
    menu_icon = "list-ul"
    menu_label = "Tribes"
    menu_name = "tribes"
    list_display = ["name", "common_name", "authority", "subfamily", UpdatedAtColumn()]
    list_filter = ["name", "common_name", "authority", "subfamily"]
    list_per_page = 100


class GenusSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the genus model."""

    model = Genus
    menu_icon = "list-ul"
    menu_label = "Genera"
    menu_name = "genera"
    list_display = ["name", "common_name", "authority", "tribe", UpdatedAtColumn()]
    list_filter = ["name", "common_name", "authority", "tribe"]
    list_per_page = 100


class SpeciesSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the species model."""

    model = Species
    menu_icon = "list-ul"
    menu_label = "Species"
    menu_name = "species"
    list_display = [
        "binomial",
        "genus",
        "name",
        "common_name",
        "authority",
        "mona",
        "ps",
        UpdatedAtColumn(),
    ]
    list_filter = ["genus", "name", "common_name", "authority", "mona", "ps"]
    list_per_page = 100


class SubspeciesSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the subspecies model."""

    model = Subspecies
    menu_icon = "list-ul"
    menu_label = "Subspecies"
    menu_name = "subspecies"
    list_display = [
        "trinomial",
        "species__genus",
        "species__name",
        "name",
        "common_name",
        "authority",
        "mona",
        "ps",
        UpdatedAtColumn(),
    ]
    list_filter = ["species", "name", "common_name", "authority", "mona", "ps"]
    list_per_page = 100


class TaxonomyViewSetGroup(SnippetViewSetGroup):
    """This groups all of the taxonomy snippets together in the Wagtail admin."""

    items = [
        OrderSnippet,
        FamilySnippet,
        SubfamilySnippet,
        TribeSnippet,
        GenusSnippet,
        SpeciesSnippet,
        SubspeciesSnippet,
    ]
    add_to_admin_menu = True
    menu_icon = "form"
    menu_label = "Taxonomy"
    menu_name = "taxonomy"
    menu_order = 70


# Registers all of the snippets grouped under the TaxonomyViewSetGroup
register_snippet(TaxonomyViewSetGroup)
