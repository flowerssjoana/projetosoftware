from django.shortcuts import render

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