# Sistema de Gerenciamento de Oficina Mecânica 🚗🔧

**Disciplina:** INF1040/INF1301 - Programação Modular (PUC-Rio)  
**Linguagem:** Python 3 (Puro)

## 📝 Sobre o Projeto

Este projeto consiste em um sistema modular desenvolvido em Python para o gerenciamento de uma oficina mecânica. O objetivo é permitir o controle completo de veículos, ordens de serviço e cálculos financeiros de forma organizada e escalável.

A aplicação foi projetada com base nos princípios da **programação modular**, dividindo suas responsabilidades em componentes independentes (baixo acoplamento) coordenados por um módulo principal.

### Funcionalidades Principais
- **Cadastro de Veículos:** Inclusão, busca, listagem e remoção (CRUD).
- **Gestão de Serviços:** Registro de manutenções atreladas a veículos.
- **Módulo Financeiro:** Cálculo automático de totais, aplicação de descontos e taxas.
- **Validação de Dados:** Verificação de placas (padrão Mercosul e antigo) e anos de fabricação.
- **Relatórios:** Exportação de dados consolidados para arquivo CSV.

---

## 📂 Estrutura do Projeto

O projeto está organizado em módulos funcionais e seus respectivos testadores unitários/integrados:

| Arquivo | Responsabilidade |
| :--- | :--- |
| `carros.py` | Banco de dados em memória e gestão de veículos. |
| `servicos.py` | Gestão das listas de serviços vinculadas aos carros. |
| `financeiro.py` | Lógica de cálculos matemáticos (somas, descontos, taxas). |
| `validacao.py` | Regras de negócio para validação de entradas (Regex, Datas). |
| `principal.py` | **Maestro do sistema**. Coordena as chamadas entre módulos e gera o CSV. |
| `testador_*.py` | Scripts de teste automatizados (veja seção abaixo). |
| `testador_common.py` | Utilitários para padronização dos logs de teste. |

---

## 🧪 Estratégia de Testes (TDD)

O desenvolvimento seguiu rigorosamente a metodologia **TDD (Test-Driven Development)**. Isso significa que os testes foram planejados para validar cada função isoladamente antes e durante a integração.

Não foram utilizados frameworks externos (como `pytest` ou `unittest`); toda a suíte de testes foi implementada em Python puro para fins didáticos.

### Como Executar os Testes

Para validar o funcionamento do sistema, execute os comandos abaixo no seu terminal, dentro da pasta do projeto:

#### 1. Testes Unitários (Por Módulo)
Validam a lógica interna de cada componente isoladamente.

```bash
# Testa validação de placas e anos
python3 testador_validacao.py

# Testa o cadastro e busca de carros
python3 testador_carros.py

# Testa registro e edição de serviços
python3 testador_servicos.py

# Testa cálculos matemáticos
python3 testador_financeiro.py