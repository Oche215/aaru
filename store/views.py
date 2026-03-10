from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages
from .forms import ContactUsForm
from django.core.mail import send_mail
from django_project.settings import DEFAULT_FROM_EMAIL

# Create your views here.

def home(request):
    products = Product.objects.all()
    form = ContactUsForm()
    if request.method == "POST":
        if 'logout' in request.POST:
            messages.success(request, 'You have signed out!')
            return render(request, 'store/home.html', {'products': products, 'form': form })
        else:
            form = ContactUsForm(request.POST, )

            address = request.POST.get('email')
            name = request.POST.get('name')
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            service = request.POST.get('service')

            if address and name and message:
                try:
                    send_mail(f'Inquiry from {name}',
                              f'From: {address}\nName: {name} \nPhone: {phone} \nServices: {service} \nMessage: {message}',
                              DEFAULT_FROM_EMAIL, ['reachus@avadacouture.com', 'avadacouturewebsite@gmail.com'], )
                    messages.success(request, 'Email sent successfully')
                except Exception as e:
                    messages.error(request, f'Error sending email {e}')
            else:
                messages.success(request, 'All fields are required to send us a note except for File')

            if form.is_valid():
                form.save()

                # messages.success(request, 'Your messages uploaded successfully!')
                return render(request, 'store/home.html', {'products': products, 'form': form })

    else:
        return render(request, 'store/home.html', {'products': products, 'form': form })

def contact(request):
    form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST, )

        address = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        service = request.POST.get('service')

        if address and name and message:
            try:
                send_mail(f'Inquiry from {name}',f'From: {address}\nName: {name} \nPhone: {phone} \nServices: {service} \nMessage: {message}', DEFAULT_FROM_EMAIL, ['reachus@avadacouture.com', 'avadacouturewebsite@gmail.com'],)
                messages.success(request, 'Email sent successfully')
            except Exception as e:
                messages.error(request, f'Error sending email {e}')
        else:
            messages.success(request, 'All fields are required to send us a note except for File')


        if form.is_valid():
            form.save()

            # messages.success(request, 'Your messages uploaded successfully!')
            return render(request, 'home.html', {'form': form})

    else:
        return redirect(home)

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
