def aplicar_desconto(valor: int | float, promocao: int) -> float:
    if promocao == 0: return 0
    desconto = promocao/100
    novo_preco = (valor * (1 - desconto))
    return float(novo_preco)


def preco_quant(quant: int, valor: float, promocao: int):
    if promocao > 0:
        return quant * aplicar_desconto(valor, promocao)
    return quant * valor

def variacao_existe(produtos, dados):
    existe = False
    for produto in produtos:
        if produto['variacao_nome'] == dados['variacao_nome'] \
        and produto['tamanho'] == dados['tamanho'] \
        and produto['variacao_id'] == dados['variacao_id']:
            produto['quantidade'] = int(produto['quantidade']) + dados['quantidade']
            existe = True
    return (existe, produtos)


def remover_produto(carrinho: dict[str,list[dict]], 
                        produto_id, variacao_nome, tamanho, variacao_id):
    produtos_restantes = []
    for produto in carrinho[produto_id]:
            if (produto['variacao_nome'] == variacao_nome) \
            and (produto['tamanho'] == tamanho) \
            and (produto['variacao_id'] == variacao_id):
                ...
            else:
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
            if produto['promocao'] > 0:
                novo_preco = aplicar_desconto(
                    produto['preco'], produto['promocao']
                )
                total += int(produto['quantidade']) * novo_preco
            else:
                total += int(produto['quantidade']) * produto['preco']
        return total
    else:
        return total
    

def editar_produtos(produtos: list[dict]) -> list[dict]:
    produtos_editados = []
    for produto in produtos:
        produto_copia = None
        produto_copia = produto.copy()
        quantidade = produto_copia.pop('quantidade')
        produto_copia.update(quantity=quantidade)
        preco = produto_copia.pop('preco')
        if produto['promocao'] > 0:
            produto_copia.update(
                unit_price=aplicar_desconto(preco, produto['promocao'])
            )
            produtos_editados.append(produto_copia)
        else:
            produto_copia.update(unit_price=preco)
            produtos_editados.append(produto_copia)
    
    return produtos_editados


def pegar_variacoes(produtos):
    ...