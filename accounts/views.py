from http.client import responses

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse
from django.contrib import messages

from .forms import RegistrationForm, AddProductForm, UserUpdateForm, ChangePasswordForm, UserProfileForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView
from store.models import Product, Catalog, Category
from django.db.models import Count

from .models import UserProfile
from django.contrib.auth.decorators import login_required

from django_project import settings
from django.contrib.staticfiles import finders
import os


def accounts(request):
    catalogs = Catalog.objects.all()
    products = Product.objects.all()
    category = Category.objects.all()
    total = catalogs.count()
    total_products = products.count()

    catalog = catalogs.annotate(count=Count('name'))
    product = products.annotate(count=Count('category'))

    category_counts = []
    for cat in category:
        cat_count = Product.objects.filter(category=cat).count()
        # catlog = Product.objects.get(category__catalog__name=cat.catalog.name)
        # print(f"Category: {cat}, Count: {cat_count} ")

        category_counts.append([cat, cat_count])

        context = category_counts

    catalog_counts = []
    for cat in catalogs:
        catalog_count = Product.objects.filter(category__catalog__name=cat).count()
        percent = (catalog_count / total_products) * 100

        catalog_counts.append([cat, catalog_count, percent])

        context2 = catalog_counts

    # Convert to a dictionary for quick lookup
    # category_count_map = {cat['category']: cat['cat_count'] for cat in category}

    if request.method == "POST":
        messages.success(request, 'You have been successfully logged in')
        return render(request, 'crm/crm.html',
                      {'catalogs': catalogs, 'total': total, 'total_products': total_products, 'products': products,
                       'catalog': catalog, 'product': product, 'percentage': 'percentage'})
    else:
        return render(request, 'crm/crm.html',
                      {'catalogs': catalogs, 'total': total, 'total_products': total_products, 'products': products,
                       'catalog': catalog, 'product': product, 'context': 'context', 'context2': 'context2',
                       'percent': 'percent'})








