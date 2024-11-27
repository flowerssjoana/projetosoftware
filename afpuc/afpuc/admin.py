from django.contrib import admin
from .models import Conta
class ContaAdmin (admin.ModelAdmin):
    list_display = ['username','nome','email','tipo','password']
admin.site.register(Conta,ContaAdmin)