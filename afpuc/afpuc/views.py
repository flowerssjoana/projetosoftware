from django.shortcuts import render, redirect
from .forms import CriarConta
from .models import Conta
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password  # Para criptografar a senha
from .models import Lanche
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

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
                username=formulario.cleaned_data['username'],
                nome=formulario.cleaned_data['nome'],
                email=formulario.cleaned_data['email'],
                tipo = formulario.cleaned_data['tipo'],
                password=make_password(formulario.cleaned_data['password'])  # Criptografa a senha
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
    return render(request, "listar_usuarios.html", {"usuarios": data})

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
    return render(request, "listar_itens.html", {"itens": data})

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
    return render(request, "listar_pedidos.html", {"pedidos": data})

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

# Exibe o cardápio com os lanches
def cardapio(request):
  lanches = Lanche.objects.all()  # Pega todos os lanches cadastrados
  return render(request, 'cardapio.html')

 #Adiciona um lanche ao carrinho (armazenado na sessão)
def adicionar_ao_carrinho(request, lanche_id):
    lanche = Lanche.objects.get(id=lanche_id)  # Pega o lanche pelo ID

    # Adiciona o lanche ao carrinho armazenado na sessão
    carrinho = request.session.get('carrinho', {})  # Pega o carrinho atual (se houver)
    if lanche_id in carrinho:
        carrinho[lanche_id]['quantidade'] += 1  
    else:
        carrinho[lanche_id] = {'nome': lanche.nome, 'preco': str(lanche.preco), 'quantidade': 1}
    request.session['carrinho'] = carrinho
    return redirect('cardapio:ver_carrinho')  # Redireciona para a página do carrinho


 #Exibe o carrinho
def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})  # Recupera o carrinho da sessão
    lanches = Lanche.objects.filter(id__in=carrinho.keys())  # Filtra os lanches no carrinho
    total = sum([lanche.preco * carrinho[str(lanche.id)] for lanche in lanches])  # Calcula o total

    return render(request, 'carrinho.html', {'lanches': lanches, 'carrinho': carrinho, 'total': total})

# Função de "Pedir" que limpa o carrinho
def pedir(request):
   carrinho = request.session.get('carrinho', {})
   if carrinho:
       request.session['carrinho'] = {}  # Limpa o carrinho após o pedido
       messages.success(request, 'Pedido realizado com sucesso!')
       return redirect('cardapio:pedido_confirmado')
   else:
       messages.error(request, 'Seu carrinho está vazio!')
       return redirect('cardapio:ver_carrinho')
   
def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Obter o nome de usuário e a senha fornecidos pelo formulário
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                # Verificar se o usuário existe na tabela Conta
                conta = Conta.objects.get(username=username)
                
                # Verificar a senha utilizando o método check_password
                if conta.check_password(password):
                    # Senha correta, fazer login
                    django_login(request, conta)
                    return redirect('cozinha/')  # Redirecionar para a página inicial ou qualquer outra página após o login
                else:
                    # Senha incorreta
                    form.add_error(None, "Nome de usuário ou senha inválidos.")

            except Conta.DoesNotExist:
                # Usuário não encontrado na tabela Conta
                form.add_error(None, "Nome de usuário ou senha inválidos.")
    
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})