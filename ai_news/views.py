from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse_lazy, reverse

from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, DeleteView
from .forms import ArticleWithUrlForm, ArticleManuallyForm
from .models import Article, Publisher, Topic
from .scrapper import MitScrapper, WikipediaScrapper, WashingtonPostsScrapper


def index(request):
    num_articles = Article.objects.count()
    num_publishers = Publisher.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_articles": num_articles,
        "num_publisher": num_publishers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "ai_news/index.html", context=context)


class ArticleListView(generic.ListView):
    model = Article
    template_name = "ai_news/article_list.html"
    paginate_by = 5


class CreateArticleWithUrlView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "ai_news/create_article_with_url.html"
    success_url = reverse_lazy("ai_news:article-list")
    form_class = ArticleWithUrlForm


class CreateArticleManuallyForm(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleManuallyForm
    success_url = reverse_lazy("ai_news:article-list")
    template_name = "ai_news/create_article_manually.html"



class ArticleDetailView(DetailView):
    model = Article


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("ai_news:article-list")
