from django.shortcuts import render
from .forms import CriarConta
from .models import Conta
from django.http import HttpResponse


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