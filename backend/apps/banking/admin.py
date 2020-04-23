from django.contrib import admin

from .models import StatementFile, Transaction

# Register your models here.


admin.site.register(StatementFile)
admin.site.register(Transaction)
