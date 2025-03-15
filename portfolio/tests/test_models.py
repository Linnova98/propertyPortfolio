# app/tests/test_models.py

from django.test import TestCase
from portfolio.models import Portfolio
from django.db import IntegrityError

class PortfolioTest(TestCase):
    def setUp(self):
        print(f"Run test: {self._testMethodName}")
        self.portfolio = Portfolio.objects.create(
            name="Test navn",
            owner_of_portfolio="Test Testersen",
            geographic_region="North America",
            image=None
        )

    def test_portfolio_str(self):
        self.assertEqual(str(self.portfolio), "Test navn")

    def test_field_properties(self):
        self.assertEqual(self.portfolio.name, "Test navn")
        self.assertEqual(self.portfolio.owner_of_portfolio, "Test Testersen")
        self.assertEqual(self.portfolio.geographic_region, "North America")
        self.assertIsNone(self.portfolio.image.name)

    def test_image_field(self):
        self.portfolio.image = None
        self.portfolio.save()
        self.portfolio.refresh_from_db()

        self.assertFalse(bool(self.portfolio.image))
        self.assertEqual(self.portfolio.image.name, '')

    def test_unique_name_for_portfolio(self):
        Portfolio.objects.create(
            name="Unikt navn",
            owner_of_portfolio="Test",
            geographic_region="Europe"
        )
        with self.assertRaises(IntegrityError):
            Portfolio.objects.create(
                name="Unikt navn",
                owner_of_portfolio="Tester",
                geographic_region="Europe"
            )
