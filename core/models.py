from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    title = models.CharField(
        verbose_name=_("Book Title"),
        max_length=150
        )