from wagtail import hooks
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.snippets.views.snippets import SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

from core.views import SnippetWithCustomDeleteViewSet
from specimens.models import Person, SpecimenRecord


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["specimens/butterfly.svg"]


class PersonSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the Person model."""

    model = Person
    menu_icon = "group"
    menu_label = "People"
    menu_name = "people"
    list_display = [
        "full_name",
        "first_name",
        "middle_initial",
        "last_name",
        "suffix",
        UpdatedAtColumn(),
    ]
    list_filter = ["first_name", "last_name"]
    list_editable = ["first_name"]
    list_per_page = 50


class SpecimenRecordSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the SpecimenRecord model."""

    model = SpecimenRecord
    menu_icon = "butterfly"
    menu_label = "Specimen Records"
    menu_name = "specimen_records"
    list_display = [
        "__str__",
        "order",
        "family",
        "subfamily",
        "tribe",
        "genus",
        "species",
        "subspecies",
        UpdatedAtColumn(),
    ]
    list_filter = [
        "subspecies",
        "species",
        "genus",
        "tribe",
        "subfamily",
        "family",
        "order",
        "collecting_trip",
        "country",
        "state",
        "county",
        "locality",
        "gps",
        "day",
        "month",
        "year",
    ]
    list_per_page = 100

    panels = [
        FieldPanel("usi"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("order"),
                        FieldPanel("family"),
                        FieldPanel("subfamily"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("tribe"),
                        FieldPanel("genus"),
                        FieldPanel("species"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("subspecies"),
                        FieldPanel("determiner"),
                        FieldPanel("determined_year"),
                    ]
                ),
            ],
            heading="Taxonomy Details",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("sex"),
                        FieldPanel("stage"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("preparer"),
                        FieldPanel("preparation"),
                        FieldPanel("preparation_date"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("labels_printed"),
                        FieldPanel("labeled"),
                        FieldPanel("photographed"),
                    ]
                ),
            ],
            heading="Specimen Details",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("country"),
                        FieldPanel("state"),
                        FieldPanel("county"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("locality"),
                        FieldPanel("gps"),
                        FieldPanel("collecting_trip"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("day"),
                        FieldPanel("month"),
                        FieldPanel("year"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("collector"),
                        FieldPanel("method"),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("weather"),
                        FieldPanel("temperature"),
                        FieldPanel("time_of_day"),
                    ]
                ),
                FieldPanel("habitat"),
                FieldPanel("notes"),
                FieldRowPanel(
                    [
                        FieldPanel("short_code", read_only=True),
                        FieldPanel("qr_code"),
                    ]
                ),
            ],
            heading="Locality Details",
        ),
    ]


class SpecimensViewSetGroup(SnippetViewSetGroup):
    """This groups all of the specimen snippets together in the Wagtail admin."""

    items = [
        PersonSnippet,
        SpecimenRecordSnippet,
    ]
    add_to_admin_menu = True
    menu_icon = "butterfly"
    menu_label = "Specimens"
    menu_name = "specimens"
    menu_order = 50


# Registers all of the snippets grouped under the SpecimensViewSetGroup
register_snippet(SpecimensViewSetGroup)


@hooks.register("register_admin_menu_item")
def register_export_qr_codes_menu_item():
    return AdminOnlyMenuItem(
        label="Export QR Codes",
        url="/admin/export-qr-codes/",
        icon_name="download",
    )
