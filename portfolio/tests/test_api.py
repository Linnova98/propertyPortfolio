from rest_framework import status
from rest_framework.test import APITestCase
from portfolio.models import Portfolio
from django.urls import reverse

class PortfolioAPITest(APITestCase):

    def setUp(self):
        print(f"Run test: {self._testMethodName}")
        self.portfolio_1 = Portfolio.objects.create(
            name="Test Portfolio 1",
            owner_of_portfolio="Test Tester",
            geographic_region="North America",
        )
        self.portfolio_2 = Portfolio.objects.create(
            name="Test Portfolio 2",
            owner_of_portfolio="Tester Test",
            geographic_region="Europe",
        )
        self.url = reverse('add-instances')

    def test_get_all_portfolios(self):
        url = reverse('view-instances')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_single_portfolio(self):
        url = reverse('view-instance', kwargs={'pk': self.portfolio_1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test Portfolio 1")

    def test_create_portfolio(self):
        data = {
            'name': "New Portfolio",
            'owner_of_portfolio': "Mr Test",
            'geographic_region': "Asia",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "New Portfolio")
    
    def test_create_portfolio_with_existing_name(self):
        data = {
            'name': "Test Portfolio 1",
            'owner_of_portfolio': "Dr Test",
            'geographic_region': "South America",
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "This portfolio already exists")

    def test_update_portfolio(self):
        url = reverse('update-instances', kwargs={'pk': self.portfolio_1.pk})
        data = {
            'name': "Updated Portfolio Name",
            'owner_of_portfolio': "Test Tester",
            'geographic_region': "North America",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('updated_data', response.data)
        self.assertIn('name', response.data['updated_data'])
        self.assertEqual(response.data['updated_data']['name'], "Updated Portfolio Name")
        
    def test_delete_portfolio(self):
        url = reverse('delete-instances', kwargs={'pk': self.portfolio_2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 202)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
