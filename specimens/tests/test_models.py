from django.test import TestCase

from specimens.models import Person, SpecimenRecord


class PersonTestCase(TestCase):
    """A test case for the Person model."""

    fixtures = ["people.json"]

    def test_name(self):
        """Ensures the __str__() method returns the Person object's full name."""

        all_fields = Person.objects.get(first_name="Paul", last_name="Smith")
        self.assertEqual(all_fields.__str__(), "Paul A. Smith, Jr.")

    def test_collector_name(self):
        """Ensures the collector_name property is formatted correctly."""

        no_suffix = Person.objects.get(
            first_name="Megan", middle_initial="E", last_name="McCarty"
        )
        no_middle = Person.objects.get(
            first_name="Thomas", last_name="Williams", suffix="III"
        )
        no_middle_no_suffix = Person.objects.get(first_name="Jane", last_name="Doe")
        all_fields = Person.objects.get(
            first_name="Paul", middle_initial="A", last_name="Smith", suffix="Jr."
        )

        self.assertEqual(no_suffix.collector_name, "M.E. McCarty")
        self.assertEqual(no_middle.collector_name, "T. Williams III")
        self.assertEqual(no_middle_no_suffix.collector_name, "J. Doe")
        self.assertEqual(all_fields.collector_name, "P.A. Smith Jr.")

    def test_full_name(self):
        """Ensures a Person object's full name is returned."""

        no_middle_no_suffix = Person.objects.get(first_name="Jane", last_name="Doe")
        no_suffix = Person.objects.get(first_name="Megan", last_name="McCarty")
        no_middle = Person.objects.get(first_name="Thomas", last_name="Williams")
        all_fields = Person.objects.get(first_name="Paul", last_name="Smith")

        self.assertEqual(no_middle_no_suffix.__str__(), "Jane Doe")
        self.assertEqual(no_suffix.__str__(), "Megan E. McCarty")
        self.assertEqual(no_middle.__str__(), "Thomas Williams, III")
        self.assertEqual(all_fields.__str__(), "Paul A. Smith, Jr.")


class SpecimenRecordTestCase(TestCase):
    """A test case for the SpecimenRecord model."""

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

    def test_name(self):
        """Ensures the __str__() method returns the SpecimenRecord object's USI."""

        specimen = SpecimenRecord.objects.get(usi="MEM-000001")
        self.assertEqual(specimen.__str__(), "MEM-000001")

    def test_generate_short_code_from_usi(self):
        """Ensures a short code is generated for a specimen based on the USI."""

        specimen = SpecimenRecord.objects.get(usi="MEM-000001")
        specimen.generate_short_code()
        self.assertEqual(specimen.short_code, "000001")

    def test_identified(self):
        """Ensures the identified property returns the correct boolean state."""

        specimen_unidentified = SpecimenRecord.objects.filter(
            species__name__isnull=True
        )[0]
        specimen_identified = SpecimenRecord.objects.filter(
            species__name__isnull=False
        )[0]

        self.assertEqual(specimen_unidentified.identified, False)
        self.assertEqual(specimen_identified.identified, True)

    def test_collected_date(self):
        """Ensures the collected date for labels is formatted correctly."""

        specimen_full_date = SpecimenRecord.objects.get(day=26, month="June", year=2006)
        specimen_month_year = SpecimenRecord.objects.get(
            day__isnull=True, month="May", year=2009
        )
        specimen_year_only = SpecimenRecord.objects.get(
            day__isnull=True, month="", year=2012
        )

        self.assertEqual(specimen_full_date.collected_date, "26-Jun-2006")
        self.assertEqual(specimen_month_year.collected_date, "May 2009")
        self.assertEqual(specimen_year_only.collected_date, "2012")

    def test_full_date(self):
        """Ensures the full_date property returns the correct formatted date."""

        specimen_full_date = SpecimenRecord.objects.get(day=26, month="June", year=2006)
        specimen_month_year = SpecimenRecord.objects.get(
            day__isnull=True, month="May", year=2009
        )
        specimen_year_only = SpecimenRecord.objects.get(
            day__isnull=True, month="", year=2012
        )

        self.assertEqual(specimen_full_date.full_date, "26 June 2006")
        self.assertEqual(specimen_month_year.full_date, "May 2009")
        self.assertEqual(specimen_year_only.full_date, "2012")

    def test_num_date(self):
        """Ensures the num_date property returns the date formatted as numbers only."""

        specimen_full_date = SpecimenRecord.objects.get(day=26, month="June", year=2006)
        specimen_full_date_2 = SpecimenRecord.objects.get(
            day=5, month="October", year=2010
        )
        specimen_month_year = SpecimenRecord.objects.get(
            day__isnull=True, month="May", year=2009
        )
        specimen_year_only = SpecimenRecord.objects.get(
            day__isnull=True, month="", year=2012
        )

        self.assertEqual(specimen_full_date.num_date, "2006-06-26")
        self.assertEqual(specimen_full_date_2.num_date, "2010-10-05")
        self.assertEqual(specimen_month_year.num_date, "2009-05")
        self.assertEqual(specimen_year_only.num_date, "2012")

    def test_collectors(self):
        """Ensures that multiple collectors are joined as a single string."""

        specimen_multiple_collectors = (
            SpecimenRecord.objects.filter(collector__last_name="Doe")
            .filter(collector__last_name="McCarty")
            .filter(collector__last_name="Smith")
            .filter(collector__last_name="Williams")
            .distinct()[0]
        )
        specimen_single_collector = SpecimenRecord.objects.filter(
            collector__last_name="McCarty"
        ).distinct()[0]

        self.assertEqual(specimen_single_collector.collectors, "M.E. McCarty")
        self.assertEqual(
            specimen_multiple_collectors.collectors,
            "J. Doe, M.E. McCarty, P.A. Smith Jr., T. Williams III",
        )

    def test_temp_F(self):
        """Ensures the temperature is correctly formatted as Fahrenheit."""

        DEGREE_SIGN = "\N{DEGREE SIGN}"
        specimen_temp_F_decimal = SpecimenRecord.objects.get(temperature="85.5")
        specimen_temp_F_integer = SpecimenRecord.objects.get(temperature="76")
        specimen_no_temp = SpecimenRecord.objects.get(temperature="")

        self.assertEqual(specimen_temp_F_decimal.temp_F, f"85.5{DEGREE_SIGN}F")
        self.assertEqual(specimen_temp_F_integer.temp_F, f"76{DEGREE_SIGN}F")
        self.assertEqual(specimen_no_temp.temp_F, "")

    def test_temp_C(self):
        """Ensures the temperature is correctly formatted as Celsius."""

        DEGREE_SIGN = "\N{DEGREE SIGN}"
        specimen_temp_F_decimal = SpecimenRecord.objects.get(temperature="85.5")
        specimen_temp_F_integer = SpecimenRecord.objects.get(temperature="76")
        specimen_no_temp = SpecimenRecord.objects.get(temperature="")

        self.assertEqual(specimen_temp_F_decimal.temp_C, f"29.7{DEGREE_SIGN}C")
        self.assertEqual(specimen_temp_F_integer.temp_C, f"24.4{DEGREE_SIGN}C")
        self.assertEqual(specimen_no_temp.temp_C, "")
