from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.published.all()

    #  https://djangocentral.com/creating-sitemaps-in-django/
    def lastmod(self, obj):
        return obj.date_updated
