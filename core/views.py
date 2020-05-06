from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from core.models import Article


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        posts = Article.objects.filter(publicated=True)[:10]
        kwargs['products'] = posts
        return kwargs

class ArticleView(TemplateView):
    template_name = 'index.html'