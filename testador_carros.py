from testador_common import assert_true, assert_false, assert_equal, resumo
import carros

def run():
    print("--- Teste Unitário: Carros & Persistência ---")
    carros.reset()

    # 1. Criação Básica
    assert_true(carros.adiciona_carro("PAG-9999", "Teste Pag", 2022), "Adiciona carro")
    
    # 2. Teste do Campo 'total_pago'
    c = carros.busca_carro("PAG-9999")
    assert_equal(c['total_pago'], 0.0, "Carro novo nasce com total_pago = 0")

    # 3. Registrar Pagamento (Simulando acesso interno ou via principal)
    # Vamos testar a função interna do módulo carros
    carros.registrar_pagamento_interno("PAG-9999", 150.00)
    
    c = carros.busca_carro("PAG-9999")
    assert_equal(c['total_pago'], 150.00, "Primeiro pagamento registrado")

    # 4. Acumular Pagamento (Pagar mais uma vez)
    carros.registrar_pagamento_interno("PAG-9999", 50.00)
    
    c = carros.busca_carro("PAG-9999")
    assert_equal(c['total_pago'], 200.00, "Segundo pagamento acumulado corretamente")

    resumo()

if __name__ == "__main__":
    run()