from django.shortcuts import render
from django.views.generic import ListView, TemplateView

# Create your views here.


class IndexPage(TemplateView):
    template_name = 'homepage/index_layout.html'

class AboutPage(TemplateView):
    template_name = 'homepage/about.html'