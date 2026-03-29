from django.contrib.sitemaps import Sitemap
from store.models import Product
from django.urls import reverse


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.modified_on

    def location(self, item):
        # Pass the required arguments as keyword arguments (kwargs) or args
        return reverse('product-details', kwargs={'slug': item.slug})
