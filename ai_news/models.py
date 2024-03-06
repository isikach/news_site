from django.contrib.auth.models import AbstractUser
from django.db import models


class Publisher(AbstractUser):
    date_of_registration = models.DateTimeField(auto_now_add=True)
    pseudonym = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.pseudonym


class Topic(models.Model):
    title = models.CharField(max_length=255)


class Article(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField("date of reposting")
    topic = models.ManyToManyField(Topic, blank=True, related_name="articles")
    publisher = models.ManyToManyField(Publisher, related_name="articles")

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name="comments")
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.pseudonym}: {self.body}"
