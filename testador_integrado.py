from testador_common import assert_true, assert_false, assert_equal, assert_file_exists, resumo
import carros
import principal
import os

def run():
    print("\n--- INICIANDO TESTE INTEGRADO (E2E) ---")
    
    # Setup: Limpa o banco para começar o teste do zero
    carros.reset() 
    if os.path.exists("saida.csv"):
        os.remove("saida.csv")

    # ====================================================================
    # PARTE 1: POPULANDO O SISTEMA (DOIS CARROS)
    # ====================================================================
    
    # Carro 1: O "Cliente Fiel" (Toyota Corolla)
    # Este carro fará serviços, pagará e ficará no banco de dados.
    principal.handle_carros('adicionar', placa="PER-2025", modelo="Toyota Corolla", ano=2022)
    principal.handle_servicos('registrar', placa="PER-2025", descricao="Revisão 10k", valor=500)
    principal.handle_servicos('registrar', placa="PER-2025", descricao="Troca de Pastilha", valor=300)
    # Total Bruto Esperado: 800.00

    # Carro 2: A "Vítima" (Fiat Uno)
    # Este carro serve EXCLUSIVAMENTE para testar se a remoção funciona (INT-05)
    principal.handle_carros('adicionar', placa="DEL-0000", modelo="Fiat Uno", ano=2010)
    principal.handle_servicos('registrar', placa="DEL-0000", descricao="Troca de Oleo", valor=100)
    
    print(f"[INFO] Carros cadastrados. Iniciando validações...")

    # ====================================================================
    # PARTE 2: TESTES FINANCEIROS E DE FLUXO (INT-01 e INT-02)
    # ====================================================================
    
    # Testando total bruto no Corolla (500 + 300 = 800)
    total = principal.handle_financeiro('calcular_total', placa="PER-2025")
    assert_equal(total, 800.00, "INT-01: Total acumulado do Corolla correto")

    # Testando apenas desconto (10% de 800 = 80 = 720 final)
    com_desc = principal.handle_financeiro('total_com_desconto', placa="PER-2025", percentual=10)
    assert_equal(com_desc, 720.00, "INT-02a: Calculo com desconto correto")
    
    # INT-02b: Cálculo Líquido Completo (Simulação de Checkout)
    # Valor: 800. Desconto: 10% (-80). Taxa: 0%.
    # Esperado: 800 - 80 = 720.00
    liquido = principal.handle_financeiro('calcular_liquido', 
                                          placa="PER-2025", 
                                          desc_perc=10, 
                                          taxa_perc=0)
    assert_equal(liquido, 720.00, "INT-02b: Cálculo liquido (Checkout) correto")

    # ====================================================================
    # PARTE 3: PAGAMENTO E PERSISTÊNCIA (NOVO CENÁRIO)
    # ====================================================================
    print("[INFO] Realizando pagamento do Corolla...")

    # 1. Efetua o pagamento de 720.00
    principal.handle_financeiro('registrar_pagamento', placa="PER-2025", valor=liquido)

    # 2. Verifica se o dinheiro entrou no histórico do carro
    carro_pos_pgto = principal.handle_carros('buscar', placa="PER-2025")
    assert_equal(carro_pos_pgto['total_pago'], 720.00, "INT-03: Valor salvo no histórico 'total_pago'")

    # 3. Verifica regra de negócio: Serviços NÃO devem ser apagados após pagar
    svcs_restantes = principal.handle_servicos('listar', placa="PER-2025")
    assert_equal(len(svcs_restantes), 2, "INT-04: Serviços mantidos após pagamento (Regra de Negócio)")

    # ====================================================================
    # PARTE 4: TESTE DE REMOÇÃO DO CARRO (INT-05)
    # ====================================================================
    
    print("[INFO] Testando remoção do Fiat Uno (Vítima)...")
    
    # Remove o Uno
    removido = principal.handle_carros('remover', placa="DEL-0000")
    assert_true(removido, "INT-05: Comando de remover retornou sucesso")

    # Verifica se o Uno sumiu
    busca_uno = principal.handle_carros('buscar', placa="DEL-0000")
    assert_equal(busca_uno, None, "INT-05: Uno não existe mais no sistema")

    # Verifica se os serviços do Uno sumiram (limpeza em cascata)
    svcs_uno = principal.handle_servicos('listar', placa="DEL-0000")
    vazio = (svcs_uno == []) or (svcs_uno is False)
    assert_true(vazio, "INT-05: Serviços do Uno inacessíveis/removidos")

    # ====================================================================
    # PARTE 5: VERIFICAÇÃO FINAL E EXPORTAÇÃO
    # ====================================================================

    # Garante que o Corolla (Sobrevivente) AINDA ESTÁ LÁ
    busca_corolla = principal.handle_carros('buscar', placa="PER-2025")
    assert_true(busca_corolla is not None, "PERSISTENCIA: O Corolla continua salvo após a remoção do Uno")

    # INT-04: Exportação de Dados
    # O CSV deve conter APENAS o Corolla, com Total Pago preenchido.
    principal.exportar_csv("saida.csv")
    assert_file_exists("saida.csv", "INT-04: Arquivo 'saida.csv' gerado com sucesso")

    print("\n[SUCESSO] Teste finalizado!")
    print(" -> Verifique 'banco_dados.json': Deve conter o Corolla com total_pago=720.")
    print(" -> Verifique 'saida.csv': Deve conter as colunas de Total Serviços e Total Pago.")
    
    resumo()

if __name__ == "__main__":
    run()