from django.urls import path
from .views import accounts, edit_user, StaffListView


urlpatterns = [
    path('', accounts, name='accounts'),

    path('user-profile/', edit_user, name='user-profile' ),
    path('list_staff/', StaffListView.as_view(), name='list_staff' ),

]