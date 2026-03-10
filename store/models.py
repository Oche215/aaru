from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
from autoslug import AutoSlugField

from io import BytesIO
from django.core.files.base import ContentFile
import barcode
from barcode.writer import ImageWriter

# Create your models here.
class Catalog(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', max_length=150, unique=True, blank=True, editable=True, always_update=True)
    description = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from='name', max_length=150, unique=True, blank=True, editable=True, always_update=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    pix = models.ImageField(upload_to="product/", blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, related_name='adder')
    added_on = models.DateTimeField(auto_now_add=True)

    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='modifier')
    modified_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', related_name='cat', on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=120)

    barcode_img = models.ImageField(upload_to='barcodes/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.code = self.code.upper()  # Convert to uppercase before saving

        if not self.slug:
            self.slug = slugify(self.name)

        if not self.barcode_img:  # Generate barcode only if it doesn't exist
            # Choose a barcode type (e.g., Code128, EAN13, Code39)
            EAN = barcode.get_barcode_class('code128')
            # Create the barcode object with the data
            ean = EAN(f'{self.code}', writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)  # Write the barcode to an in-memory buffer

            # Save the image to the ImageField
            self.barcode_img.save(f'{self.code}.png', ContentFile(buffer.getvalue()), save=False)

        super(Product, self).save(*args, **kwargs)



class Category(models.Model):
    catalog = models.ForeignKey('Catalog', related_name='categories', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', max_length=150, unique=True, blank=True, editable=True, always_update=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        if self.parent:
            return u'%s: %s - %s' % (self.catalog.name, self.parent.name, self.name)
        return u'%s: %s' % (self.catalog.name, self.name)

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    name = models.CharField(max_length=220)
    date_created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True, )
    email = models.EmailField(
        max_length=254,  # Optional, default is 254
        blank=False,  # Field must be filled in forms
        null=False,  # Field cannot be NULL in the database
        help_text="Enter a valid email address"

    )
    message = models.TextField(max_length=360, blank=True)
    service = models.CharField(max_length=120, blank=True)


    def __str__(self):
        return f"{self.name} ({self.email})"

