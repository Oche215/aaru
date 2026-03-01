from django.urls import path
from .views import home, details, services, about

urlpatterns = [
    path('', home, name='home'),
    path('details/<slug:slug>', details, name='product-details'),
    path('services/', services, name='services'),
    path('about/', about, name='about'),

]