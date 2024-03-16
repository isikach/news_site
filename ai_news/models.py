from django.contrib.auth.models import AbstractUser
from django.db import models


class Publisher(AbstractUser):
    date_of_registration = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Topic(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Article(models.Model):
    CHOICES = (
        ("from_url", "from_url"),
        ("from_user", "from_user")
    )
    title = models.CharField(max_length=500, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    topic = models.ManyToManyField(Topic, blank=True, related_name="articles")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="articles")
    url = models.URLField(default="", blank=True, null=True)
    created_by = models.CharField(max_length=10, choices=CHOICES, default="from_user")
    likes = models.ManyToManyField(Publisher, blank=True, related_name="articles_liked")

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name="comments")
    comment = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.publisher.username}: {self.article}"
