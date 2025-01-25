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
]
