from django.urls import path
from .views import accounts, edit_user, StaffListView, logout_user, CustomLoginView, product_admin, UpdateProductView

urlpatterns = [
    path('', accounts, name='accounts'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", logout_user, name="logout"),

    path('user-profile/', edit_user, name='user-profile' ),
    path('list_staff/', StaffListView.as_view(), name='list_staff' ),

    path('product_admin/', product_admin, name='product_admin'),
    path('update_product/', UpdateProductView.as_view(), name='update_product'),


]