import os

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your models here.


class StatementFile(models.Model):
    statement_file = models.FileField()
    month = models.DateField(
        null=False,
        blank=False
    )

    def __str__(self):
        return self.statement_file.name

class Transaction(models.Model):
    source_file = models.ForeignKey(
        StatementFile,
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    description = models.CharField(
        max_length=1000
    )
    location = models.CharField(
        max_length=1000
    )
    amount = models.FloatField(
        null=False,
        blank=False
    )