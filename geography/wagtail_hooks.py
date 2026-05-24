from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.views.snippets import SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

from core.views import SnippetWithCustomDeleteViewSet
from geography.models import CollectingTrip, Country, County, GPS, Locality, State


class CountrySnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the Country model."""

    model = Country
    menu_icon = "globe"
    menu_label = "Countries"
    menu_name = "countries"
    list_display = ["name", "abbr", UpdatedAtColumn()]


class StateSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the State model."""

    model = State
    menu_icon = "globe"
    menu_label = "States"
    menu_name = "states"
    list_display = ["name", "abbr", "country", UpdatedAtColumn()]
    list_per_page = 50


class CountySnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the County model."""

    model = County
    menu_icon = "globe"
    menu_label = "Counties"
    menu_name = "counties"
    list_display = ["full_name", "state", UpdatedAtColumn()]
    list_filter = ["name", "state"]
    list_per_page = 100


class LocalitySnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the Locality model.

    It includes some custom panels for display in the Wagtail admin. While these panels could be
    included directly within the Locality model, I chose to separate as much of the Wagtail logic
    as possible from the plain Django model."""

    model = Locality
    menu_icon = "globe"
    menu_label = "Localities"
    menu_name = "localities"
    list_display = [
        "name",
        "range",
        "town",
        "county",
        "state",
        "country",
        UpdatedAtColumn(),
    ]
    list_filter = ["name", "town", "county"]
    list_per_page = 100

    panels = [
        FieldPanel("name"),
        FieldPanel("range"),
        FieldPanel("town"),
        MultiFieldPanel(
            [
                HelpPanel(
                    heading="Note:", content="Choose a maximum of 1 option below)"
                ),
                FieldPanel("county"),
                FieldPanel("state"),
                FieldPanel("country"),
            ]
        ),
    ]


class GPSSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the GPS model."""

    model = GPS
    menu_icon = "globe"
    menu_label = "GPS Coordinates"
    menu_name = "gps_coordinates"
    list_display = [
        "gps_coordinates",
        "locality",
        "locality__county",
        "elevation_meters",
        UpdatedAtColumn(),
    ]
    list_filter = ["latitude", "longitude", "locality"]
    list_per_page = 100


class CollectingTripSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the CollectingTrip model."""

    model = CollectingTrip
    menu_icon = "globe"
    menu_label = "Collecting Trips"
    menu_name = "collecting_trips"
    list_display = [
        "name",
        "joined_states",
        "start_date",
        "end_date",
        UpdatedAtColumn(),
    ]
    list_filter = ["name", "start_date", "end_date"]


class GeographyViewSetGroup(SnippetViewSetGroup):
    """This groups all of the geography snippets together in the Wagtail admin."""

    items = (
        CountrySnippet,
        StateSnippet,
        CountySnippet,
        LocalitySnippet,
        GPSSnippet,
        CollectingTripSnippet,
    )
    add_to_admin_menu = True
    menu_icon = "site"
    menu_label = "Geography"
    menu_name = "geography"
    menu_order = 90


# Registers all of the snippets grouped under the GeographyViewSetGroup
register_snippet(GeographyViewSetGroup)
