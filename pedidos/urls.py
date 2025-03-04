from django.urls import path
from . import views


app_name = 'pedidos'

urlpatterns = [
    path(
        'pagar_pedidos/', 
        views.pagar_pedidos, 
        name='pagar_pedidos'
    ),
    path(
        'efetuar_pagamento/', 
        views.efetuar_pagamento, 
        name='pagar'
    ),
    path(
        'pedidos/todos', 
        views.meus_pedidos,
        name='pedidos'
    ),
    path(
        'pedidos/a_pagar', 
        views.meus_pedidos_a_pagar, 
        name='pedidos_a_pagar'
    ),
    path(
        'pedidos/cancelar/<int:id>', 
        views.cancelar_pedido, 
        name='cancelar_pedido'
    ),
    path(
        'pedidos/cancelados', 
        views.pedidos_cancelados, 
        name='cancelados'
    ),
    path(
        'pedidos/finalizados', 
        views.pedidos_finalizados, 
        name='finalizados'
    ),
    path(
        'pedidos/devolver/<int:id>', 
        views.devolver_pedido, 
        name='devolver'
    ),
    path(
        'pedidos/devolvidos', 
        views.pedidos_devolvidos, 
        name='devolvidos'
    ),
]
