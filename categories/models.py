from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=32, blank=False)
    is_optional = models.BooleanField()

    def __str__(self):
        return self.name
