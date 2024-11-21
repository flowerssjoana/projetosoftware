from django.contrib import admin
from .models import Conta
class ContaAdmin (admin.ModelAdmin):
    list_display = ['matricula','nome','email']
admin.site.register(Conta,ContaAdmin)