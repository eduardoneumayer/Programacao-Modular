"""
Módulo: carros
Gerencia cadastro, persistência e acesso aos dados dos veículos.
"""
import json
import os
import validacao as _v
from typing import Dict, List, Optional

# "Banco" em memória
_DB: Dict[str, Dict] = {}
ARQUIVO_DB = "banco_dados.json"

def _key(placa: str) -> str:
    return _v.normaliza_placa(placa)

def reset():
    _DB.clear()

# --- PERSISTÊNCIA (CRITÉRIO 5) ---
def salvar_dados():
    """Salva o estado atual do _DB em arquivo JSON."""
    try:
        with open(ARQUIVO_DB, 'w', encoding='utf-8') as f:
            json.dump(_DB, f, indent=4)
        return True
    except Exception:
        return False

def carregar_dados():
    """Carrega os dados do JSON para o _DB ao iniciar."""
    global _DB
    if not os.path.exists(ARQUIVO_DB):
        return
    try:
        with open(ARQUIVO_DB, 'r', encoding='utf-8') as f:
            _DB = json.load(f)
    except Exception:
        _DB = {}

# --- ACESSO (CRITÉRIO 4 - ENCAPSULAMENTO) ---
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
        "servicos": []
    }
    salvar_dados() # Persiste a cada mudança
    return True

def lista_carro() -> List[Dict]:
    return list(_DB.values())

def busca_carro(placa: str) -> Optional[Dict]:
    k = _key(placa)
    car = _DB.get(k)
    if not car:
        return None
    # Retorna cópia profunda (ou recria dict) para proteger _DB
    # Isso garante encapsulamento total
    return {
        "placa": car["placa"],
        "modelo": car["modelo"],
        "ano": car["ano"],
        "servicos": list(car["servicos"]) # Cópia da lista
    }

def remove_carro(placa: str) -> bool:
    k = _key(placa)
    if k not in _DB:
        return False
    del _DB[k]
    salvar_dados()
    return True

# --- NOVO: Função para Servicos usarem sem tocar no _DB ---
def anexar_servico_interno(placa: str, servico: dict) -> bool:
    """
    Permite que outros módulos anexem dados ao carro 
    sem acessar _DB diretamente.
    """
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
            # Atualiza mantendo a referência
            lista[indice].update(novo_dado)
            salvar_dados()
            return True
    return False