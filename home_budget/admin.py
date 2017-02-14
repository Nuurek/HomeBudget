from django.contrib import admin
from brands.models import Brand, Shop
from categories.models import ProductCategory
from receipts.models import Receipt, Purchase


admin.site.register(Brand)
admin.site.register(Shop)
admin.site.register(Receipt)
admin.site.register(Purchase)
admin.site.register(ProductCategory)
