import csv
import os 
import carros
import servicos
import financeiro
import validacao

# Inicialização
carros.carregar_dados()

def handle_carros(operacao: str, **kwargs):
    if operacao == 'adicionar':
        return carros.adiciona_carro(kwargs.get('placa'), kwargs.get('modelo'), kwargs.get('ano'))
    elif operacao == 'listar':
        return carros.lista_carro()
    elif operacao == 'buscar':
        return carros.busca_carro(kwargs.get('placa'))
    elif operacao == 'remover':
        return carros.remove_carro(kwargs.get('placa'))
    return None

def handle_servicos(operacao: str, **kwargs):
    placa = kwargs.get('placa')
    if not carros.busca_carro(placa):
        return [] if operacao == 'listar' else False

    if operacao == 'registrar':
        return servicos.registra_servico(placa, kwargs.get('descricao'), kwargs.get('valor'))
    elif operacao == 'listar':
        return servicos.lista_servico(placa)
    elif operacao == 'remover':
        return servicos.remove_servico(placa, kwargs.get('indice'))
    return None

def handle_financeiro(operacao: str, **kwargs):
    placa = kwargs.get('placa')
    
    # Cálculos baseados na lista atual de serviços
    lista_svcs = servicos.lista_servico(placa)
    total_bruto = financeiro.calcula_total(lista_svcs)
    
    if operacao == 'calcular_total':
        return total_bruto
    
    elif operacao == 'total_com_desconto':
        return financeiro.aplica_desconto(total_bruto, kwargs.get('percentual', 0))
    
    elif operacao == 'total_com_taxa':
        return financeiro.aplica_taxa(total_bruto, kwargs.get('percentual', 0))
        
    elif operacao == 'calcular_liquido':
        # Usa o módulo financeiro puro para fazer a conta
        return financeiro.calcular_liquido(
            total_bruto, 
            kwargs.get('desc_perc', 0), 
            kwargs.get('taxa_perc', 0)
        )
    
    # --- NOVO: Registra o pagamento no histórico do carro ---
    elif operacao == 'registrar_pagamento':
        valor = kwargs.get('valor', 0.0)
        return carros.registrar_pagamento_interno(placa, valor)
        
    return 0.0

def handle_validacao(tipo: str, valor) -> bool:
    if tipo == 'placa':
        return validacao.valida_placa(valor)
    elif tipo == 'ano':
        return validacao.valida_ano(valor)
    return False

def historico_carro(placa: str) -> dict:
    carro = carros.busca_carro(placa)
    if not carro:
        return {}
    svcs = servicos.lista_servico(placa)
    return {
        "dados_veiculo": carro,
        "historico_servicos": svcs,
        "total_servicos": financeiro.calcula_total(svcs),
        "total_pago": carro.get("total_pago", 0.0)
    }

def resumo_servico(placa: str) -> dict:
    svcs = servicos.lista_servico(placa)
    return {
        "placa": placa,
        "qtd_servicos": len(svcs),
        "total": financeiro.calcula_total(svcs),
        "descricoes": [s['descricao'] for s in svcs]
    }

def exportar_csv(nome_arquivo: str = "relatorio_oficina.csv") -> bool:
    lista_veiculos = carros.lista_carro()
    if not lista_veiculos:
        return False
        
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(diretorio_atual, nome_arquivo)
        
        print(f"Salvando arquivo em: {caminho_completo}")

        with open(caminho_completo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # --- ALTERADO: Adicionado Coluna TOTAL PAGO ---
            writer.writerow(['Placa', 'Modelo', 'Ano', 'Qtd Servicos', 'Total em Servicos', 'Total Pago (Caixa)'])
            
            for veiculo in lista_veiculos:
                p = veiculo['placa']
                svcs = servicos.lista_servico(p)
                total_servicos = financeiro.calcula_total(svcs)
                total_pago = veiculo.get('total_pago', 0.0)
                
                writer.writerow([
                    p,
                    veiculo['modelo'],
                    veiculo['ano'],
                    len(svcs),
                    f"{total_servicos:.2f}",
                    f"{total_pago:.2f}"
                ])
        return True
    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")
        return False