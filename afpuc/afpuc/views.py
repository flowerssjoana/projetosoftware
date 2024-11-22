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

def listar_usuarios(request):
    usuarios = Usuario.objects.all()  # Corrigido para 'Usuario'
    data = [
        {
            "id": usuario.idPUC,
            "nome_completo": usuario.nomeCompleto,
            "email": usuario.emailDoCliente
        }
        for usuario in usuarios
    ]
    return render(request, "usuarios/listar_usuarios.html", {"usuarios": data})

def listar_itens(request):
    itens = Itens.objects.all()  # Corrigido para 'Itens'
    data = [
        {
            "id": item.id_produto,  # Corrigido de 'usuario' para 'item'
            "nome_produto": item.nomeProduto,
            "valor": float(item.valor_produto),
            "descricao": item.descricao
        }
        for item in itens
    ]
    return render(request, "itens/listar_itens.html", {"itens": data})

def listar_pedidos(request):
    pedidos = ItensDoPedido.objects.all()  # Corrigido para 'ItensDoPedido'
    data = [
        {
            "id": pedido.id_pedido.id,  # Ajustado para acessar o id do pedido
            "cliente": pedido.id_cliente.nomeCompleto,  # Corrigido para 'nomeCompleto'
            "valor_total": str(pedido.valorTotalDoPedido),
            "status": pedido.statusDoPedido,
        }
        for pedido in pedidos
    ]
    return render(request, "pedidos/listar_pedidos.html", {"pedidos": data})

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
        # Criação do pedido
        pedido = Pedido.objects.create()  # Considerando que Pedido tem relação com Produto
        produtos = Produto.objects.all()
        pedido.produtos.set(produtos)  # Defina como 'produtos' são relacionados no modelo Pedido
        
        # Calcular o total do pedido
        pedido.calcular_total()  # Assumindo que este método calcula o total corretamente
        
        context = {
            "pedido_id": pedido.id,
            "total": pedido.total,
        }
        return render(request, 'pedido_finalizado.html', context)
    
    return redirect('carrinho')