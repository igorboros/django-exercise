# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str
from .models import Product
from .models import Location
from .forms import ProductForm, LocationForm
from exercise import settings
import csv

from django.contrib.messages import constants as message_constants

# Create your views here.
def product_create(request):
	product = Product()
	LocationInlineFormSet = inlineformset_factory(Product, Location, form=LocationForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = ProductForm(request.POST, request.FILES, instance=product, prefix="main")
		formset = LocationInlineFormSet(request.POST, request.FILES, instance=product, prefix="nested")

		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return redirect("products:list")
	else:
		form = ProductForm(instance=product, prefix="main")
		formset = LocationInlineFormSet(instance=product, prefix="nested")

	context = {
		"page_title": "Add a New Product",
		"page_header": "Add Product",
		"form": form, 
		"formset": formset
	}
	return render(request, "product_form.html", context)

def product_list(request):
	template = "product_list.html"
	write_to_csv = False
	if request.method == "POST":	
		form_vars = [x for x in request.POST if 'product_' in x]
		product_ids = []
		for form_var in form_vars:
			product_ids.append(form_var.split("product_",1)[1])

		products = Product.objects.filter(id__in=product_ids)
		queryset = []
		start_date = request.POST["from_date"]
		end_date = request.POST["end_date"]
		export_to_csv = request.POST["export_to_csv"]
		for product in products:
			fitlered_locations = product.location_set.filter(datetime__gt=start_date, datetime__lt=end_date)
			if fitlered_locations:
				p = Product()
				p.id = product.id
				p.description = product.description
				p.locations = fitlered_locations
				queryset.append(p)

		if export_to_csv:
			write_to_csv = True
			report_file  = open(os.path.join(settings.BASE_DIR, "output.txt"), "wb")
			writer = csv.writer(report_file, delimiter=str('\t').encode('utf-8'), quotechar=str('"').encode('utf-8'), quoting=csv.QUOTE_ALL)

			for row in queryset:
				for location_row in row.locations:
					writer.writerow([row.id, row.description, location_row.datetime, location_row.longitude, location_row.latitude, location_row.elevation])
			
			report_file.close()

		template = "product_report.html"
	else:
		queryset = Product.objects.all()
	
	context = {
			"write_to_csv": write_to_csv,
			"page_title": "Product List",
			"queryset": queryset
		}
	return render(request, template, context)

def product_update(request, id=None):       

	if id is None:
		product = Product()
	else:
		product = get_object_or_404(Product, id=id)

	LocationInlineFormSet = inlineformset_factory(Product, Location, form=LocationForm, extra=1, can_delete=True)

	if request.method == "POST":
		form = ProductForm(request.POST, request.FILES, instance=product, prefix="main")
		formset = LocationInlineFormSet(request.POST, request.FILES, instance=product, prefix="nested")

		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return redirect("products:list")
	else:
		form = ProductForm(instance=product, prefix="main")
		formset = LocationInlineFormSet(instance=product, prefix="nested")
	
	context = {
		"page_title": "avc",
		"page_header": "Edit Product",
		"form": form, 
		"formset": formset
	}

	return render(request, "product_form.html", context)


def product_delete(request, id=None):
	instance = get_object_or_404(Product, id=id)
	instance.delete()
	return redirect("products:list")

# def send_file(request):
# 	response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
# 	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('output.txt')
# 	xsendfile = smart_str(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output.txt'))
# 	print(xsendfile)
# 	response['X-Sendfile'] = xsendfile
# 	response['Content-Length'] = os.path.getsize('output.txt')
# 	return response


def send_file(request):
    file_path = os.path.join(settings.BASE_DIR, "output.txt")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/text-plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404