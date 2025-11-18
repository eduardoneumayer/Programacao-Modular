"""
Módulo: validacao
Responsável por validar e normalizar entradas (placa, ano, dados do carro).
"""

import re
from datetime import date

# Aceita formatos tradicionais (ABC-1234) e Mercosul (ABC1D23)
_PLACA_TRAD = re.compile(r"^[A-Z]{3}-?\d{4}$")
_PLACA_MERC = re.compile(r"^[A-Z]{3}\d[A-Z]\d{2}$")

def normaliza_placa(placa: str) -> str:
    """
    Remove hífen e coloca em maiúsculo. Não valida formato.
    """
    if not isinstance(placa, str):
        return ""
    return placa.replace("-", "").upper().strip()

def valida_placa(placa: str) -> bool:
    """
    Valida formato de placa (tradicional ou Mercosul).
    Aceita com ou sem hífen; internamente normaliza para checagem.
    """
    if not isinstance(placa, str) or not placa.strip():
        return False
    p = placa.upper().strip()
    return bool(_PLACA_TRAD.match(p) or _PLACA_MERC.match(p.replace("-", "")))

def valida_ano(ano: int, *, minimo: int = 1980) -> bool:
    """
    Ano válido entre 'minimo' e ano corrente (inclusivos).
    """
    if not isinstance(ano, int):
        return False
    atual = date.today().year
    return minimo <= ano <= atual

def valida_carro(placa: str, modelo: str, ano: int) -> bool:
    """
    Conjunto mínimo para cadastro de carro.
    - placa válida (qualquer dos padrões)
    - modelo não vazio
    - ano no intervalo permitido
    """
    if not isinstance(modelo, str) or not modelo.strip():
        return False
    return valida_placa(placa) and valida_ano(ano)