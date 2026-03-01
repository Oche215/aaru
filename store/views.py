from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages

# Create your views here.

def home(request):
    products = Product.objects.all()
    if request.method == "POST":
        messages.success(request, 'You have signed out!')
        return render(request, 'store/home.html', {'products': products, })
    return render(request, 'store/home.html', {'products': products, })

def details(request, slug):
    product = Product.objects.get(slug=slug)

    return render(request, 'store/details.html', {'product': product,})


def services(request):
    return render(request, 'store/services.html', {})

def about(request):
    return render(request, 'store/about.html', {})


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Product.objects.create(name=name, added_by=request.user)
        return redirect('success_page')
    return render(request, 'create_item.html')
