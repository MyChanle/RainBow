from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown


class Avatar(models.Model):
    """ Avatar """
    content = models.ImageField(upload_to="avatar/%Y%m%d")


class Tag(models.Model):
    """ Tag """
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.text


class Category(models.Model):
    """ Category class """
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title


class Article(models.Model):
    """ Article model """

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="article"
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="article"
    )
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # for markdown
    def get_md(self):
        """ get_md """
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc'
            ]
        )
        md_body = md.convert(self.body)

        return md_body, md.toc

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
