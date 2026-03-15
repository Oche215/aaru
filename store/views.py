from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages
from .forms import ContactUsForm
from django.core.mail import send_mail
from django_project.settings import DEFAULT_FROM_EMAIL

from django.http import HttpResponse
from django.views.decorators.http import condition

# Create your views here.

def home(request):
    products = Product.objects.all()

    form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your messages was sent successfully!')
            return render(request, 'store/home.html', {'products': products, 'form': form})
        else:
            return render(request, 'store/contact.html', {'products': products, 'form': form})

    else:
        return render(request, 'store/home.html', {'products': products, 'form': form})



def contact(request):
    form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your messages was sent successfully!')
            return render(request, 'store/home.html', {'form': form})
        else:
            return render(request, 'store/contact.html', {'form': form})

    else:
        return render(request, 'store/contact.html', {'form': form})


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


def get_product_image(request, product_id):
    """Serve product image from database"""
    try:
        product = Product.objects.get(id=product_id)
        if product.pix:
            return HttpResponse(product.pix.read(), content_type='image/jpeg')
    except Product.DoesNotExist:
        pass

    # Return placeholder if no image
    return HttpResponse(status=404)


def index(request):
    products = Product.objects.all()

    return render(request, 'store/index.html', {'products': products, })


def serve_image(request, id):
    product = Product.objects.get(id=id)
    if product.pix:
        return HttpResponse(product.pix.read(), content_type='image/jpeg')
    return HttpResponse(status=404)


def gallery(request):

    return render(request, 'store/gallery.html', )

