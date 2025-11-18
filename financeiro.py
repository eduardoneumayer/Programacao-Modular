"""
Módulo: financeiro
Realiza cálculos de totais, descontos e taxas sobre valores monetários.
Sem dependência de banco de dados.
"""

def calcula_total(lista_servicos: list) -> float:
    """
    Soma os valores de uma lista de dicionários de serviços.
    Retorna 0.00 se a lista estiver vazia.
    """
    if not lista_servicos:
        return 0.00
    total = sum(item.get("valor", 0.0) for item in lista_servicos)
    return float(total)

def aplica_desconto(valor: float, percentual: float) -> float:
    """
    Aplica um desconto percentual (0-100) sobre um valor.
    Retorna False se o percentual for inválido.
    """
    # Retorna False se inválido, conforme padrão dos testes
    if percentual < 0 or percentual > 100:
        return False 
    desconto = valor * (percentual / 100)
    return valor - desconto

def aplica_taxa(valor: float, percentual: float) -> float:
    """
    Acrescenta uma taxa percentual sobre um valor.
    Retorna False se a taxa for negativa.
    """
    if percentual < 0:
        return False
    taxa = valor * (percentual / 100)
    return valor + taxa