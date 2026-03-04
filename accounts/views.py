from http.client import responses

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse
from django.contrib import messages

from .forms import RegistrationForm, AddProductForm, UserUpdateForm, ChangePasswordForm, UserProfileForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView
from store.models import Product, Catalog, Category
from django.db.models import Count

from .models import UserProfile
from django.contrib.auth.decorators import login_required

from django_project import settings
from django.contrib.staticfiles import finders
import os



class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


@login_required
def edit_user(request):
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        if 'setting_submit' in request.POST:
            form = UserUpdateForm(request.POST or None, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Your settings has been updated successfully.")

                return redirect('user-profile')  # Redirect to a profile page
            else:
                for field, errors in form.errors.items():
                    form_profile = UserProfileForm(instance=user_profile)
                    for error in errors:
                        messages.warning(request, f"{field}: {error}")
                        return render(request, 'registration/user-profile.html', {'post_data': request.POST, 'form': form, 'form_profile': form_profile, 'user_profile': user_profile})
                return redirect('user-profile')  # Redirect to a profile page

        elif 'profile_submit' in request.POST:
            form_profile = UserProfileForm(request.POST or None, request.FILES, instance=user_profile)
            if form_profile.is_valid():
                image_file = form_profile.cleaned_data['pix']

                form_profile.save()

                messages.success(request, "Your profile has been updated successfully.")
                return redirect('user-profile')  # Redirect to a profile page
            else:
                form = UserUpdateForm(instance=request.user)
                for field, errors in form_profile.errors.items():
                    for error in errors:
                        active_tab = request.POST.get('active_tab', 'profile-tab')
                        messages.warning(request, f"{field}: {error}" )

                        return render(request, 'registration/user-profile.html', {'post_data': request.POST, 'form_profile': form_profile, 'form': form, 'user_profile': user_profile, 'active_tab': active_tab})
                return redirect('user-profile')  # Redirect to a profile page

    else:
        form = UserUpdateForm(instance=request.user)
        form_profile = UserProfileForm(instance=user_profile)
        return render(request, 'registration/user-profile.html', {'form': form, 'form_profile': form_profile, 'user_profile': user_profile})


class AddProductView(CreateView):
    form_class = AddProductForm
    success_url = reverse_lazy("list_products")
    template_name = "registration/add_product.html"

    def form_valid(self, form):
        # You can add extra logic here before saving
        return super().form_valid(form)


class ListProductsView(ListView):
    model = Product
    template_name = 'registration/list_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-pk')  # Descending order



class UpdateProductView(UpdateView):
    model = Product
    template_name = 'registration/update_product.html'
    success_url = reverse_lazy('list_products')  # Redirect after successful update
    fields = ['category', 'name', 'slug', 'description', 'photo', 'manufacturer', 'price', ]

    # Optional: extra context for template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = f"Edit Product: {self.object.name}"
        return context


def product_list(request):
    products = Product.objects.all().order_by('-pk')
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)

        name = request.POST.get('name')

        if form.is_valid():
            form.save()
            messages.success(request, f"{name} has been saved successfully!")
            return render(request, 'registration/list_products.html', {'products': products, 'form': form})

        return render(request, 'registration/list_products.html', {'products': products, 'form': form})
    else:
        return render(request, 'registration/list_products.html', {'products': products, 'form': form})


def product_table(request):
    products = Product.objects.all().order_by('-pk')
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        name = request.POST.get('name')

        if form.is_valid():
            form.save()
            messages.success(request, f"PRODUCT: {name} has been saved successfully!")
            return render(request, 'registration/product_data.html', {'products': products, 'form': form })

        return render(request, 'registration/product_data.html', {'products': products, 'form': form})
    else:
        return render(request, 'registration/product_data.html', {'products': products, 'form': form})


def product_detail(request, slug,):
    detail = Product.objects.get(slug=slug)
    name = detail.name
    return render(request, 'registration/product_detail.html', {'detail': detail,})

def change_password(request):
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, )
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been updated successfully.")
            return redirect('user-profile')  # Redirect to a profile page
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = ChangePasswordForm(request.user, )
        return render(request, 'registration/change-password.html', {'form': form, 'user_profile': user_profile})
    return render(request, 'registration/change-password.html', {'form': form, 'user_profile': user_profile})


class StaffListView(TemplateView):
    template_name = 'registration/list_staff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["staffs"] = User.objects.all()
        context["profiles"] = UserProfile.objects.select_related("user").all()
        context['form'] = kwargs.get('form', RegistrationForm())

        return context

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            messages.success(request, f"You can successfully created a USER: {username}")
            return HttpResponseRedirect(reverse('list_staff'))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-pk')  # Descending order


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = [os.path.realpath(path) for path in result]
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def accounts(request):
    catalogs = Catalog.objects.all()
    products = Product.objects.all()
    category = Category.objects.all()
    total = catalogs.count()
    total_products = products.count()

    catalog = catalogs.annotate(count=Count('name'))
    product = products.annotate(count=Count('category'))

    category_counts = []
    for cat in category:
        cat_count = Product.objects.filter(category=cat).count()
        # catlog = Product.objects.get(category__catalog__name=cat.catalog.name)
        # print(f"Category: {cat}, Count: {cat_count} ")

        category_counts.append([cat, cat_count])

        context = category_counts

    catalog_counts = []
    for cat in catalogs:
        catalog_count = Product.objects.filter(category__catalog__name=cat).count()
        percent = (catalog_count / total_products) * 100

        catalog_counts.append([cat, catalog_count, percent])

        context2 = catalog_counts

    # Convert to a dictionary for quick lookup
    # category_count_map = {cat['category']: cat['cat_count'] for cat in category}

    if request.method == "POST":
        messages.success(request, 'You have been successfully logged in')
        return render(request, 'crm/crm.html',
                      {'catalogs': catalogs, 'total': total, 'total_products': total_products, 'products': products,
                       'catalog': catalog, 'product': product, 'percentage': 'percentage'})
    else:
        return render(request, 'crm/crm.html',
                      {'catalogs': catalogs, 'total': total, 'total_products': total_products, 'products': products,
                       'catalog': catalog, 'product': product, 'context': 'context', 'context2': 'context2',
                       'percent': 'percent'})








