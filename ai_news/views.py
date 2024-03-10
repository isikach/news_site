from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
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
    form_class = ArticleWithUrlForm
    template_name = "ai_news/create_article_with_url.html"
    success_url = reverse_lazy("article-list")

    @transaction.atomic
    def create_and_save_article(self, request, url_with_parameters, form):
        if "en.wikipedia.org" in url_with_parameters:
            scrapper = WikipediaScrapper(url_with_parameters)
        elif "www.washingtonpost.com" in url_with_parameters:
            scrapper = WashingtonPostsScrapper(url_with_parameters)
        elif "news.mit.edu" in url_with_parameters:
            scrapper = MitScrapper(url_with_parameters)
        else:
            return HttpResponse("Error: unknown source")

        article = scrapper.create_article()
        article.save()
        return HttpResponse("Article created successfully")


    def post(self, request):
        url_with_parameters = request.POST.get('url')
        if url_with_parameters:
            form = ArticleWithUrlForm(request.POST)
            if form.is_valid():
                response = self.create_and_save_article(request, url_with_parameters, form)
                return response
        return HttpResponse("Помилка: статтю не можна створити")



class CreateArticleManuallyForm(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleManuallyForm
    template_name = "ai_news/create_article_manually.html"


class ArticleDetailView(DetailView):
    model = Article


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("ai_news:article-list")
