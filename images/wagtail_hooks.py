from wagtail.snippets.views.snippets import SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

from core.views import SnippetWithCustomDeleteViewSet
from images.models import HabitatImage, InsectImage, PlantImage, SpecimenRecordImage


class SpecimenRecordImageSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the SpecimenRecordImage model."""

    model = SpecimenRecordImage
    menu_icon = "image"
    menu_label = "Specimen Record Images"
    menu_name = "specimen_record_images"


class InsectImageSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the InsectImage model."""

    model = InsectImage
    menu_icon = "image"
    menu_label = "Insect Images"
    menu_name = "insect_images"


class PlantImageSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the PlantImage model."""

    model = PlantImage
    menu_icon = "image"
    menu_label = "Plant Images"
    menu_name = "plant_images"


class HabitatImageSnippet(SnippetWithCustomDeleteViewSet):
    """A snippet for the HabitatImage model."""

    model = HabitatImage
    menu_icon = "image"
    menu_label = "Habitat Images"
    menu_name = "habitat_images"


class CustomImagesViewSetGroup(SnippetViewSetGroup):
    """This groups all of the custom image snippets together in the Wagtail admin."""

    items = [
        SpecimenRecordImageSnippet,
        InsectImageSnippet,
        PlantImageSnippet,
        HabitatImageSnippet,
    ]
    add_to_admin_menu = True
    menu_icon = "image"
    menu_label = "Custom Images"
    menu_name = "custom_images"
    menu_order = 150


# Registers all of the snippets grouped under the CustomImagesViewSetGroup
register_snippet(CustomImagesViewSetGroup)
