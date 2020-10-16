"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.admin import my_admin_site
########## Site Maps ##############
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from apps.models import plan
from apps.sitemaps import StaticSitemap
info_dict = {
    'queryset': plan.objects.all(),
    
}
sitemaps={
    'static':StaticSitemap,
    # 'blog': GenericSitemap(info_dict),
    
}

###################################
urlpatterns = [
    path('admin/', my_admin_site.urls),
    url(r'', include('apps.urls')),
    url(r'^blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml/', sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
