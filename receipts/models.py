from django.db import models
from brands.models import Shop
from categories.models import ProductCategory


class Receipt(models.Model):
    time_of_purchase = models.DateField()
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)

    def __str__(self):
        name = self.time_of_purchase.strftime("%d/%m/%Y")
        name += ' - ' + str(self.shop)
        return name


class Purchase(models.Model):
    name = models.CharField(max_length=128, blank=False)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=16, decimal_places=3, default=1)
    receipt = models.ForeignKey(Receipt, models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        name = self.name + ' '
        name += str(self.amount * self.unit_price)
        return name
