from django.urls import path
from .views import home, details, services, about, contact

urlpatterns = [
    path('', home, name='home'),
    path('details/<slug:slug>', details, name='product-details'),
    path('services/', services, name='services'),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

]