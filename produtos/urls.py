from django.urls import path

from . import views

app_name = 'produtos'

urlpatterns = [
    path(
        '', 
        views.home, 
        name='home'
    ),
    
    path(
        'busca/', 
        views.busca, 
        name='busca'
    ),

    path(
        'produto/<slug>', 
        views.detalhe_produto, 
        name='produto'
    ),

    path('carrinho/add_produto/', 
        views.adicionar_no_carrinho, 
        name='add_produto'
    ),

    path(
        'carrinho/', 
        views.carrinho, 
        name='carrinho'
    ),

    path('carrinho/remover_produto', 
        views.remover_do_carrinho, 
        name='remover_produto'
    ),

    path('avaliacao/<int:id>', 
        views.produto_avaliacao, 
        name='avaliacao'
    ),

    path('avaliar/<str:uuid>', 
        views.avaliar, 
        name='avaliar'
    ),

    path(
        'promocao/',
        views.produtos_em_promocao,
        name='promocao'
    ),

    path(
        'blusas/',
        views.produtos_blusas,
        name='blusas'
    ),

    path(
        'camisas/',
        views.produtos_camisas,
        name='camisas'
    ),

    path(
        'calcados/',
        views.produtos_calcados,
        name='calcados'
    ),

    path(
        'calsas/',
        views.produtos_calsas,
        name='calsas'
    ),

    path(
        'shorts/',
        views.produtos_shorts,
        name='shorts'
    ),
]
