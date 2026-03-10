from django.db import models
from django import forms
from .models import ContactUs

class ContactUsForm(forms.ModelForm):

	class Meta:
		model = ContactUs
		fields = ('name', 'phone', 'email', 'message', 'service' )

	def __init__(self, *args, **kwargs):
		super(ContactUsForm, self).__init__(*args, **kwargs)
		self.fields["name"].widget.attrs['class'] = 'form-control form-input-field'
		self.fields["name"].widget.attrs['placeholder'] = 'Name'
		self.fields["name"].label = ''

		self.fields["phone"].widget.attrs['class'] = 'form-control form-input-field'
		self.fields["phone"].widget.attrs['placeholder'] = 'Phone'
		self.fields["phone"].label = ''

		self.fields["email"].widget.attrs['class'] = 'form-control form-input-field'
		self.fields["email"].widget.attrs['placeholder'] = 'Email'
		self.fields["email"].label = ''

		self.fields["message"].widget.attrs['class'] = 'form-control form-input-field'
		self.fields["message"].widget.attrs['placeholder'] = 'Type your Message here'
		self.fields["message"].label = ''

		self.fields["service"].widget.attrs['class'] = 'form-control form-input-field custom-select my-1 mr-sm-2'
		self.fields["service"].label = ''
		self.fields["service"].empty_label = '-------  Select a Service  -------'
