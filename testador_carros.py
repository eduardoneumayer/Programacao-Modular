from testador_common import assert_true, assert_false, assert_equal, resumo
import carros

def run():
    # Cenário limpo
    try:
        carros.reset()
    except Exception:
        pass

    # Adicionar
    assert_true(carros.adiciona_carro("ABC-1234", "Civic", 2015), "adiciona_carro primeira vez")
    assert_false(carros.adiciona_carro("ABC1234", "Civic", 2015), "adiciona_carro duplicado (mesma placa)")

    # Listar
    lst = carros.lista_carro()
    assert_true(len(lst) == 1 and lst[0]["placa"] == "ABC1234", "lista_carro contém o carro cadastrado")

    # Buscar
    achado = carros.busca_carro("ABC1234")
    assert_equal(achado["modelo"], "Civic", "busca_carro retorna dados corretos")
    assert_equal(carros.busca_carro("NAOEXISTE"), None, "busca_carro inexistente retorna None")

    # Remover
    assert_false(carros.remove_carro("ZZZ9999"), "remove_carro inexistente => False")
    assert_true(carros.remove_carro("ABC-1234"), "remove_carro existente => True")
    assert_equal(carros.busca_carro("ABC1234"), None, "após remoção, carro não deve existir")

    resumo()

if __name__ == "__main__":
    run()