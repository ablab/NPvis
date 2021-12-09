from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^npvis/$', views.main_page, name='main_page')
] + staticfiles_urlpatterns()
