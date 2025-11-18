from testador_common import assert_true, assert_false, assert_equal, resumo
import validacao

def run():
    # Placas
    assert_true(validacao.valida_placa("ABC-1234"), "placa tradicional com hífen válida")
    assert_true(validacao.valida_placa("ABC1234"),  "placa tradicional sem hífen válida")
    assert_true(validacao.valida_placa("ABC1D23"),  "placa Mercosul válida")
    assert_false(validacao.valida_placa("A1C-12D4"), "placa inválida mistura fora do padrão")
    assert_equal(validacao.normaliza_placa("abc-1234"), "ABC1234", "normaliza para maiúsculo sem hífen")

    # Ano
    assert_true(validacao.valida_ano(1980), "ano limite inferior ok")
    assert_false(validacao.valida_ano(0), "ano 0 inválido")

    # Pacote de carro
    assert_true(validacao.valida_carro("ABC1234", "Civic", 2015), "valida_carro com dados válidos")
    assert_false(validacao.valida_carro("AAAAAAA", "", 2015), "modelo vazio => inválido")
    resumo()

if __name__ == "__main__":
    run()