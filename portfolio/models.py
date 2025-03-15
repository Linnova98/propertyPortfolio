from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner_of_portfolio = models.CharField(max_length=50)
    geographic_region = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/portfolio/', null=True, blank=True)

    def __str__(self):
        return self.name