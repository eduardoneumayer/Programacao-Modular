"""
Módulo: carros
Gerencia cadastro, listagem, busca e remoção de veículos.

Estrutura interna (exemplo):
_DB = {
  "ABC1234": {"placa": "ABC1234", "modelo": "Civic", "ano": 2015, "servicos": []}
}
"""

from typing import Dict, List, Optional
import validacao as _v

# "Banco" em memória
_DB: Dict[str, Dict] = {}

def _key(placa: str) -> str:
    # Sempre indexar pela placa normalizada SEM hífen
    return _v.normaliza_placa(placa)

def reset():
    """
    Opcional: usado pelos testadores para garantir cenário limpo.
    """
    _DB.clear()

def adiciona_carro(placa: str, modelo: str, ano: int) -> bool:
    """
    Cadastra um veículo. Retorna False se inválido ou placa já existente.
    """
    if not _v.valida_carro(placa, modelo, ano):
        return False
    k = _key(placa)
    if k in _DB:
        return False
    _DB[k] = {
        "placa": _v.normaliza_placa(placa),
        "modelo": modelo.strip(),
        "ano": ano,
        # Lista vazia para integração com módulo de serviços
        "servicos": []
    }
    return True

def lista_carro() -> List[Dict]:
    """
    Retorna lista dos carros cadastrados.
    """
    return list(_DB.values())

def busca_carro(placa: str) -> Optional[Dict]:
    """
    Retorna o dicionário do carro ou None se não existir.
    """
    k = _key(placa)
    car = _DB.get(k)
    if not car:
        return None
    # Retornar uma cópia rasa para evitar mutações externas não-controladas
    return {k_: v for k_, v in car.items()}

def remove_carro(placa: str) -> bool:
    """
    Remove o carro identificado pela placa (normalizada). Retorna True/False.
    Observação: regras sobre remoção de serviços associados são tratadas
    na integração (módulo principal/serviços), se necessário.
    """
    k = _key(placa)
    if k not in _DB:
        return False
    del _DB[k]
    return True
