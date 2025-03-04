from django.http import HttpRequest


def criar_pedidos(request: HttpRequest, response):
    transaction = response['transaction']
    status = 'PD'

    match transaction:
        case 'success':
            status = 'PG'
        case 'failure':
            status = 'PD'
        case 'pending':
            status = 'PD'

    pedidos = []

    for item in response['items']:
        obj = {
            'produto_id': item['produto_id'], 
            'variacao_nome': item['variacao_nome'], 
            'produto_nome': item['produto_nome'], 
            'tamanho': item['tamanho'], 
            'slug': item['slug'], 
            'imagem': item['imagem'], 
            'quantidade': item['quantity'], 
            'preco_unitario': item['unit_price'], 
            'status': status, 
            'comprador': request.user
        }

        pedidos.append(obj)

    return pedidos