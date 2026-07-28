import os
import tempfile

from core.utils.helpers import get_fields
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from wagtail.api.v2.views import BaseAPIViewSet

from specimens.filters import SpecimenRecordFilter
from specimens.models import Person, SpecimenRecord
from specimens.serializers import PersonSerializer, SpecimenRecordSerializer


class PeopleAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the Person model using the PersonSerializer."""

    base_serializer_class = PersonSerializer
    model = Person
    queryset = Person.objects.all()
    body_fields = get_fields(PersonSerializer)
    listing_default_fields = get_fields(PersonSerializer)


class SpecimenRecordAPIViewSet(BaseAPIViewSet):
    """A custom API view set for the SpecimenRecord model using the
    SpecimenRecordSerializer."""

    base_serializer_class = SpecimenRecordSerializer
    model = SpecimenRecord
    queryset = SpecimenRecord.objects.all()
    body_fields = get_fields(SpecimenRecordSerializer)
    listing_default_fields = get_fields(SpecimenRecordSerializer)
    filterset_class = SpecimenRecordFilter

    def check_query_parameters(self, query_params):
        """Disables Wagtail's strict query param validation so that
        custom django-filter parameters are allowed."""
        return

    def get_queryset(self):
        queryset = super().get_queryset()

        filterset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
            request=self.request,
        )

        if filterset.is_valid():
            return filterset.qs.distinct()

        return queryset


@staff_member_required
def export_qr_codes_pdf(request):
    """Export QR codes to printable PDF."""
    specimens = SpecimenRecord.objects.filter(qr_code__isnull=False)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    labels_per_row = 25
    labels_per_col = 24
    label_width = width / labels_per_row
    label_height = height / labels_per_col

    label_count = 0
    for specimen in specimens:
        row = label_count % labels_per_col
        col = (label_count // labels_per_col) % labels_per_row

        x = col * label_width
        y = height - (row + 1) * label_height

        c.rect(x, y, label_width, label_height)

        qr_size = 20
        qr_x = x + (label_width - qr_size) - 2
        qr_y = y + (label_height - qr_size) - 2

        if specimen.qr_code:
            if os.getenv("ENVIRONMENT") == "prod":
                qr_file = BytesIO(specimen.qr_code.read())
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                    tmp_file.write(qr_file.read())
                    tmp_path = tmp_file.name
                
                c.drawImage(
                    tmp_path,
                    qr_x,
                    qr_y,
                    width=qr_size,
                    height=qr_size,
                    preserveAspectRatio=True,
                )
                os.unlink(tmp_path)
            else:
                c.drawImage(
                    specimen.qr_code.path,
                    qr_x,
                    qr_y,
                    width=qr_size,
                    height=qr_size,
                    preserveAspectRatio=True,
                )

        # Put specimen usi as text below QR code
        c.setFont("Helvetica", 3)
        usi_text = specimen.usi
        text_width = c.stringWidth(usi_text, "Helvetica", 3)
        text_x = x + (label_width - text_width) - 3
        text_y = qr_y - 8
        c.drawString(text_x, text_y, usi_text)

        label_count += 1

        if label_count % (labels_per_row * labels_per_col) == 0:
            c.showPage()

    c.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="specimen-qr-codes.pdf"'
    return response
