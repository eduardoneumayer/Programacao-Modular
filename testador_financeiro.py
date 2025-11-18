from testador_common import assert_true, assert_false, assert_equal, resumo
import financeiro

def run():
    lista_vazia = []
    lista_cheia = [
        {"descricao": "A", "valor": 100.00},
        {"descricao": "B", "valor": 200.00}
    ] # Soma esperada: 300.00

    # FIN-01: Total lista vazia
    val = financeiro.calcula_total(lista_vazia)
    assert_equal(val, 0.00, "FIN-01: Total de lista vazia é 0.00")

    # FIN-02: Total correto
    val = financeiro.calcula_total(lista_cheia)
    assert_equal(val, 300.00, "FIN-02: Soma dos serviços correta (300.00)")

    # FIN-03: Desconto
    # 10% de 100 = 10. Final = 90.
    res = financeiro.aplica_desconto(100.00, 10)
    assert_equal(res, 90.00, "FIN-03: Aplica desconto de 10% corretamente")
    
    # Desconto de 100% (Gratis)
    res = financeiro.aplica_desconto(100.00, 100)
    assert_equal(res, 0.00, "FIN-03: Aplica desconto de 100% corretamente")

    # FIN-04: Desconto inválido
    res = financeiro.aplica_desconto(100.00, -5)
    assert_false(res, "FIN-04: Desconto negativo retorna False")
    res = financeiro.aplica_desconto(100.00, 150)
    assert_false(res, "FIN-04: Desconto > 100% retorna False")

    # FIN-05: Taxa
    # 10% de 100 = 10. Final = 110.
    res = financeiro.aplica_taxa(100.00, 10)
    assert_equal(res, 110.00, "FIN-05: Aplica taxa de 10% corretamente")

    # FIN-06: Taxa inválida
    res = financeiro.aplica_taxa(100.00, -10)
    assert_false(res, "FIN-06: Taxa negativa retorna False")

    resumo()

if __name__ == "__main__":
    run()