from django.urls import path, include, re_path
from . import views as homePageViews


urlpatterns = [
    path('', homePageViews.IndexPage.as_view(), name='index'),
    path('about', homePageViews.AboutPage.as_view(), name='about')
]