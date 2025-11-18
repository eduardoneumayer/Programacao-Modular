from testador_common import assert_true, assert_false, assert_equal, assert_file_exists, resumo
import carros
import principal
import os

def run():
    print("\n--- INICIANDO TESTE INTEGRADO (E2E) ---")
    
    # Limpeza inicial
    try:
        carros.reset()
        if os.path.exists("saida.csv"):
            os.remove("saida.csv")
    except:
        pass

    # INT-01: Fluxo de Uso Completo
    # 1. Adicionar Carro
    principal.handle_carros('adicionar', placa="XYZ-5555", modelo="Corolla", ano=2020)
    
    # 2. Registrar Serviços (3 serviços: 100 + 200 + 300 = 600)
    principal.handle_servicos('registrar', placa="XYZ-5555", descricao="Svc 1", valor=100)
    principal.handle_servicos('registrar', placa="XYZ-5555", descricao="Svc 2", valor=200)
    principal.handle_servicos('registrar', placa="XYZ-5555", descricao="Svc 3", valor=300)
    
    # 3. Verificar Total
    total = principal.handle_financeiro('calcular_total', placa="XYZ-5555")
    assert_equal(total, 600.00, "INT-01: Total acumulado correto")

    # INT-02: Financeiro Completo (Desconto e Taxa)
    # Aplicar 50% de desconto -> deve ir para 300
    com_desc = principal.handle_financeiro('total_com_desconto', placa="XYZ-5555", percentual=50)
    assert_equal(com_desc, 300.00, "INT-02: Calculo com desconto no fluxo")

    # INT-03: Remoção Segura de Serviço
    # Remover o serviço do meio (index 1, valor 200). Sobram 100 e 300 -> Total 400.
    principal.handle_servicos('remover', placa="XYZ-5555", indice=1)
    novo_total = principal.handle_financeiro('calcular_total', placa="XYZ-5555")
    assert_equal(novo_total, 400.00, "INT-03: Total atualizado após remoção de serviço")

    # INT-04: Exportação de Dados
    principal.exportar_csv("saida.csv")
    assert_file_exists("saida.csv", "INT-04: CSV gerado no final do fluxo")

    # INT-05: Consistência na Remoção do Carro
    # Ao remover o carro, ele deve sumir da busca
    principal.handle_carros('remover', placa="XYZ-5555")
    carro = principal.handle_carros('buscar', placa="XYZ-5555")
    assert_equal(carro, None, "INT-05: Carro removido do sistema")
    
    # Tentar listar serviços de carro removido deve retornar vazio
    svcs = principal.handle_servicos('listar', placa="XYZ-5555")
    assert_equal(len(svcs), 0, "INT-05: Serviços inacessíveis após remoção do carro")

    # Limpeza final
    if os.path.exists("saida.csv"):
        os.remove("saida.csv")

    resumo()

if __name__ == "__main__":
    run()