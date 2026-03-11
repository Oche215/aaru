from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, UserChangeForm
from django.contrib.auth.models import User, models
from django import forms

from accounts.models import UserProfile
from store.models import Product


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control form-input-field', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length="50", widget=forms.TextInput(attrs={'class': 'form-control form-input-field', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length="50", widget=forms.TextInput(attrs={'class': 'form-control form-input-field', 'placeholder': 'Last Name'}))

    field_order = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email', 'password1', 'password2' }


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs['class'] = 'form-control input-lg form-input-field'
        self.fields["username"].widget.attrs['placeholder'] = 'username'
        self.fields["username"].label = ''
        self.fields["username"].help_text = '<span class="form-text text-muted"><small>Required. 150 Characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'


        self.fields["password1"].widget.attrs['class'] = 'form-control input-lg form-input-field'
        self.fields["password1"].widget.attrs['placeholder'] = 'password'
        self.fields["password1"].label = ''
        self.fields["password1"].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control input-lg form-input-field'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'code', 'name', 'slug', 'description', 'pix', 'manufacturer', 'price', ]

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.attrs['class'] = 'form-control form-input-field custom-select'
        self.fields["category"].label = ''
        self.fields["category"].empty_label = '-------  Select a Category  -------'

        self.fields["name"].widget.attrs['class'] = 'form-control form-input-field'
        self.fields["name"].widget.attrs['placeholder'] = 'Name'
        self.fields["name"].label = ''

        self.fields["slug"].widget.attrs['class'] = 'form-control form-input-field'
        self.fields["slug"].widget.attrs['placeholder'] = 'Slug'
        self.fields["slug"].label = ''
        self.fields["slug"].disabled = True

        self.fields["description"].widget.attrs['class'] = 'form-control form-input-field'
        self.fields["description"].widget.attrs['placeholder'] = 'Product Description'
        self.fields["description"].label = ''
        self.fields["description"].widget.attrs['rows'] = 4

        self.fields["pix"].widget.attrs['class'] = 'form-control'
        self.fields["pix"].widget.attrs['placeholder'] = 'Product Image'
        self.fields["pix"].label = ''

        self.fields["manufacturer"].widget.attrs['class'] = 'form-control form-input-field'
        self.fields["manufacturer"].widget.attrs['placeholder'] = 'Manufacturer'
        self.fields["manufacturer"].label = ''

        self.fields["price"].widget.attrs['class'] = 'form-control form-input-field'
        self.fields["price"].widget.attrs['placeholder'] = 'Price'
        self.fields["price"].label = ''

        self.fields["code"].widget.attrs['class'] = 'form-control form-input-field'
        self.fields["code"].widget.attrs['placeholder'] = 'Product Code'
        self.fields["code"].label = ''



class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'pix', 'manufacturer', 'price', ]

    # Example of custom validation
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class UserUpdateForm(UserChangeForm):
    password = None
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'}), required=True)
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False)
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ]  # Fields you want to allow editing

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class UserProfileForm(forms.ModelForm):

    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'data-mask': '(000) 000 000-0000',}), required=False)
    pix = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', }), required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["pix"].error_messages = {'invalid': "Please select a legit image file e.g., *.png, *.jpg, *.webp"}
        self.fields["phone"].error_messages = {'invalid': "Please enter your phone number in the correct format, e.g., +234 801 234 5678."}
    class Meta:
        model = UserProfile
        fields = ('phone', 'pix')
