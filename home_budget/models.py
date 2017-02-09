from django.db import models
from djmoney.models.fields import MoneyField


class Brand(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)

    def __str__(self):
        return self.name


class Shop(models.Model):
    address = models.CharField(max_length=128, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.address


class Receipt(models.Model):
    time_of_purchase = models.DateField()
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)

    def __str__(self):
        name = self.time_of_purchase.strftime("%d-%m-%Y")
        name += ' - ' + str(self.shop)
        return name


class ProductCategory(models.Model):
    name = models.CharField(max_length=32, blank=False)
    is_optional = models.BooleanField()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    name = models.CharField(max_length=128, blank=False)
    unit_price = MoneyField(max_digits=8, decimal_places=2, default_currency="PLN")
    amount = models.DecimalField(max_digits=16, decimal_places=3, default=1)
    receipt = models.ForeignKey(Receipt, models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        name = self.name + ' '
        name += str(self.ilosc_produktu * float(self.cena_jednostkowa)) + 'zł'
        return name
