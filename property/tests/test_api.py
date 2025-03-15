from rest_framework.test import APITestCase
from property.models import Property
from portfolio.models import Portfolio
from django.urls import reverse

class PropertyAPITest(APITestCase):

    def setUp(self):
        print(f"Run test: {self._testMethodName}")
        self.portfolio = Portfolio.objects.create(
            name="Test Portfolio",
            owner_of_portfolio="Test Tester",
            geographic_region="Europe",
        )

        self.property_1 = Property.objects.create(
            address="Testveien 1",
            zip_code="0010",
            zip_place="Oslo",
            estimated_value=150000.5,
            construction_year=2025,
            usable_area=100.85,
            image=None,
            portfolio=self.portfolio
        )

        self.property_2 = Property.objects.create(
            address="Testveien 2",
            zip_code="0010",
            zip_place="Oslo",
            estimated_value=15095.5,
            construction_year=2024,
            usable_area=150000.85,
            image=None,
            portfolio=self.portfolio
        )

        self.url = reverse('add-items')
        self.list_url = reverse('view-items') 
    
    def test_get_all_properties(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_simple_property(self):
        url = reverse('view-item', kwargs={'pk': self.property_1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['address'], "Testveien 1")
        self.assertEqual(response.data['zip_code'], "0010")
        self.assertEqual(response.data['zip_place'], "Oslo")
        self.assertEqual(response.data['estimated_value'], 150000.5)
        self.assertEqual(response.data['construction_year'], 2025)
        self.assertEqual(response.data['usable_area'], 100.85)

    def test_create_property(self):
        data = {
            "address": "Testveien 2",
            "zip_code": "0010",
            "zip_place": "Oslo",
            "estimated_value": 4500000.0,
            "construction_year": 2024,
            "usable_area": 1000.75,
            "portfolio": self.portfolio.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['address'], "Testveien 2")
        self.assertEqual(response.data['zip_code'], "0010")
        self.assertEqual(response.data['zip_place'], "Oslo")
        self.assertEqual(response.data['estimated_value'], 4500000.0)
        self.assertEqual(response.data['construction_year'], 2024)
        self.assertEqual(response.data['usable_area'], 1000.75)
        self.assertEqual(response.data['portfolio'], 1)

    def test_create_property_with_invalid_zip_code(self):
        data = {
            "address": "Testveien 3",
            "zip_code": "999",
            "zip_place": "Oslo",
            "estimated_value": 2500000.0,
            "construction_year": 2020,
            "usable_area": 80.0,
            "portfolio": self.portfolio.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('zip_code', response.data)

    def test_update_property(self):
        url = reverse('update-items', kwargs={'pk': self.property_1.pk})
        data = {
            "address": "Testveien 4",
            "zip_code": "0010",
            "zip_place": "Oslo",
            "estimated_value": 6000000.0,
            "construction_year": 2020,
            "usable_area": 130.0,
            "portfolio": self.portfolio.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['updated_data']['address'], "Testveien 4")
        self.assertEqual(response.data['updated_data']['zip_code'], "0010")
        self.assertEqual(response.data['updated_data']['portfolio'], self.portfolio.id)

    def test_delete_property(self):
        url = reverse('delete-items', kwargs={'pk': self.property_2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 202)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)