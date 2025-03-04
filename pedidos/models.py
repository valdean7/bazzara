from django.db import models as m
from django.contrib.auth.models import User
from produtos.models import Produto


class Pedido(m.Model):
    choices = (
        ('PG', 'Pago'), ('PD', 'Pendente'), 
        ('CL', 'Cancelado'), ('DV', 'Devolvido')
    )

    produto = m.ForeignKey(Produto, on_delete=m.CASCADE)
    comprador = m.ForeignKey(User, on_delete=m.CASCADE, related_name='pedidos')
    variacao_nome = m.CharField(max_length=150)
    produto_nome = m.CharField(max_length=150)
    tamanho = m.CharField(max_length=2)
    slug = m.SlugField()
    imagem = m.CharField(max_length=255)
    quantidade = m.IntegerField()
    preco_unitario = m.FloatField()
    status = m.CharField(max_length=2, choices=choices, default='PD')
    criado_em = m.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.status}-{self.produto.nome}'
