from django.contrib import admin
from django import forms
from .models import Product, Catalog, Category, ContactUs, Service


# Register your models here.
class MyModelAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'pix': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'custom-file-input'})
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('added_by', 'modified_by')  # Hide from form

    def save_model(self, request, obj, form, change):
        if not change or not obj.added_by or not obj.modified_by:  # Only set when creating
            obj.added_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    prepopulated_fields = {'slug': ('name',)}

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.slug == True:
            return ('slug',) + self.readonly_fields
        return self.readonly_fields


admin.site.register(Catalog)
admin.site.register(Category)
admin.site.register(ContactUs)
admin.site.register(Service)
