def calcula_total(lista_servicos: list) -> float:
    if not lista_servicos:
        return 0.00
    total = sum(item.get("valor", 0.0) for item in lista_servicos)
    return float(total)

def aplica_desconto(valor: float, percentual: float) -> float:
    # Retorna False se inválido, conforme padrão dos testes
    if percentual < 0 or percentual > 100:
        return False 
    desconto = valor * (percentual / 100)
    return valor - desconto

def aplica_taxa(valor: float, percentual: float) -> float:
    if percentual < 0:
        return False
    taxa = valor * (percentual / 100)
    return valor + taxa