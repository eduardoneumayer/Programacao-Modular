# Utilitários mínimos para padronizar relatórios dos testadores
import math, os

TOTAL = {"ok": 0, "fail": 0}

def _ok(msg): print("OK  -", msg); TOTAL["ok"] += 1
def _fail(msg, obtido, esperado): print("FAIL-", msg, f"(obtido={obtido}, esperado={esperado})"); TOTAL["fail"] += 1

def assert_equal(obtido, esperado, msg=""):
    if obtido == esperado or (isinstance(esperado, float) and math.isclose(obtido, esperado, rel_tol=1e-9, abs_tol=1e-2)):
        _ok(msg)
    else:
        _fail(msg, obtido, esperado)

def assert_true(cond, msg=""):  assert_equal(bool(cond), True, msg)
def assert_false(cond, msg=""): assert_equal(bool(cond), False, msg)

def assert_file_exists(path, msg=""):
    try:
        ok = os.path.exists(path) and os.path.getsize(path) > 0
    except Exception:
        ok = False
    assert_true(ok, msg)

def resumo():
    print("\n--- RESUMO ---")
    print(f"Passaram: {TOTAL['ok']}  |  Falharam: {TOTAL['fail']}")
    return dict(TOTAL)