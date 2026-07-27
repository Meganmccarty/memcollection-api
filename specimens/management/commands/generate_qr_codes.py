from django.core.management.base import BaseCommand
from specimens.models import SpecimenRecord


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
        parser.add_argument(
            "--range",
            nargs=2,
            metavar=("START_USI", "END_USI"),
            help="Generate for a range of specimens (e.g., MEM-000001 thru MEM-000100)",
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

        elif options["range"]:
            # Generate for range of specimens
            start_usi, end_usi = options["range"]
            self.generate_range(start_usi, end_usi)

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
                if not specimen.qr_code or not specimen.qr_code.storage.exists(
                    specimen.qr_code.name
                ):
                    missing_specimens.append(specimen)

            if missing_specimens:
                self.stdout.write(
                    f"Generating QR codes for {len(missing_specimens)} specimens..."
                )
                count = self.generate_for_specimens(missing_specimens)
                self.stdout.write(self.style.SUCCESS(f"\nGenerated {count} QR codes"))
            else:
                self.stdout.write("All specimens have QR codes.")

    def generate_range(self, start_usi, end_usi):
        """Generate QR codes for a range of USIs"""
        try:
            # Extract numeric portions
            start_num = int(start_usi.split("-")[1])
            end_num = int(end_usi.split("-")[1])
            prefix = start_usi.split("-")[0]

            self.stdout.write(
                f"Generating QR codes for {prefix}-{start_num:06d} to {prefix}-{end_num:06d}..."
            )

            specimens = []
            for num in range(start_num, end_num + 1):
                usi = f"{prefix}-{num:06d}"
                try:
                    specimen = SpecimenRecord.objects.get(usi=usi)
                    specimens.append(specimen)
                except SpecimenRecord.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"⚠ {usi} not found, skipping")
                    )

            if specimens:
                count = self.generate_for_specimens(specimens)
                self.stdout.write(self.style.SUCCESS(f"\nGenerated {count} QR codes"))
            else:
                self.stdout.write(self.style.WARNING("No specimens found in range"))

        except (ValueError, IndexError):
            self.stdout.write(
                self.style.ERROR(
                    "Invalid USI format. Use format: MEM-000001 MEM-000100"
                )
            )

    def generate_for_specimens(self, specimens):
        count = 0
        for specimen in specimens:
            specimen.generate_qr_code()
            specimen.save()
            self.stdout.write(self.style.SUCCESS(f"{specimen.usi}"))
            count += 1
        return count
