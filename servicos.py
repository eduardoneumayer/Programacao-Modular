"""
Módulo: servicos
Gerencia a lógica de manipulação de serviços vinculados aos veículos.
Delega a persistência para o módulo carros.
"""
import carros

def registra_servico(placa: str, descricao: str, valor: float) -> bool:
    """
    Valida os dados e solicita ao módulo carros a inclusão de um novo serviço.
    """
    if not descricao or not isinstance(descricao, str):
        return False
    if not isinstance(valor, (int, float)) or valor <= 0:
        return False

    # Verifica existência via função pública
    if not carros.busca_carro(placa):
        return False

    novo_servico = {
        "descricao": descricao,
        "valor": float(valor)
    }

    # CRITÉRIO 4: Usa função de acesso, não mexe na variável global
    return carros.anexar_servico_interno(placa, novo_servico)

def lista_servico(placa: str) -> list:
    """
    Retorna a lista de serviços de um carro específico.
    """
    carro = carros.busca_carro(placa)
    if carro:
        return carro.get("servicos", [])
    return []

def remove_servico(placa: str, indice: int) -> bool:
    """
    Remove um serviço baseando-se no índice da lista.
    """
    return carros.remover_servico_interno(placa, indice)

def edita_servico(placa: str, indice: int, nova_descricao: str, novo_valor: float) -> bool:
    """
    Atualiza descrição e valor de um serviço existente.
    """
    if not isinstance(novo_valor, (int, float)) or novo_valor <= 0:
        return False
    
    dados_atualizados = {
        "descricao": nova_descricao,
        "valor": float(novo_valor)
    }
    
    return carros.atualizar_servico_interno(placa, indice, dados_atualizados)