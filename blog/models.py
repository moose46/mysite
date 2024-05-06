from email.policy import default
from tkinter import CASCADE
from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Base(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(Base):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "PUBLISHED"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
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

    def __str__(self):
        return self.title
