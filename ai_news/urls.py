from django.urls import path

from .views import (
    index,
    ArticleListView,
    ArticleDetailView,
    CreateArticleWithUrlView,
    CreateArticleManuallyForm,
    ArticleUpdateView,
    ArticleDeleteView,
    PublishersListView,
    PublisherCreateView,
    PublisherDetailView,
    TopicsListView,
    TopicCreateView
)

urlpatterns = [
    path("", index, name="index"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path(
        'articles/create/',
        CreateArticleManuallyForm.as_view(),
        name="article-create-manually"
    ),
    path(
        "articles/create/url/",
        CreateArticleWithUrlView.as_view(),
        name="article-create-with-url"
    ),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path("articles/<int:pk>/update/", ArticleUpdateView.as_view(), name="article-update"),
    path("articles/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article-delete"),
    path("publishers/", PublishersListView.as_view(), name="publisher-list"),
    path("publishers/create", PublisherCreateView.as_view(), name="publisher-create"),
    path("publishers/<int:pk>/", PublisherDetailView.as_view(), name="publisher-detail"),
    path("topics/", TopicsListView.as_view(), name="topic-list"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create")
]

app_name = "ai_news"
