from django.template import Library


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
