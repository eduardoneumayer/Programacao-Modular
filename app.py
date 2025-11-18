import os
import sys
import time
import principal

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def cabecalho(titulo):
    limpar_tela()
    print("=" * 50)
    print(f"{titulo:^50}")
    print("=" * 50)

def pausar():
    print("\n")
    input("Pressione [ENTER] para continuar...")

def msg_erro(mensagem):
    print(f"\n❌ ERRO: {mensagem}")
    time.sleep(0.5)
    pausar()

# ... (MANTENHA AS FUNÇÕES menu_carros E menu_servicos IGUAIS AO ANTERIOR) ...
# Vou repetir apenas o menu_financeiro modificado e o menu_carros/servicos encurtados 
# para caber na resposta, mas você pode manter o código antigo deles se quiser, 
# ou copiar tudo abaixo que é o arquivo completo.

def menu_carros():
    while True:
        cabecalho("GESTÃO DE CARROS")
        print("[1] Adicionar Carro")
        print("[2] Listar Carros")
        print("[3] Buscar Carro")
        print("[4] Remover Carro")
        print("[0] Voltar")
        print("-" * 50)
        op = input("Escolha uma opção: ")
        if op == '0': break
        elif op == '1':
            print("\n--- Novo Carro ---")
            placa = input("Placa: ")
            modelo = input("Modelo: ")
            try:
                if principal.handle_carros('adicionar', placa=placa, modelo=modelo, ano=int(input("Ano: "))):
                    print(f"\n✅ Sucesso! Veículo cadastrado.")
                else: msg_erro("Dados inválidos ou duplicado.")
            except ValueError: msg_erro("Ano inválido.")
            pausar()
        elif op == '2':
            lista = principal.handle_carros('listar')
            if not lista: print("Vazio.")
            else:
                print(f"{'PLACA':<10} | {'MODELO':<15} | {'TOT. PAGO'}")
                print("-" * 45)
                for c in lista:
                    print(f"{c['placa']:<10} | {c['modelo']:<15} | R$ {c.get('total_pago', 0):.2f}")
            pausar()
        elif op == '3':
            placa = input("Placa: ")
            c = principal.handle_carros('buscar', placa=placa)
            if c: 
                print(f"\nModelo: {c['modelo']} | Ano: {c['ano']}")
                print(f"Total já pago em histórico: R$ {c.get('total_pago',0):.2f}")
            else: msg_erro("Não encontrado.")
            pausar()
        elif op == '4':
            placa = input("Placa para remover: ")
            if principal.handle_carros('remover', placa=placa): print("✅ Removido.")
            else: msg_erro("Erro.")
            pausar()

def menu_servicos():
    while True:
        cabecalho("GESTÃO DE SERVIÇOS")
        placa = input("Placa (0 voltar): ")
        if placa == '0': break
        if not principal.handle_carros('buscar', placa=placa): 
            msg_erro("Não encontrado.")
            continue
        while True:
            cabecalho(f"SERVIÇOS: {placa}")
            print("[1] Registrar | [2] Listar | [3] Remover | [0] Voltar")
            op = input("Opção: ")
            if op == '0': break
            if op == '1':
                desc = input("Descrição: ")
                try: 
                    if principal.handle_servicos('registrar', placa=placa, descricao=desc, valor=float(input("Valor: "))):
                        print("✅ Registrado.")
                except: msg_erro("Valor inválido.")
            elif op == '2':
                lista = principal.handle_servicos('listar', placa=placa)
                for s in lista: print(f"R$ {s['valor']:<10} - {s['descricao']}")
                pausar()
            elif op == '3':
                try:
                    if principal.handle_servicos('remover', placa=placa, indice=int(input("ID: "))): print("✅ Removido")
                except: msg_erro("Erro ID.")

def menu_financeiro():
    cabecalho("MÓDULO FINANCEIRO (PDV)")
    placa = input("Digite a placa (ou 0 para sair): ")
    if placa == '0': return

    carro = principal.handle_carros('buscar', placa=placa)
    if not carro:
        msg_erro("Veículo não encontrado.")
        return

    perc_desc = 0.0
    perc_taxa = 0.0

    while True:
        # Valores atuais
        bruto = principal.handle_financeiro('calcular_total', placa=placa)
        liquido = principal.handle_financeiro('calcular_liquido', placa=placa, desc_perc=perc_desc, taxa_perc=perc_taxa)
        
        if liquido == -1.0: liquido = bruto

        cabecalho(f"CAIXA: {carro['modelo']} ({carro['placa']})")
        print(f"Total Serviços (Bruto):   R$ {bruto:.2f}")
        print(f"Desconto ({perc_desc}%):         -R$ {bruto * (perc_desc/100):.2f}")
        print(f"Taxa ({perc_taxa}%):             +R$ {bruto * (perc_taxa/100):.2f}")
        print("-" * 40)
        print(f"A RECEBER (Líquido):      R$ {liquido:.2f}")
        print("=" * 40)
        print(f"Histórico Total Pago:     R$ {carro.get('total_pago', 0):.2f}")
        print("-" * 40)
        
        print("[1] Definir Desconto | [2] Definir Taxa | [3] CONFIRMAR PAGAMENTO | [0] Voltar")
        op = input("Opção: ")

        if op == '0': break
        elif op == '1': perc_desc = float(input("Desconto %: "))
        elif op == '2': perc_taxa = float(input("Taxa %: "))
        elif op == '3':
            # REGISTRA O PAGAMENTO
            principal.handle_financeiro('registrar_pagamento', placa=placa, valor=liquido)
            
            print("\n✅ Pagamento registrado com sucesso!")
            print(f"Valor de R$ {liquido:.2f} adicionado ao histórico do carro.")
            
            # NÃO APAGA OS SERVIÇOS AUTOMATICAMENTE
            # Mantém eles lá para o CSV sair com "Qtd Servicos" e "Total Servicos" preenchidos
            print("Os serviços permanecem na lista para conferência no relatório.")
            
            # Atualiza o objeto carro local para mostrar o novo total pago na tela
            carro = principal.handle_carros('buscar', placa=placa)
            
            # Reseta descontos para próxima operação
            perc_desc = 0.0
            perc_taxa = 0.0
            pausar()

def menu_relatorios():
    cabecalho("RELATÓRIOS")
    if input("[1] Gerar CSV Geral (Enter confirma): ") == '1':
        if principal.exportar_csv("relatorio_oficina.csv"):
            print(f"\n✅ CSV Gerado em: {os.getcwd()}/relatorio_oficina.csv")
        else: print("Erro.")
        pausar()

def main():
    while True:
        cabecalho("OFICINA v3.0 - FINAL")
        print("[1] Carros | [2] Serviços | [3] Caixa | [4] Relatório | [0] Sair")
        op = input("Op: ")
        if op=='1': menu_carros()
        elif op=='2': menu_servicos()
        elif op=='3': menu_financeiro()
        elif op=='4': menu_relatorios()
        elif op=='0': sys.exit()

if __name__ == "__main__":
    main()