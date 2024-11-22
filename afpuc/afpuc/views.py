from django.shortcuts import render
from .forms import CriarConta
from .models import Conta
from django.http import HttpResponse
from .models import Produto, Pedido


def cozinha (request):
    pedidos = {
        'numero1' : '1002',
        'conteudo1' : 'pão de queijo',
        'conteudo21' : 'mate com limão',
        'sit1': 'em preparo',
        'numero' : '997',
        'conteudo' : 'pão com ovo',
        'conteudo2' : 'suco de laranja',
        'sit': 'entregue'
    }
    return render(request,'cozinha.html',pedidos)

def criar_conta (request):
    if request.method == 'GET':
        # Renderizar o formulário vazio
        formulario = CriarConta()
    elif request.method == 'POST':
        # Processar os dados enviados no formulário
        formulario = CriarConta(request.POST)
        if formulario.is_valid():
             # Criar e salvar a instância do modelo
            Conta.objects.create(
                matricula=formulario.cleaned_data['matricula'],
                nome=formulario.cleaned_data['nome'],
                email=formulario.cleaned_data['email']
            )
            # Aqui você pode salvar os dados no banco ou realizar outra lógica
            return HttpResponse(f"Conta criada com sucesso para {formulario.cleaned_data['nome']} ({formulario.cleaned_data['email']})!")

    else:
        # Caso o método HTTP não seja suportado
        return HttpResponse("Método não suportado.", status=405)

    return render(request, 'criarconta.html', {'formulario': formulario})

def listar_usuarios (request):
    usuarios = usuario.objects.all()
    data = [
        {
            "id" : usuario.idPUC,
            "nome_completo" : usuario.nomeCompleto,
            "email" : usuario.emailDoCliente
        }
        for usuario in usuarios 
    ]
        return render(request, "usuarios/listar_usuarios.html",{"usuarios": usuarios})


def listar_itens (request): 
    itens = Itens.objects.all()
    data = [
        {
            "id" : usuario.id_produto,
            "nome_produto" : usuario.nomeProduto,
            "valor": float(item.valor_produto),
            "descricao": item.descricao
        }
        for item in itens 
    ]
        return render(request, "itens/listar_itens.html",{"itens": itens})
    
def listar_pedidos (request): 
    pedidos = itensDoPedido.objects.all()
    data = [{
        "id" : pedido.id_pedido
        "cliente" : pedido.id_cliente.nome_completo,
        "valor_total" : str(pedido.valorTotalDoPedido),
        "status" : pedido.statusDoPedido,
    }
    for pedido in pedidos
 ]
    #return JsonResponse(data, safe=False)
    return render(request, "pedidos/listar_pedidos.html",{"pedidos": pedidos})

def carrinho(request):
    produtos = Produto.objects.all()
    total = sum(produto.preco for produto in produtos)
    context = {
        'produtos': produtos,
        'total': total,
    }
    return render(request, 'carrinho.html', context)

def finalizar_pedido(request):
    if request.method == "POST":
        pedido = Pedido.objects.create()
        produtos = Produto.objects.all() 
        pedido.produtos.set(produtos)
        pedido.calcular_total()
        return JsonResponse({"status": "Pedido realizado com sucesso!", "total": float(pedido.total)})
    return JsonResponse({"status": "Método não permitido."}, status=405)
