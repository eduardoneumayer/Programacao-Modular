# 📄 README – Pessoa 1

## 📂 Módulos e Testadores
- **Módulos**: `validacao.py` e `carros.py`
- **Testadores**: `testador_validacao.py` e `testador_carros.py`

Este README documenta exclusivamente a parte desenvolvida pelo **Integrante 1** do grupo, referente aos módulos **Validação** e **Carros**, além dos respectivos programas testadores implementados em Python puro, seguindo as regras da disciplina de **Programação Modular**.

---

## 🚀 Visão Geral

Nesta parte do projeto, foram implementados:

### ✅ Módulos de Código

#### `validacao.py`
Responsável por validar e normalizar entradas da aplicação, incluindo:
- Formato de placa (tradicional e Mercosul)
- Ano do veículo
- Conjunto mínimo de dados para cadastro de carro

#### `carros.py`
Realiza a gestão de veículos cadastrados, com as seguintes funcionalidades:
- Cadastro
- Listagem
- Busca
- Remoção

Ambos os módulos seguem o princípio da **programação modular**, sem uso de classes ou frameworks externos.

---

## 🧪 Programas Testadores

Cada módulo possui seu próprio arquivo de testes:

| **Módulo**      | **Testador**            | **Conteúdo**                                      |
|------------------|-------------------------|--------------------------------------------------|
| `validacao.py`   | `testador_validacao.py` | Testes para placa, ano e estrutura mínima do carro |
| `carros.py`      | `testador_carros.py`    | Testes para cadastro, listagem, busca e remoção  |

Os testadores possuem um relatório padronizado (**OK/FAIL**) e utilizam o arquivo auxiliar `testador_common.py`.

---

## ▶️ Como Executar os Testes

1. Certifique-se de que os arquivos estão no mesmo diretório:
   - `validacao.py`  
   - `carros.py`  
   - `testador_validacao.py`  
   - `testador_carros.py`  
   - `testador_common.py`  

2. Execute os testadores via terminal:
   ```bash
   python testador_validacao.py
   python testador_carros.py
   ```

3. Saída esperada no console:
   ```
   OK  - placa tradicional com hífen válida
   OK  - normaliza para maiúsculo sem hífen
   OK  - valida_carro com dados válidos
   ...

   --- RESUMO ---
   Passaram: X  |  Falharam: Y
   ```

   Se Falharam: 0, o módulo está funcionando corretamente.

---

## 🔁 Reset do módulo carros

O módulo `carros.py` possui a função `reset()` para limpar o armazenamento em memória:

```python
import carros
carros.reset()
```

Isso é útil para garantir que os testes rodem sempre com um cenário limpo.

---

## 📦 Dependências

- Python 3.8 ou superior
- Nenhuma dependência externa
- Apenas módulos internos do próprio projeto

---

## 🧠 Metodologia Utilizada

Foi aplicado o ciclo básico de **TDD (Test-Driven Development)**:
- Testes definidos primeiro
- Implementação mínima para o teste passar
- Pequenas refatorações quando necessário
- Execução repetida dos testadores para garantir estabilidade

Isso garante que os módulos:
- sejam confiáveis,
- possam ser usados por outros módulos sem efeitos colaterais,
- e sigam o padrão de modularização pedido na disciplina.

---

## 📬 Contato / Identificação

Integrante responsável: **Pessoa 1** — [Seu Nome Aqui]
Módulos implementados: `validacao.py`, `carros.py`
Testadores: `testador_validacao.py`, `testador_carros.py`