def aplicar_desconto(valor: int | float, promocao: int) -> float | int:
    if promocao == 0: return 0
    desconto = promocao/100
    novo_preco = (valor * (1 - desconto))
    return novo_preco


def variacao_existe(produtos, dados):
    existe = False
    for produto in produtos:
        if produto['variacao_nome'] == dados['variacao_nome'] and produto['tamanho'] == dados['tamanho']:

            produto['quantidade'] = int(produto['quantidade']) + dados['quantidade']

            produto['preco_quantitativo'] = int(produto['quantidade']) * float(produto['preco'])

            produto['preco_promocional'] = aplicar_desconto(produto['preco_quantitativo'],int(produto['promocao']))

            existe = True

    return (existe, produtos)


def remover_produto(carrinho: dict[str,list[dict]], 
                        produto_id, nome, tamanho):
    produtos_restantes = []
    for produto in carrinho[produto_id]:
            if produto['variacao_nome'] != nome and produto['tamanho'] != tamanho:
                produtos_restantes.append(produto)

    carrinho[produto_id] = produtos_restantes
    return carrinho


def pegar_produtos(carrinho: dict):
    produtos = []

    for items in carrinho.items():
        for item in items[1]:
            item['produto_id'] = items[0]
            produtos.append(item)
    return produtos


def produtos_preco_total(produtos: list):
    total = 0
    if produtos:
        for produto in produtos:
            if produto.get('preco_promocional', 0) > 0:
                total += produto['preco_promocional']
            else: 
                total += produto['preco_quantitativo']
        return total
    else:
        return total
    

def editar_produtos(produtos: list[dict]) -> list[dict]:
    produtos_editados = []

    for produto in produtos:
        produto_copia = None
        if produto['preco_promocional'] > 0:
            produto_copia = produto.copy()
            preco_promocional = produto_copia.pop('preco_promocional')
            produto_copia.update(unit_price=preco_promocional)
        else:
            produto_copia = produto.copy()
            preco_quantitativo = produto_copia.pop('preco_quantitativo')
            produto_copia.update(unit_price=preco_quantitativo)

        quantidade = produto_copia.pop('quantidade')
        produto_copia.update(quantity=quantidade)

        produtos_editados.append(produto_copia)
    
    return produtos_editados