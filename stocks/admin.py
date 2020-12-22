from django.contrib import admin

from .models import Stock, Share, StockValue


admin.site.register(Stock)
admin.site.register(Share)
admin.site.register(StockValue)