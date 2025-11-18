import carros

def registra_servico(placa: str, descricao: str, valor: float) -> bool:
    if not descricao or not isinstance(descricao, str):
        return False
    # Aceita int ou float, converte para float para padronizar
    if not isinstance(valor, (int, float)) or valor <= 0:
        return False

    key = carros._key(placa)
    # Verifica se o carro existe no banco de dados
    if key not in carros._DB:
        return False

    novo_servico = {
        "descricao": descricao,
        "valor": float(valor)
    }

    carros._DB[key]["servicos"].append(novo_servico)
    return True

def lista_servico(placa: str) -> list:
    key = carros._key(placa)
    if key in carros._DB:
        return list(carros._DB[key]["servicos"])
    return []

def remove_servico(placa: str, indice: int) -> bool:
    key = carros._key(placa)
    if key in carros._DB:
        servicos = carros._DB[key]["servicos"]
        if 0 <= indice < len(servicos):
            servicos.pop(indice)
            return True
    return False

def edita_servico(placa: str, indice: int, nova_descricao: str, novo_valor: float) -> bool:
    if not isinstance(novo_valor, (int, float)) or novo_valor <= 0:
        return False
    
    key = carros._key(placa)
    if key in carros._DB:
        servicos = carros._DB[key]["servicos"]
        if 0 <= indice < len(servicos):
            servicos[indice]["descricao"] = nova_descricao
            servicos[indice]["valor"] = float(novo_valor)
            return True
    return False