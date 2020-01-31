from django.contrib import admin

# Register your models here.

from .models import StatementFile, Transaction

admin.site.register(StatementFile)
admin.site.register(Transaction)
