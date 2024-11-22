from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import BooleanField

class Conta(models.Model):
    matricula = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome