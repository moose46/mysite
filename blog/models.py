from email.policy import default
from tkinter import CASCADE
from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# Create your models here.
class Base(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="blog_posts"
    # )

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(Base):
    tags = TaggableManager()

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "PUBLISHED"

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    objects = models.Manager()  # default manager
    published = PublishedManager()  # customer manager

    class META:
        ordering = ["-publish"]
        indexes = [
            models.Index(
                fields=["-publish"],
            )
        ]

    def get_absolute_url(self):
        """
        Returns the absolute URL for the blog post detail page.
        page 57
        Returns:
                str: The absolute URL for the blog post detail page.
        """

        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    def __str__(self):
        return self.title


class Comment(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["date_created"]
        indexes = [models.Index(fields=["date_created"])]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"
