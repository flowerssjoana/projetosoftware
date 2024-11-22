from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import BooleanField

class Conta(models.Model):
    matricula = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nomeCompleto = models.CharField(max_length=100)
    idPUC = models.EmailField(max_length=100)
    emailDoCliente = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nomeCompleto

class Item(models.Model):  # Alterei para 'Item' (singular)
    nomeProduto = models.CharField(max_length=300)
    id_produto = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Alterei para 'Usuario'
    valor_produto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    descricao = models.TextField(max_length=300)
    foto_produto = models.ImageField(upload_to='produtos')

    def __str__(self):
        return self.nomeProduto


class ItensDoPedido(models.Model):  # Alterei para 'ItensDoPedido' (nome mais apropriado)
    id_pedido = models.ForeignKey(Item, on_delete=models.CASCADE)  # Alterei para 'Item'
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Alterei para 'Usuario'
    dataHorarioDoPedido = models.DateTimeField()
    valorTotalDoPedido = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    numDeItens = models.IntegerField(validators=[MinValueValidator(1)])

    statusDoPedido = models.BooleanField(default=False)

    def calculaTotal(self):
        # Agora estamos pegando o valor de cada 'Item' associado ao pedido
        self.valorTotalDoPedido = sum(item.valor_produto for item in self.id_pedido.all())  # Corrigido
        self.save()

    def __str__(self):
        return f"Pedido {self.id_pedido} - Cliente {self.id_cliente}"


