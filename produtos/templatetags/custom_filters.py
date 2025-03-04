from django.template import Library
from django.utils.safestring import mark_safe


register = Library()

@register.filter
def addpromotion(value, promotion):
    desc = promotion/100
    new_value = value * (1 - desc)
    return new_value


@register.filter(name='format')
def format(value, sifra):
    return f'{sifra}{value:.2f}'.replace(',','.')


@register.filter
def mask(value: str, type):
    match type:
        case 'cep':
            return f'{value[:5]}-{value[5:]}'
        case 'tel':
            return f'({value[:2]}) {value[2:7]}-{value[6:]}'


@register.filter
def subtotal(value, quant):
    return quant * value


@register.simple_tag()
def pathname(path):
    match path:
        case '/pedidos/todos':
            return 'Todos os pedidos'
        case '/pedidos/a_pagar':
            return 'Pedidos a pagar'
        case '/pedidos/finalizados':
            return 'Pedidos finalizados'
        case '/pedidos/cancelados':
            return 'Pedidos cancelados'
        case '/pedidos/devolvidos':
            return 'Pedidos devolvidos'


@register.filter
def cardlength(card):
    length = 0
    for card_item in card.items():
        for item in card_item[1]:
            length += item['quantidade']
    if length > 0:
        return length
    else:
        return ''
