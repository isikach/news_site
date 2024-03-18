from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic

from .forms import (
    ArticleWithUrlForm,
    ArticleManuallyForm,
    ArticleSearchForm,
    CreateTopicForm,
    CommentCreationForm,
    PublisherCreationForm,
)
from .models import Article, Publisher, Topic, Comment


def index(request):
    num_articles = Article.objects.count()
    num_publishers = Publisher.objects.count()
    num_topics = Topic.objects.count()
    all_topics = Topic.objects.all()
    context = {
        "num_articles": num_articles,
        "num_publisher": num_publishers,
        "num_topics": num_topics,
        "all_topics": all_topics,
    }

    return render(request, "ai_news/index.html", context=context)


class ArticleListView(generic.ListView):
    model = Article
    template_name = "ai_news/article_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        body = self.request.GET.get("body", "")
        context["search_form"] = ArticleSearchForm(initial={"body": body})
        return context

    def get_queryset(self):
        form = ArticleSearchForm(self.request.GET)
        if form.is_valid():
            return Article.objects.filter(body__icontains=form.cleaned_data["body"])
        return Article.objects.all()


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ArticleDetailView(generic.DetailView):
    model = Article

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        stuff = get_object_or_404(Article, pk=self.kwargs["pk"])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        return context


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


class PublisherCreateView(generic.CreateView):
    form_class = PublisherCreationForm
    success_url = reverse_lazy("ai_news:index")
    template_name = "ai_news/publisher_form.html"


class PublisherDetailView(generic.DetailView):
    model = Publisher


class TopicCreateView(generic.CreateView):
    model = Topic
    form_class = CreateTopicForm
    success_url = reverse_lazy("ai_news:index")


@login_required
def like_view(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, id=pk)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        article.save()
    return redirect(request.META.get("HTTP_REFERER"))


class AddCommentView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["publisher"] = self.request.user
        kwargs["article"] = self.get_article()
        return kwargs

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        form.instance.article = self.get_article()
        return super().form_valid(form)

    def get_article(self):
        article_id = self.kwargs.get("pk")
        return get_object_or_404(Article, pk=article_id)

    def get_success_url(self):
        return reverse_lazy(
            "ai_news:article-detail", kwargs={"pk": self.kwargs.get("pk")}
        )
