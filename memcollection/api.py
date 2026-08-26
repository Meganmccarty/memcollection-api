from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from geography.views import (
    CollectingTripsAPIViewSet,
    CountiesAPIViewSet,
    CountriesAPIViewSet,
    GPSAPIViewSet,
    LocalitiesAPIViewSet,
    NestedCountiesAPIViewSet,
    NestedGPSAPIViewSet,
    NestedLocalitiesAPIViewSet,
    NestedStatesAPIViewSet,
    StatesAPIViewSet,
)
from pages.views import SpeciesPagesAPIViewSet
from specimens.views import PeopleAPIViewSet, SpecimenRecordAPIViewSet
from taxonomy.views import (
    FamiliesAPIViewSet,
    GeneraAPIViewSet,
    NestedFamiliesAPIViewSet,
    NestedGeneraAPIViewSet,
    NestedSpeciesAPIViewSet,
    NestedSubfamiliesAPIViewSet,
    NestedSubspeciesAPIViewSet,
    NestedTribesAPIViewSet,
    OrdersAPIViewSet,
    SpeciesAPIViewSet,
    SubfamiliesAPIViewSet,
    SubspeciesAPIViewSet,
    TribesAPIViewSet,
)

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (such as pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)

# Custom endpoints for the geography app
api_router.register_endpoint("countries", CountriesAPIViewSet)
api_router.register_endpoint("states", StatesAPIViewSet)
api_router.register_endpoint("nested-states", NestedStatesAPIViewSet)
api_router.register_endpoint("counties", CountiesAPIViewSet)
api_router.register_endpoint("nested-counties", NestedCountiesAPIViewSet)
api_router.register_endpoint("localities", LocalitiesAPIViewSet)
api_router.register_endpoint("nested-localities", NestedLocalitiesAPIViewSet)
api_router.register_endpoint("gps-coordinates", GPSAPIViewSet)
api_router.register_endpoint("nested-gps-coordinates", NestedGPSAPIViewSet)
api_router.register_endpoint("collecting-trips", CollectingTripsAPIViewSet)

# Custom endpoint for pages app (SpeciesPage, specifically)
api_router.register_endpoint("species-pages", SpeciesPagesAPIViewSet)

# Custom endpoints for the specimens app
api_router.register_endpoint("people", PeopleAPIViewSet)
api_router.register_endpoint("specimen-records", SpecimenRecordAPIViewSet)

# Custom endpoints for the taxonomy app
api_router.register_endpoint("orders", OrdersAPIViewSet)
api_router.register_endpoint("families", FamiliesAPIViewSet)
api_router.register_endpoint("nested-families", NestedFamiliesAPIViewSet)
api_router.register_endpoint("subfamilies", SubfamiliesAPIViewSet)
api_router.register_endpoint("nested-subfamilies", NestedSubfamiliesAPIViewSet)
api_router.register_endpoint("tribes", TribesAPIViewSet)
api_router.register_endpoint("nested-tribes", NestedTribesAPIViewSet)
api_router.register_endpoint("genera", GeneraAPIViewSet)
api_router.register_endpoint("nested-genera", NestedGeneraAPIViewSet)
api_router.register_endpoint("species", SpeciesAPIViewSet)
api_router.register_endpoint("nested-species", NestedSpeciesAPIViewSet)
api_router.register_endpoint("subspecies", SubspeciesAPIViewSet)
api_router.register_endpoint("nested-subspecies", NestedSubspeciesAPIViewSet)
