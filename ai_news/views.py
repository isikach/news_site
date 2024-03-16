from msilib.schema import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy, reverse

from django.shortcuts import render, redirect
from django.views import generic
from .forms import ArticleWithUrlForm, ArticleManuallyForm
from .models import Article, Publisher, Topic



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


class CreateArticleWithUrlView(LoginRequiredMixin, generic.CreateView):
    model = Article
    template_name = "ai_news/create_article_with_url.html"
    success_url = reverse_lazy("ai_news:article-list")
    form_class = ArticleWithUrlForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CreateArticleManuallyForm(LoginRequiredMixin, generic.CreateView):
    model = Article
    form_class = ArticleManuallyForm
    success_url = reverse_lazy("ai_news:article-list")
    template_name = "ai_news/create_article_manually.html"


class ArticleDetailView(generic.DetailView):
    model = Article


class ArticleDeleteView(generic.DeleteView):
    model = Article
    success_url = reverse_lazy("ai_news:article-list")


class PublishersListView(generic.ListView):
    model = Publisher
    template_name = "ai_news/publisher_list.html"
    paginate_by = 5
