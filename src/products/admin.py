# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from models import Product, Location

class ProductModelAdmin(admin.ModelAdmin):
	list_display = ["description"]
	class Meta:
		model = Product

class LocationModelAdmin(admin.ModelAdmin):
	list_display = ["longitude", "latitude", "elevation"]
	class Meta:
		model = Location		

admin.site.register(Product, ProductModelAdmin)
admin.site.register(Location, LocationModelAdmin)