from django.contrib import admin

from .models import Stock, Share


admin.site.register(Stock)
admin.site.register(Share)