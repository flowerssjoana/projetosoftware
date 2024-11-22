from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import BooleanField

class Conta(models.Model):
    matricula = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class usuario(models.Model):
    nomeCompleto = models.CharField(max_length=100)
    idPUC = models.EmailField(max_length=100)
    emailDoCliente = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nomeCompleto

class itens(models.Model):
    nome_produto = models.CharField(max_length=300)
    id_produto = models.ForeignKey(usuario, on_delete=models.CASCADE)
    valor_produto = models.DecimalField(max_digits=10, decimal_places=2, validadors=[MinValueValidator(0.00)])
    descricao = models.TextField(max_length=300)
    foto_produto = models.ImageField(upload_to='produtos')
    
    def __str__(self):
        return self.nome_produto


class itensDoPedido(models.Model):
    id_pedido = models.ForeignKey(itens, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(usuario, on_delete=models.CASCADE)
    dataHorarioDoPedido = models.DateTimeField()
    valorTotalDoPedido = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00))
    numDeItens = models.IntegerField(validadors=[MinValueValidator(1)])
    statusDoPedido = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido {self.id_pedido} - Cliente {self.id_cliente}"



