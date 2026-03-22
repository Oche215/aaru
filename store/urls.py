from django.urls import path
from .views import home, details, services, about, contact, get_product_image, index, serve_image, gallery, ProductDetailView
from accounts.views import delete_message

urlpatterns = [
    path('', home, name='home'),
    path('details/<slug:slug>', ProductDetailView.as_view(), name='product-details'),
    path('services/', services, name='services'),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('delete_message/<int:pk>/', delete_message, name='delete_message'),

    path('index/', index, name='index'),
    path('product/<int:product_id>/image/', get_product_image, name='product-image'),

    path('image/<int:id>/', serve_image, name='serve_image'),

    path('gallery/', gallery, name='gallery'),

    # path('post/<int:pk>/', ProductDetailView.as_view(), name='post-detail'),

]