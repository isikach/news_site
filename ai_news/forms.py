from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import Article, Comment, Topic
from .scrapper import AVAILABLE_SITES


class ArticleWithUrlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
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
        url_parts = url.split("/")
        if url_parts[2] not in AVAILABLE_SITES:
            raise ValidationError("You should choose available source")
        if len(url_parts) < AVAILABLE_SITES[url_parts[2]]:
            raise ValidationError(f"You should choose an article from {url_parts[2]}")
        return url



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
