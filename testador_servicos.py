from testador_common import assert_true, assert_false, assert_equal, resumo
import carros
import servicos

def run():
    # Setup: Limpa DB e cria um carro base para os testes
    try:
        carros.reset()
    except:
        pass # Caso nao exista reset
    
    carros.adiciona_carro("ABC-1234", "Gol", 2010)
    placa = "ABC1234"

    # SER-01: Registra serviço válido
    res = servicos.registra_servico(placa, "Troca de Oleo", 150.00)
    assert_true(res, "SER-01: Registra servico com sucesso")

    # SER-02: Registra em placa inexistente
    res = servicos.registra_servico("XYZ-9999", "Pneu", 100)
    assert_false(res, "SER-02: Falha ao registrar em placa inexistente")

    # SER-03: Listagem
    servicos.registra_servico(placa, "Alinhamento", 100.00) # Add mais um
    lista = servicos.lista_servico(placa)
    assert_equal(len(lista), 2, "SER-03: Lista deve conter 2 servicos")
    
    # Verifica conteúdo
    assert_equal(lista[0]['descricao'], "Troca de Oleo", "Descrição do servico 1 correta")

    # SER-04: Remoção válida (Remove o primeiro, indice 0)
    res = servicos.remove_servico(placa, 0)
    assert_true(res, "SER-04: Remove serviço existente")
    assert_equal(len(servicos.lista_servico(placa)), 1, "Lista diminuiu para 1 item")

    # SER-05: Remoção inválida (Indice fora da faixa)
    res = servicos.remove_servico(placa, 5)
    assert_false(res, "SER-05: Não remove índice inválido")

    # SER-06: Edição válida (Edita o que sobrou - Alinhamento)
    res = servicos.edita_servico(placa, 0, "Alinhamento 3D", 120.00)
    assert_true(res, "SER-06: Edita serviço com sucesso")
    item = servicos.lista_servico(placa)[0]
    assert_equal(item['valor'], 120.00, "Valor do serviço editado está correto")

    # SER-07: Edição com valor inválido
    res = servicos.edita_servico(placa, 0, "Erro", -50)
    assert_false(res, "SER-07: Não edita com valor negativo")

    resumo()

if __name__ == "__main__":
    run()