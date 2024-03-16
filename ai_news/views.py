from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from django.shortcuts import render
from django.views import generic
from .forms import ArticleWithUrlForm, ArticleManuallyForm, CreateTopicForm, PublisherCreationForm
from .models import Article, Publisher, Topic


def index(request):
    num_articles = Article.objects.count()
    num_publishers = Publisher.objects.count()
    num_topics = Topic.objects.count()

    context = {
        "num_articles": num_articles,
        "num_publisher": num_publishers,
        "num_topics": num_topics,
    }

    return render(request, "ai_news/index.html", context=context)


class ArticleListView(generic.ListView):
    model = Article
    queryset = Article.objects.prefetch_related("articles")
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


class ArticleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Article
    success_url = reverse_lazy("ai_news:article-list")

class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Article
    success_url = reverse_lazy("ai_news:article-list")
    fields = ["title", "body"]
    template_name = "ai_news/create_article_manually.html"


class PublishersListView(generic.ListView):
    model = Publisher
    template_name = "ai_news/publisher_list.html"
    paginate_by = 5


class PublisherCreateView(generic.CreateView):
    form_class = PublisherCreationForm
    template_name = "ai_news/publisher_form.html"




class PublisherDetailView(generic.DetailView):
    model = Publisher


class TopicsListView(generic.ListView):
    model = Topic


class TopicCreateView(generic.CreateView):
    model = Topic
    form_class = CreateTopicForm
    success_url = reverse_lazy("ai_news:topic-list")
