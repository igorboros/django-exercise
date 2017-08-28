# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import Product, Location

# Create your tests here.
class ProductModelTestCase(TestCase):
	def setup(self):
		Product.objects.create(description="Test")

	def test_product_description(self):
		obj = Product.objects.get(id=1)
		self.assertTrue(obj.description != "")