from django.core.management.base import BaseCommand
from specimens.models import SpecimenRecord


class Command(BaseCommand):
    help = "Generate short codes for specimens that do not have one"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Generate for all specimens (overwrites existing)",
        )

    def handle(self, *args, **options):
        if options["all"]:
            specimens = SpecimenRecord.objects.all()
            self.stdout.write("Generating short codes for all specimens...")
        else:
            specimens = SpecimenRecord.objects.filter(short_code="")
            self.stdout.write("Generating short codes for specimens without one...")

        count = specimens.count()

        if count == 0:
            self.stdout.write(self.style.WARNING("No specimens found."))
            return

        for specimen in specimens:
            specimen.save()

        self.stdout.write(
            self.style.SUCCESS(f"\nGenerated short codes for {count} specimens")
        )
