from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import Article, Topic, Publisher, Comment
from .scrapper import AVAILABLE_SITES
from .scrapper import MitScrapper, WikipediaScrapper, WashingtonPostsScrapper


class ArticleWithUrlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.publisher_user = kwargs.pop("user")
        self.scrap = None
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
            raise forms.ValidationError("This url already exists.")

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

        if not self.scrup().check_if_article():
            raise ValidationError("Invalid URL. Choose an article")

        return url

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.title, instance.body = self.parse_title_and_body_article()
        instance.publisher = self.publisher_user
        if commit:
            instance.save()
            topics = self.cleaned_data["topic"]
            for topic in topics:
                instance.topic.add(topic)
        return instance

    def scrup(self):
        url_with_parameters = self.cleaned_data["url"]
        if "en.wikipedia.org" in url_with_parameters:
            self.scrup = WikipediaScrapper(url_with_parameters)
        elif "www.washingtonpost.com" in url_with_parameters:
            self.scrup = WashingtonPostsScrapper(url_with_parameters)
        elif "news.mit.edu" in url_with_parameters:
            self.scrup = MitScrapper(url_with_parameters)
        return self.scrup

    def parse_title_and_body_article(self):
        return self.scrup.parse_title(), self.scrup.parse_article()


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
            for topic in topics:
                instance.topic.add(topic)
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
