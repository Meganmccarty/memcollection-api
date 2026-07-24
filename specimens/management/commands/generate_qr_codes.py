from django.core.management.base import BaseCommand
from specimens.models import SpecimenRecord
import os


class Command(BaseCommand):
    help = "Generate QR codes for specimens"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Generate for all specimens (overwrites existing)",
        )
        parser.add_argument(
            "--usi",
            type=str,
            help="Generate for a specific specimen by usi",
        )

    def handle(self, *args, **options):
        if options["usi"]:
            # Generate for specific specimen
            try:
                specimen = SpecimenRecord.objects.get(usi=options["usi"])
                specimen.generate_qr_code()
                specimen.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Generated QR code for {specimen.usi}")
                )
            except SpecimenRecord.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Specimen {options["usi"]} not found')
                )

        elif options["all"]:
            specimens = SpecimenRecord.objects.all()
            self.stdout.write("Generating QR codes for ALL specimens...")
            count = self.generate_for_specimens(specimens)
            self.stdout.write(self.style.SUCCESS(f"\nGenerated {count} QR codes"))

        else:
            # Generate only for specimens missing files
            specimens = SpecimenRecord.objects.all()
            missing_specimens = []

            for specimen in specimens:
                # Check if file exists on disk
                if not specimen.qr_code or not os.path.exists(specimen.qr_code.path):
                    missing_specimens.append(specimen)

            if missing_specimens:
                self.stdout.write(
                    f"Generating QR codes for {len(missing_specimens)} specimens..."
                )
                count = self.generate_for_specimens(missing_specimens)
                self.stdout.write(self.style.SUCCESS(f"\nGenerated {count} QR codes"))
            else:
                self.stdout.write("All specimens have QR codes.")

    def generate_for_specimens(self, specimens):
        count = 0
        for specimen in specimens:
            specimen.generate_qr_code()
            specimen.save()
            self.stdout.write(self.style.SUCCESS(f"{specimen.usi}"))
            count += 1
        return count
