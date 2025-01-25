from django.shortcuts import render, redirect
from django.http import HttpRequest
from endereco.models import Endereco
from django.contrib.auth.decorators import login_required
from utils.carrinho import (pegar_produtos, produtos_preco_total,
                            editar_produtos)
from pprint import pprint
# from payment_emulation.payment.paymentSDK import PaymentSDK


@login_required(login_url='registro:registrar')
def pagar_pedidos(request: HttpRequest):
    endereco = Endereco.objects.filter(usuario=request.user).first()
    carrinho = request.session.get('carrinho', {})
    produtos = pegar_produtos(carrinho)
    total = produtos_preco_total(produtos)

    context = {'endereco': endereco, 'produtos': produtos, 'total': total}
    return render(request, 'pagar_pedidos.html', context)


# def efetuar_pagamento(request: HttpRequest):
#     carrinho = request.session.get('carrinho', {})
#     seed = PaymentSDK.get_seeds()['REPROBI']
#     cpf = seed['account'].get('cpf')
#     card_number = seed['card'].get('card_number')
#     cvv = seed['card'].get('cvv')
#     validity = seed['card'].get('validity')
#     holder = seed['card'].get('card_holder_name')

#     produtos = pegar_produtos(carrinho)
#     itens = editar_produtos(produtos)

#     sdk = PaymentSDK(itens)
#     response = sdk.payment(cpf,card_number,validity, cvv, holder)
#     pprint(response)
#     return redirect('pedidos:pagar_pedidos')