# 🔧 Sistema de Gerenciamento de Oficina Mecânica

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Architecture](https://img.shields.io/badge/Arquitetura-Modular-orange.svg)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Tests-100%25-green.svg)

**Disciplina:** INF1040/INF1301 - Programação Modular (PUC-Rio)  
**Semestre:** 2025.2

---

## 📝 Sobre o Projeto

Este projeto consiste em um sistema completo para o gerenciamento de uma oficina mecânica, desenvolvido estritamente sob os paradigmas da **Programação Modular**.

A aplicação foi projetada para garantir **baixo acoplamento** e **alta coesão**, separando responsabilidades de interface, lógica de negócios, persistência de dados e validação. O sistema permite o controle total de veículos, ordens de serviço e fluxo de caixa, com persistência automática de dados.

### ✨ Destaques Funcionais
* **🖥️ Interface Interativa (CLI):** Sistema de menus navegáveis para operação completa via terminal (`app.py`).
* **🚗 Gestão de Frota:** Cadastro, busca, listagem e remoção de veículos com validação de placas (Mercosul/Antiga).
* **🛠️ Ordens de Serviço:** Registro de manutenções e peças vinculadas a cada veículo.
* **💰 Módulo Financeiro (PDV):** Cálculo de orçamentos, aplicação de descontos, taxas e **Checkout** (cobrança), com registro histórico de pagamentos.
* **💾 Persistência de Dados:** O sistema salva automaticamente o estado (veículos, serviços e pagamentos) em arquivo JSON. Os dados são recuperados automaticamente a cada execução.
* **📊 Relatórios Gerenciais:** Exportação de planilha CSV consolidada com totais de serviços e valores arrecadados por veículo.

---

## 📂 Arquitetura do Sistema

O projeto está estruturado em camadas lógicas, respeitando o encapsulamento de estruturas de dados (TADs).

| Arquivo | Camada/Tipo | Responsabilidade |
| :--- | :--- | :--- |
| **`app.py`** | **View (Interface)** | Camada de apresentação. Gerencia os menus e a interação com o usuário. **Não contém regra de negócio**, apenas delega para o controlador. |
| **`principal.py`** | **Controller (Facade)** | O "Maestro" do sistema. Coordena as chamadas entre os módulos, gerencia a inicialização e a exportação de dados. |
| **`carros.py`** | **Model (TAD)** | Gerencia o banco de dados em memória e a persistência em disco (`banco_dados.json`). **Encapsula** rigorosamente o acesso aos dados; nenhum outro módulo acessa o dicionário global. |
| **`servicos.py`** | **Model Logic** | Gerencia a lógica de manipulação de serviços. Comunica-se com `carros.py` exclusivamente através de funções de acesso públicas (`anexar_servico_interno`), mantendo o encapsulamento. |
| **`financeiro.py`** | **Domain Logic** | Biblioteca de funções puras para cálculos matemáticos (totais, descontos, taxas, cálculo líquido). |
| **`validacao.py`** | **Utility** | Utilitários para validação de entradas (Regex de placas, consistência de ano). |

---

## ✅ Critérios de Avaliação Atendidos

O desenvolvimento seguiu rigorosamente a checklist de avaliação da disciplina:

1.  **Aplicação Funcionando:** O sistema executa o fluxo completo (Cadastro -> Serviço -> Pagamento -> Relatório) sem erros, tratando exceções de entrada.
2.  **Testes Automatizados (TDD):** Suíte de testes completa cobrindo cenários de sucesso e falha para todos os módulos.
3.  **Especificação:** Todas as funções públicas possuem documentação (*Docstrings*) e tipagem (*Type Hints*).
4.  **Modularização de TADs:**
    * O dicionário `_DB` é privado ao módulo `carros.py`.
    * **Zero violações de encapsulamento:** O módulo `servicos.py` não importa nem acessa a estrutura de dados diretamente.
5.  **Persistência:**
    * Gravação automática em `banco_dados.json` a cada operação de escrita (CRUD ou Pagamento).
    * Carregamento automático na inicialização.

---

## 🚀 Instruções de Uso

Certifique-se de ter o **Python 3** instalado.

### 1. Modo Interativo (Usuário Final)
Para utilizar o sistema no dia a dia:

```bash
python3 app.py