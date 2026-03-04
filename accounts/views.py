from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse
from django.contrib import messages

from django.contrib.auth.views import LoginView
from store.models import Product, Catalog, Category
from django.db.models import Count
from .forms import CustomLoginForm



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
                       'catalog': catalog, 'product': product, 'percentage': percent})
    else:
        return render(request, 'crm/crm.html',
                      {'catalogs': catalogs, 'total': total, 'total_products': total_products, 'products': products,
                       'catalog': catalog, 'product': product, 'context': context, 'context2': context2,
                       'percent': percent})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm







