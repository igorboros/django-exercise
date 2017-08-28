# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Product(models.Model):
	description = models.CharField(max_length=120)

	def locations(self):
		return self.locations

	def has_locations(self):
		return self.location_set.all()

	def get_last_location(self):
		return self.location_set.last()

	def get_delete_url(self):
		return reverse("products:delete", kwargs={ "id":self.id })

	def get_edit_url(self):
		return reverse("products:edit", kwargs={ "id":self.id })

	def __unicode__(self):
		return self.description		

class Location(models.Model):
	datetime = models.DateTimeField(auto_now=False, auto_now_add = False)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	elevation = models.IntegerField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	class Meta: 
		ordering = ["-datetime"]