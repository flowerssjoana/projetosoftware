from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Conta(models.Model):
    username = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo_choices = [('F','Funcionário'),('C','Cliente'),('A','Cliente Associado')]
    tipo = models.CharField(max_length = 1,choices=tipo_choices,default='0')
    password = models.CharField(max_length=128, default='senhapadrao')  # Campo para armazenar a senha criptografada
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class Lanche(models.Model):
  nome = models.CharField(max_length=100)
  descricao = models.TextField()
  preco = models.DecimalField(max_digits=10, decimal_places=2)
  imagem = models.ImageField(upload_to='lanches/', null=True, blank=True)

  def __str__(self):
      return self.nome

class Pedido(models.Model):
    itens = models.JSONField()  
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente_nome}'