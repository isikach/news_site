from django import forms
from django.core.exceptions import ValidationError
from .models import Article, Topic
from .scrapper import AVAILABLE_SITES
from .scrapper import MitScrapper, WikipediaScrapper, WashingtonPostsScrapper


class ArticleWithUrlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.publisher_user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['topic'] = forms.ModelMultipleChoiceField(
            queryset=Topic.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )

    class Meta:
        model = Article
        fields = ['topic', 'url',]

    def clean_url(self):
        url = self.cleaned_data['url']
        if url.endswith("Main_Page"):
            raise ValidationError("You should choose an article")
        url_part = url.split("/")[2]
        if url_part not in AVAILABLE_SITES:
            raise ValidationError("You should choose available source")
        if len(url_part) < AVAILABLE_SITES[url_part]:
            raise ValidationError(f"You should choose an article from {url_part}")
        return url

    def save(self, commit=True):
#        breakpoint()
        instance = super().save(commit=False)
        instance.title, instance.body = self.create_and_save_article()
        instance.publisher = self.publisher_user
#        breakpoint()
        if commit:
            instance.save()
            topics = self.cleaned_data['topic']
            for topic in topics:
                instance.topic.add(topic)
        return instance

    def create_and_save_article(self):
        url_with_parameters = self.cleaned_data["url"]
        if "en.wikipedia.org" in url_with_parameters:
            scrapper = WikipediaScrapper(url_with_parameters)
        if "www.washingtonpost.com" in url_with_parameters:
            scrapper = WashingtonPostsScrapper(url_with_parameters)
        if "news.mit.edu" in url_with_parameters:
            scrapper = MitScrapper(url_with_parameters)
        return scrapper.parse_title(), scrapper.parse_article()


class ArticleManuallyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'] = forms.ModelMultipleChoiceField(
            queryset=Topic.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )

    class Meta:
        model = Article
        fields = ['topic', 'title', "body",]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.publisher_id = 1
        if commit:
            instance.save()
            topics = self.cleaned_data['topic']
            for topic in topics:
                instance.topic.add(topic)
        return instance
