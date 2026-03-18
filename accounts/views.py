from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView, TemplateView
from store.models import Product, Catalog, Category, ContactUs
from .models import UserProfile
from django.db.models import Count
from .forms import CustomLoginForm, UserUpdateForm, UserProfileForm, RegistrationForm, AddProductForm, UpdateProductForm

from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy

from django.urls import path

class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("list_staff")
    template_name = "registration/register.html"


def mail(request):
    if request.user.is_authenticated:
        mails = ContactUs.objects.all().order_by('-pk')
        total = mails.count()
        return render(request, 'crm/mail.html', {'mails': mails, 'total': total})
    else:
        messages.warning(request, 'You must be logged in to view this page')
        redirect('login')


@login_required
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
                       'catalog': catalog, 'product': product, 'percentage': percent})
    else:
        return render(request, 'crm/crm.html',
                      {'catalogs': catalogs, 'total': total, 'total_products': total_products, 'products': products,
                       'catalog': catalog, 'product': product, 'context': context, 'context2': context2,
                       'percent': percent})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm

@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out....')
    return redirect('/')


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
                updated_profile = form_profile.save(commit=False)
                user = request.user

                updated_profile.save()
                messages.success(request, f"{user}: Your profile has been updated successfully!")
                return redirect('user-profile')  # Redirect to a profile page

            else:

                form_profile = UserProfileForm(instance=user_profile)

                for field, errors in form_profile.errors.items():
                    for error in errors:
                        active_tab = request.POST.get('active_tab', 'profile-tab')
                        messages.warning(request, f"{field}: {error}" )

                return render(request, 'registration/user-profile.html', {'post_data': request.POST, 'form_profile': form_profile, 'user_profile': user_profile, 'active_tab': active_tab})


    else:
        form = UserUpdateForm(instance=request.user)
        form_profile = UserProfileForm(instance=user_profile)
        return render(request, 'registration/user-profile.html', {'form': form, 'form_profile': form_profile, 'user_profile': user_profile})


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


@login_required
def product_admin(request):
    products = Product.objects.all().order_by('-pk')
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        name = request.POST.get('name', '').strip()

        if form.is_valid():
            form.save()
            messages.success(request, f"PRODUCT: {name} has been added successfully!")
            return redirect('product_admin')
        else:
            messages.error(request, "There was an error adding the product. Please check the form.")

    return render(request, 'accounts/product_admin.html', {'products': products, 'form': form })



def edit_product(request, slug):
    if request.user.is_authenticated:
        # Fetch the product or return 404 if not found
        product = get_object_or_404(Product, slug=slug)

        if request.method == "POST":
            form = UpdateProductForm(request.POST or None, request.FILES, instance=product)
            if form.is_valid():
                updated_product = form.save(commit=False)
                name = form.cleaned_data.get('name')

                updated_product.save()
                messages.success(request, f"PRODUCT: {name} was updated successfully!")
                return redirect('product_record', slug=product.slug)

            else:
                messages.error(request, "Please correct the errors below.")
                form = UpdateProductForm(instance=product)
        else:
            form = UpdateProductForm(instance=product)

        return render(request, "accounts/update_product.html", {"form": form, "product": product})

    messages.warning(request, "You must be logged in to edit info!")
    return redirect("login",)

@login_required()
def product_record(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "accounts/product_record.html", {"product": product})

@login_required()
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    name = product.name
    product.delete()
    messages.success(request, f"PRODUCT: {name} was DELETED successfully!")
    return redirect("product_admin", )

class AddProductView(CreateView):
    form_class = AddProductForm
    success_url = reverse_lazy("list_products")
    template_name = "accounts/add_product.html"

    def form_valid(self, form):
        # You can add extra logic here before saving
        return super().form_valid(form)




