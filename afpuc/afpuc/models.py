from django.db import models

class Conta(models.Model):
    matricula = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome
