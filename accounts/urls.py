from django.urls import path
from .views import (RegistrationView, AddProductView, product_table, accounts,
                    ListProductsView, UpdateProductView, product_list, product_detail, edit_user, StaffListView)


urlpatterns = [
    path('', accounts, name='accounts'  ),

    path('register/', RegistrationView.as_view(), name='register'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('list_products/', product_list, name='list_products' ),
    path('product_table/', product_table, name='product_table' ),
    path('update_product/<slug:slug>', UpdateProductView.as_view(), name='update_product'),

    path('product_detail/<slug:slug>', product_detail, name='product_detail'),
    path('user-profile/', edit_user, name='user-profile' ),
    path('list_staff/', StaffListView.as_view(), name='list_staff' ),

]