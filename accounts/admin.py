from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(UserProfile)

class ProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)