from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)

    def __str__(self):
        return self.name


class Shop(models.Model):
    address = models.CharField(max_length=128, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.brand.name + ', ' + self.address
