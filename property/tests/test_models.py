from django.test import TestCase
from property.models import Property
from portfolio.models import Portfolio
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.db import IntegrityError

class PropertyTest(TestCase):
    def setUp(self):
        print(f"Run test: {self._testMethodName}")

        self.portfolio = Portfolio.objects.create(
            name="Test navn",
            owner_of_portfolio="Test Testersen",
            geographic_region="North America",
            image=None
        )

        self.property = Property.objects.create(
            address="Testveien 1",
            zip_code="0010",
            zip_place="Oslo",
            estimated_value=150000.5,
            construction_year=2025,
            usable_area=100.85,
            image=None,
            portfolio=self.portfolio
        )

    def test_property_has_portfolio(self):
        self.assertEqual(self.property.portfolio, self.portfolio)

    def test_property_without_portfolio(self):
        with self.assertRaises(IntegrityError):
            Property.objects.create(
                address="Testveien 2",
                zip_code="7010",
                zip_place="Trondheim",
                estimated_value=200000.0,
                construction_year=2024,
                usable_area=120.5,
                image=None,
                portfolio=None,
            )

    def test_address_fields(self):
        self.assertEqual(self.property.address, "Testveien 1")
        self.assertEqual(self.property.zip_code, "0010")
        self.assertEqual(self.property.zip_place, "Oslo")

    def test_address_data_type(self):
        self.assertIsInstance(self.property.address, str)

    def test_zip_code_data_type(self):
        self.assertIsInstance(self.property.zip_code, str)

    def test_zip_place_data_type(self):
        self.assertIsInstance(self.property.zip_place, str)

    def test_zip_code_int_float_string(self):
        property_int = Property.objects.create(
                address="Testveien 2",
                zip_code=7010,
                zip_place="Trondheim",
                estimated_value=150000.5,
                construction_year=2025,
                usable_area=100.85,
                image=None,
                portfolio=self.portfolio
            )
        property_int.refresh_from_db()
        self.assertIsInstance(property_int.zip_code, str)
        self.assertEqual(property_int.zip_code, "7010")

        property_float = Property.objects.create(
                address="Testveien 2",
                zip_code=71.0,
                zip_place="Trondheim",
                estimated_value=150000.5,
                construction_year=2025,
                usable_area=100.85,
                image=None,
                portfolio=self.portfolio
            )

        property_float.refresh_from_db()
        self.assertIsInstance(property_float.zip_code, str)
        self.assertEqual(property_float.zip_code, "71.0")

        property_string = Property.objects.create(
            address="Testveien 2",
            zip_code="7010",
            zip_place="Trondheim",
            estimated_value=150000.5,
            construction_year=2025,
            usable_area=100.85,
            image=None,
            portfolio=self.portfolio
        )
        self.assertEqual(property_string.zip_code, "7010")

        with self.assertRaises((ValidationError, DataError)):  
            property_invalid = Property(
                address="Testveien 2",
                zip_code="70105",
                zip_place="Trondheim",
                estimated_value=150000.5,
                construction_year=2025,
                usable_area=100.85,
                image=None,
                portfolio=self.portfolio
            )
            property_invalid.full_clean()
            property_invalid.save()

    def test_number_fields(self):
        self.assertEqual(self.property.estimated_value, 150000.5)
        self.assertEqual(self.property.construction_year, 2025)
        self.assertEqual(self.property.usable_area, 100.85)

    def test_estimated_value_data_type(self):
        self.assertIsInstance(self.property.estimated_value, float)

    def test_construction_year_data_type(self):
        self.assertIsInstance(self.property.construction_year, int)

    def test_usable_area_data_type(self):
        self.assertIsInstance(self.property.usable_area, float)

def test_invalid_float_in_int_field_and_int_in_float(self):
    with self.assertRaises(ValueError):
        Property.objects.create(
            address="Testveien 4",
            zip_code="3030",
            zip_place="Drammen",
            estimated_value=1500005,
            construction_year=202.5,
            usable_area=10085,
            image=None,
            portfolio=self.portfolio
        )