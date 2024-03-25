from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import Article, Topic, Publisher, Comment
from .scrapper import AVAILABLE_SITES
from .scrapper import MitScrapper, WikipediaScrapper, WashingtonPostsScrapper


WIKIPEDIA_URL = "en.wikipedia.org"
WASHINGTON_POST_URL = "www.washingtonpost.com"
MIT_URL = "news.mit.edu"


class ArticleWithUrlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.publisher_user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["topic"] = forms.ModelMultipleChoiceField(
            queryset=Topic.objects.all(), widget=forms.CheckboxSelectMultiple
        )

    class Meta:
        model = Article
        fields = [
            "topic",
            "url",
        ]

    def clean_url(self):
        url = self.cleaned_data["url"]
        if Article.objects.filter(url=url).exists():
            raise forms.ValidationError("This URL already exists.")

        if url.endswith("Main_Page"):
            raise ValidationError("You should choose an article")

        url_parts = url.split("/")
        if len(url_parts) < 3:
            raise ValidationError("Invalid URL format")

        url_part = url_parts[2]
        if url_part not in AVAILABLE_SITES:
            raise ValidationError("You should choose an available source")

        if len(url_part) < AVAILABLE_SITES[url_part]:
            raise ValidationError(f"You should choose an article from {url_part}")

        return url

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        if url:
            scrup = self.scrup(url)
            if not scrup.check_if_article():
                raise ValidationError("Invalid URL. Choose an article")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.title, instance.body = self.parse_title_and_body_article(instance.url)
        instance.publisher = self.publisher_user
        if commit:
            instance.save()
            topics = self.cleaned_data["topic"]
            instance.topic.add(*topics)
        return instance

    def scrup(self, url):
        if WIKIPEDIA_URL in url:
            return WikipediaScrapper(url)
        elif WASHINGTON_POST_URL in url:
            return WashingtonPostsScrapper(url)
        elif MIT_URL in url:
            return MitScrapper(url)

    def parse_title_and_body_article(self, url):
        scrup = self.scrup(url)
        return scrup.parse_title(), scrup.parse_article()


class ArticleManuallyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.publisher_user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["topic"] = forms.ModelMultipleChoiceField(
            queryset=Topic.objects.all(), widget=forms.CheckboxSelectMultiple
        )

    class Meta:
        model = Article
        fields = [
            "topic",
            "title",
            "body",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.publisher_id = self.publisher_user.id
        if commit:
            instance.save()
            topics = self.cleaned_data["topic"]
            instance.topic.add(*topics)
        return instance


class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            "title",
        ]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if Topic.objects.filter(title=title).exists():
            raise forms.ValidationError("This topic already exists.")
        return title


class PublisherCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Publisher
        fields = UserCreationForm.Meta.fields


class ArticleSearchForm(forms.Form):
    body = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Write here..."}),
    )


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "comment",
        ]

    def __init__(self, *args, **kwargs):
        self.publisher = kwargs.pop("publisher", None)
        self.article = kwargs.pop("article", None)
        super(CommentCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CommentCreationForm, self).save(commit=False)
        instance.publisher = self.publisher
        instance.article = self.article
        if commit:
            instance.save()
        return instance
