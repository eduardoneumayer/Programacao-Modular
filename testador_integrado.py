from testador_common import assert_true, assert_false, assert_equal, assert_file_exists, resumo
import carros
import principal
import os

def run():
    print("\n--- INICIANDO TESTE INTEGRADO (E2E) ---")
    
    # Setup: Limpa o banco para começar o teste do zero
    # (Isso é necessário para o teste ser previsível, mas no final vai sobrar dados)
    carros.reset() 
    if os.path.exists("saida.csv"):
        os.remove("saida.csv")

    # ====================================================================
    # PARTE 1: POPULANDO O SISTEMA (DOIS CARROS)
    # ====================================================================
    
    # Carro 1: O "Sobrevivente" (Toyota Corolla)
    # Este carro vai ficar no banco de dados no final para você conferir o JSON
    principal.handle_carros('adicionar', placa="PER-2025", modelo="Toyota Corolla", ano=2022)
    principal.handle_servicos('registrar', placa="PER-2025", descricao="Revisão 10k", valor=500)
    principal.handle_servicos('registrar', placa="PER-2025", descricao="Troca de Pastilha", valor=300)

    # Carro 2: A "Vítima" (Fiat Uno)
    # Este carro serve EXCLUSIVAMENTE para testar se a remoção funciona (INT-05)
    principal.handle_carros('adicionar', placa="DEL-0000", modelo="Fiat Uno", ano=2010)
    principal.handle_servicos('registrar', placa="DEL-0000", descricao="Troca de Oleo", valor=100)
    
    print(f"[INFO] Carros cadastrados. Iniciando validações...")

    # ====================================================================
    # PARTE 2: TESTES FINANCEIROS E DE FLUXO (INT-01 e INT-02)
    # ====================================================================
    
    # Testando total no Corolla (500 + 300 = 800)
    total = principal.handle_financeiro('calcular_total', placa="PER-2025")
    assert_equal(total, 800.00, "INT-01: Total acumulado do Corolla correto")

    # Testando desconto no Corolla (10% de 800 = 80 = 720 final)
    com_desc = principal.handle_financeiro('total_com_desconto', placa="PER-2025", percentual=10)
    assert_equal(com_desc, 720.00, "INT-02: Calculo com desconto correto")

    # ====================================================================
    # PARTE 3: TESTE DE REMOÇÃO DO CARRO (INT-05)
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
    # Nota: handle_servicos retorna lista vazia ou False se carro não existe, 
    # em ambos os casos confirma que não há dados acessíveis.
    vazio = (svcs_uno == []) or (svcs_uno is False)
    assert_true(vazio, "INT-05: Serviços do Uno inacessíveis/removidos")

    # ====================================================================
    # PARTE 4: VERIFICAÇÃO FINAL E EXPORTAÇÃO
    # ====================================================================

    # Garante que o Corolla (Sobrevivente) AINDA ESTÁ LÁ
    busca_corolla = principal.handle_carros('buscar', placa="PER-2025")
    assert_true(busca_corolla is not None, "PERSISTENCIA: O Corolla continua salvo após a remoção do Uno")

    # INT-04: Exportação de Dados
    # O CSV deve conter APENAS o Corolla, pois o Uno foi removido.
    principal.exportar_csv("saida.csv")
    assert_file_exists("saida.csv", "INT-04: Arquivo 'saida.csv' gerado com sucesso")

    print("\n[SUCESSO] Teste finalizado!")
    print(" -> Verifique 'banco_dados.json': Deve conter o Corolla.")
    print(" -> Verifique 'saida.csv': Deve conter o relatório do Corolla.")
    
    resumo()

if __name__ == "__main__":
    run()