from django.http import HttpRequest
from django.test import TestCase

if __name__ == "__main__":
    from ai_news.forms import ArticleWithUrlForm
    from ai_news.views import CreateArticleWithUrlView

    request = HttpRequest()
    request.method = "POST"

    form_data = {
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "topic": "Google",
    }
    form = ArticleWithUrlForm(data=form_data)

    response = CreateArticleWithUrlView().create_and_save_article(request, form)

    print(response)
