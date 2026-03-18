from django.urls import path

from store.views import add_product
from .views import accounts, edit_user, StaffListView, logout_user, CustomLoginView, product_admin, edit_product, \
    product_record, delete_product, AddProductView, RegistrationView, mail, email

urlpatterns = [
    path('', accounts, name='accounts'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", logout_user, name="logout"),

    path('user-profile/', edit_user, name='user-profile' ),
    path('list_staff/', StaffListView.as_view(), name='list_staff' ),
    path('register/', RegistrationView.as_view(), name='register'),
    path('mail/', mail, name='mail'),
    path('email/', email, name='email'),

    path('product_admin/', product_admin, name='product_admin'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('product_record/<slug:slug>/', product_record, name='product_record'),
    path('update_product/<slug:slug>/', edit_product, name='update_product'),
    path('delete_product/<slug:slug>/', delete_product, name='delete_product'),

]