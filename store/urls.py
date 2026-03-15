from django.urls import path
from .views import home, details, services, about, contact, get_product_image, index, serve_image, gallery

urlpatterns = [
    path('', home, name='home'),
    path('details/<slug:slug>', details, name='product-details'),
    path('services/', services, name='services'),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('index/', index, name='index'),
    path('product/<int:product_id>/image/', get_product_image, name='product-image'),

    path('image/<int:id>/', serve_image, name='serve_image'),

    path('gallery/', gallery, name='gallery'),

]