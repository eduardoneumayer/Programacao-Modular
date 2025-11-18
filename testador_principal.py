from testador_common import assert_true, assert_false, assert_equal, assert_file_exists, resumo
import carros
import principal
import os

def run():
    # Setup
    try:
        carros.reset()
        if os.path.exists("relatorio_oficina.csv"):
            os.remove("relatorio_oficina.csv")
    except:
        pass

    # PRI-01: Handle Carros
    # Teste adicionar via principal
    res = principal.handle_carros('adicionar', placa="ABC-1234", modelo="Fiat Uno", ano=2010)
    assert_true(res, "PRI-01: handle_carros adiciona veículo")
    # Teste buscar
    busca = principal.handle_carros('buscar', placa="ABC1234")
    assert_true(busca is not None, "PRI-01: handle_carros busca veículo")

    # PRI-02: Handle Serviços
    res = principal.handle_servicos('registrar', placa="ABC1234", descricao="Freio", valor=200.00)
    assert_true(res, "PRI-02: handle_servicos registra serviço")
    
    lst = principal.handle_servicos('listar', placa="ABC1234")
    assert_equal(len(lst), 1, "PRI-02: handle_servicos lista retorna tamanho 1")

    # PRI-03: Handle Financeiro
    # Adiciona mais um serviço de 100. Total deve ser 300.
    principal.handle_servicos('registrar', placa="ABC1234", descricao="Oleo", valor=100.00)
    
    total = principal.handle_financeiro('calcular_total', placa="ABC1234")
    assert_equal(total, 300.00, "PRI-03: handle_financeiro calcula total bruto")
    
    desc = principal.handle_financeiro('total_com_desconto', placa="ABC1234", percentual=10)
    # 10% de 300 = 30. Final = 270.
    assert_equal(desc, 270.00, "PRI-03: handle_financeiro calcula desconto")

    # PRI-04: Handle Validação
    assert_true(principal.handle_validacao('placa', 'ABC1D23'), "PRI-04: Valida placa Mercosul")
    assert_false(principal.handle_validacao('ano', 1900), "PRI-04: Valida ano invalido (muito antigo)")

    # PRI-05: Histórico Completo
    hist = principal.historico_carro("ABC1234")
    
    # --- CORREÇÃO AQUI: chaves atualizadas para 'total_servicos' e 'total_pago' ---
    assert_equal(hist['total_servicos'], 300.00, "PRI-05: Historico traz total de serviços correto")
    assert_equal(hist['total_pago'], 0.00, "PRI-05: Historico traz total pago zerado (ainda não pagou)")
    
    assert_equal(hist['dados_veiculo']['modelo'], "Fiat Uno", "PRI-05: Historico traz dados do carro")

    # PRI-06: Resumo Serviço
    res_dict = principal.resumo_servico("ABC1234")
    assert_equal(res_dict['qtd_servicos'], 2, "PRI-06: Resumo traz quantidade correta")
    
    # PRI-07: Exportar CSV
    res = principal.exportar_csv("relatorio_teste.csv")
    assert_true(res, "PRI-07: Função exportar retorna True")
    assert_file_exists("relatorio_teste.csv", "PRI-07: Arquivo CSV foi criado fisicamente")

    # Limpeza
    if os.path.exists("relatorio_teste.csv"):
        os.remove("relatorio_teste.csv")

    resumo()

if __name__ == "__main__":
    run()