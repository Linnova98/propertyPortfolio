from django.db import models

class Property(models.Model):
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=4)
    zip_place = models.CharField(max_length=50)

    estimated_value = models.FloatField()
    construction_year = models.IntegerField()
    usable_area = models.FloatField()
    image = models.ImageField(upload_to='images/property/', null=True, blank=True)

    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='property')