"""
Módulo: carros
Gerencia cadastro, persistência e acesso aos dados dos veículos.
"""
import json
import os
import validacao as _v
from typing import Dict, List, Optional

_DB: Dict[str, Dict] = {}
ARQUIVO_DB = "banco_dados.json"

def _key(placa: str) -> str:
    return _v.normaliza_placa(placa)

def salvar_dados():
    try:
        with open(ARQUIVO_DB, 'w', encoding='utf-8') as f:
            json.dump(_DB, f, indent=4)
        return True
    except Exception:
        return False

def carregar_dados():
    global _DB
    if not os.path.exists(ARQUIVO_DB):
        return
    try:
        with open(ARQUIVO_DB, 'r', encoding='utf-8') as f:
            _DB = json.load(f)
    except Exception:
        _DB = {}

def adiciona_carro(placa: str, modelo: str, ano: int) -> bool:
    if not _v.valida_carro(placa, modelo, ano):
        return False
    k = _key(placa)
    if k in _DB:
        return False
    _DB[k] = {
        "placa": _v.normaliza_placa(placa),
        "modelo": modelo.strip(),
        "ano": ano,
        "servicos": [],
        "total_pago": 0.0  # NOVO CAMPO: Acumula pagamentos
    }
    salvar_dados()
    return True

def lista_carro() -> List[Dict]:
    # Garante que carros antigos tenham o campo total_pago ao listar
    lista = []
    for c in _DB.values():
        if "total_pago" not in c:
            c["total_pago"] = 0.0
        lista.append(c)
    return lista

def busca_carro(placa: str) -> Optional[Dict]:
    k = _key(placa)
    car = _DB.get(k)
    if not car:
        return None
    return {
        "placa": car["placa"],
        "modelo": car["modelo"],
        "ano": car["ano"],
        "servicos": list(car["servicos"]),
        "total_pago": car.get("total_pago", 0.0) # Retorna o valor pago
    }

def remove_carro(placa: str) -> bool:
    k = _key(placa)
    if k not in _DB:
        return False
    del _DB[k]
    salvar_dados()
    return True

# --- Funções Internas de Manipulação ---

def anexar_servico_interno(placa: str, servico: dict) -> bool:
    k = _key(placa)
    if k in _DB:
        _DB[k]["servicos"].append(servico)
        salvar_dados()
        return True
    return False

def remover_servico_interno(placa: str, indice: int) -> bool:
    k = _key(placa)
    if k in _DB:
        lista = _DB[k]["servicos"]
        if 0 <= indice < len(lista):
            lista.pop(indice)
            salvar_dados()
            return True
    return False

def atualizar_servico_interno(placa: str, indice: int, novo_dado: dict) -> bool:
    k = _key(placa)
    if k in _DB:
        lista = _DB[k]["servicos"]
        if 0 <= indice < len(lista):
            lista[indice].update(novo_dado)
            salvar_dados()
            return True
    return False

def registrar_pagamento_interno(placa: str, valor: float) -> bool:
    """
    Soma o valor recebido ao total_pago do carro.
    """
    k = _key(placa)
    if k in _DB:
        atual = _DB[k].get("total_pago", 0.0)
        _DB[k]["total_pago"] = atual + valor
        salvar_dados()
        return True
    return False

def reset():
    _DB.clear()
    salvar_dados()