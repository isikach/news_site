from django.urls import path

from .views import (
    index,
    ArticleListView,
    ArticleDetailView,
    CreateArticleWithUrlView,
    CreateArticleManuallyForm,
    ArticleDeleteView,
    PublishersListView
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
    path("publishers/", PublishersListView.as_view(), name="publisher-list"),
    path("articles/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article-delete"),
]

app_name = "ai_news"
