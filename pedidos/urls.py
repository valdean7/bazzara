from django.urls import path
from . import views


app_name = 'pedidos'

urlpatterns = [
    path('pagar_pedidos/', views.pagar_pedidos, name='pagar_pedidos'),
    # path('efetuar_pagamento/', views.efetuar_pagamento, name='pagar'),
]
