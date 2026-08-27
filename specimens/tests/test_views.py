from django.test import Client, TestCase, override_settings
from django.contrib.auth.models import User

from specimens.models import SpecimenRecord


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    DEBUG=True,
    WHITENOISE_AUTOREFRESH=True,
)
class ExportQrCodesToPdfTestCase(TestCase):
    """A test case for the export_qr_codes view."""

    fixtures = [
        "countries.json",
        "states.json",
        "counties.json",
        "localities.json",
        "gps_coordinates.json",
        "collecting_trips.json",
        "orders.json",
        "families.json",
        "subfamilies.json",
        "tribes.json",
        "genera.json",
        "species.json",
        "subspecies.json",
        "people.json",
        "specimen_records.json",
    ]

    def setUp(self):
        """Set up test data."""

        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="staff", password="testpass123", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username="regular", password="testpass123"
        )
        self.specimen = SpecimenRecord.objects.get(usi="MEM-000001")
        self.specimen.generate_qr_code()
        self.specimen.save()

    def test_requires_staff_member(self):
        """Ensures view requires authentication."""

        response = self.client.get("/admin/export-qr-codes/", follow=False)
        self.assertIn(response.status_code, [301, 302])

    def test_regular_user_denied(self):
        """Ensures a non-staff user is denied access to the view."""

        self.client.login(username="regular", password="testpass123")
        response = self.client.get("/admin/export-qr-codes/", follow=False)
        self.assertIn(response.status_code, [403, 302])

    def test_staff_user_allowed(self):
        """Ensures a staff user is allowed to access view."""

        self.client.login(username="staff", password="testpass123")
        response = self.client.get("/admin/export-qr-codes/")
        self.assertEqual(response.status_code, 200)

    def test_response_filename_and_type(self):
        """Ensures response has a PDF content type with a name of 'specimen-qr-codes'."""

        self.client.login(username="staff", password="testpass123")
        response = self.client.get("/admin/export-qr-codes/download/")
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("specimen-qr-codes.pdf", response["Content-Disposition"])

    def test_pdf_has_data(self):
        """Ensures the PDF response has QR code data."""

        self.client.login(username="staff", password="testpass123")
        response = self.client.get("/admin/export-qr-codes/download/")
        self.assertGreater(len(response.content), 100)
