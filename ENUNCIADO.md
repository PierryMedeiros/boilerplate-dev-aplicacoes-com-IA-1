# Criação de Skills para Claude Code — Refatoração Arquitetural Automatizada

## Objetivo

Você deve entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado com todos os achados
- Refatorar o projeto para o padrão MVC (Model-View-Controller), eliminando os problemas encontrados
- Validar o resultado garantindo que a aplicação continua funcionando após as mudanças

A skill deve ser agnóstica de tecnologia — funcionar com diferentes linguagens e frameworks.

## Definição de Severidades

Para padronizar a sua auditoria e os relatórios gerados pela IA, utilize a seguinte escala de classificação baseada em problemas de MVC e SOLID:

- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

## Exemplo no CLI

```bash
# Executar a skill no projeto com problemas
claude "/refactor-arch ../code-smells-project"
```

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependencies:  flask-cors
Domain:        System API genérica (usuários, autenticação)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     usuarios, logs, configuracoes
================================
```

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 5 | MEDIUM: 2 | LOW: 3

## Findings

### [CRITICAL] God Class / God Method
File: models.py:1-350
Description: Arquivo único contém toda lógica de negócio, queries SQL, validação e formatação para 4 domínios diferentes.
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models e controllers por domínio.

### [CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
...

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```

```
[... refatoração executada ...]

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
src/
├── config/settings.py
├── models/
│   ├── usuario_model.py
│   └── log_model.py
├── views/
│   └── routes.py
├── controllers/
│   ├── usuario_controller.py
│   └── auth_controller.py
├── middlewares/error_handler.py
└── app.py (composition root)

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

## Tecnologias obrigatórias

- **Ferramenta:** Claude Code (CLI)
- **Recurso:** Custom Skills (`.claude/skills/`)
- **Formato dos arquivos de referência:** Markdown
- **Projetos-alvo:** Python/Flask, Node.js/Express e JavaScript vanilla (fornecidos no repositório base)

## Contexto: o que é uma Claude Code Skill?

Uma Skill é um conjunto de instruções em Markdown que ensina o Claude Code a executar uma tarefa complexa de forma padronizada e repetível. Uma skill vive no diretório `.claude/skills/` do projeto e é invocada como um slash command (ex: `/refactor-arch`).

### Estrutura de uma Skill

```
.claude/skills/nome-da-skill/
├── SKILL.md              # Ponto de entrada — define nome, descrição e o fluxo
└── references/           # Arquivos de referência que a SKILL.md referencia
    ├── arquivo1.md
    ├── arquivo2.md
    └── ...
```

### Anatomia do SKILL.md

```markdown
---
name: nome-da-skill
description: >
  Descrição do que a skill faz. O Claude usa isso para decidir
  quando sugerir a skill ao usuário.
disable-model-invocation: true
argument-hint: "[argumento-opcional]"
---

# Título da Skill

Instruções que o Claude vai seguir quando a skill for invocada.
Pode referenciar arquivos em references/ com links relativos:

Leia [references/meu-arquivo.md](references/meu-arquivo.md) para...
```

O SKILL.md é um prompt. Ele diz ao Claude o que fazer, em que ordem, e onde encontrar informações de referência. Os arquivos em `references/` contêm o conhecimento de domínio (catálogos, templates, guias) que a skill consulta durante a execução.

---

## Requisitos

### 1. Análise Manual dos Projetos

Antes de criar a skill, você deve entender os problemas que ela vai resolver.

**Tarefas:**

- Analisar o projeto `code-smells-project/` (Python/Flask — API genérica)
- Analisar o projeto `ecommerce-api-legacy/` (Node.js/Express — API de E-commerce)
- Analisar o projeto `task-manager-api/` (JavaScript vanilla — App de tarefas no browser)

Para cada projeto, identificar e documentar no mínimo 5 problemas, incluindo pelo menos:

- 1 de severidade CRITICAL ou HIGH
- 2 de severidade MEDIUM
- 2 de severidade LOW

Documentar os achados na seção "Análise Manual" do seu `README.md`

> **Dica:** Não precisa encontrar todos os problemas — foque nos que têm maior impacto arquitetural. Use os projetos como insumo para entender quais padrões sua skill precisa detectar.

> **Por que 3 projetos?** Um é Python/Flask (backend API), um é Node.js/Express (backend API), e um é JavaScript vanilla (frontend). Sua skill precisa funcionar nos 3 para provar que é verdadeiramente agnóstica de tecnologia.

### 2. Criação da Skill

Agora que você conhece os problemas, crie uma skill que os detecte e corrija automaticamente.

**Tarefas:**

Criar a estrutura de diretórios da skill dentro do projeto `code-smells-project/`:

```
.claude/skills/refactor-arch/
├── SKILL.md
└── references/
    ├── analysis-guide.md
    ├── antipatterns-catalog.md
    ├── report-template.md
    ├── mvc-guidelines.md
    └── refactoring-playbook.md
```

Implementar o SKILL.md com 3 fases sequenciais:

- **Fase 1 — Análise:** Detectar stack, mapear arquitetura atual, imprimir resumo
- **Fase 2 — Auditoria:** Cruzar código contra catálogo de anti-patterns, gerar relatório, pedir confirmação
- **Fase 3 — Refatoração:** Reestruturar para o padrão MVC, validar que funciona

Criar os 5 arquivos de referência obrigatórios:

| Arquivo | Propósito |
|---|---|
| `analysis-guide.md` | Heurísticas para detecção de linguagem, framework, banco de dados e mapeamento de arquitetura |
| `antipatterns-catalog.md` | Catálogo de anti-patterns com sinais de detecção e classificação de severidade |
| `report-template.md` | Template exato do relatório de auditoria (Fase 2) |
| `mvc-guidelines.md` | Regras do padrão MVC alvo (camadas Models, Views/Routes e Controllers, responsabilidades de cada uma) |
| `refactoring-playbook.md` | Padrões concretos de transformação para cada anti-pattern (com exemplos de código) |

**Requisitos da skill:**

- Deve ser agnóstica de tecnologia — os sinais de detecção e exemplos devem cobrir pelo menos 3 linguagens/frameworks diferentes
- O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída (CRITICAL, HIGH, MEDIUM, LOW)
- O catálogo deve incluir detecção de APIs deprecated — identificar uso de APIs obsoletas e recomendar o equivalente moderno
- O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois
- A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo
- A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)

### 3. Execução contra o Projeto 1 (code-smells-project)

Execute sua skill e valide que ela funciona.

**Tarefas:**

Invocar a skill no Claude Code:

```bash
claude "/refactor-arch"
```

- Verificar que a Fase 1 detecta corretamente a stack e imprime o resumo
- Verificar que a Fase 2 encontra no mínimo 8 dos problemas documentados na sua análise manual
- Confirmar a execução da Fase 3
- Verificar que a Fase 3:
  - Cria a estrutura de diretórios baseada em MVC
  - A aplicação inicia sem erros
  - Os endpoints originais continuam respondendo
- Salvar o relatório de auditoria (output da Fase 2) em `reports/audit-project-1.md`

### 4. Execução contra o Projeto 2 (ecommerce-api-legacy)

Prove que sua skill é reutilizável em outro projeto de backend, mas com stack diferente.

**Tarefas:**

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `ecommerce-api-legacy/`
- Invocar a skill:

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

- Verificar que as 3 fases executam corretamente neste projeto
- Salvar o relatório em `reports/audit-project-2.md`

### 5. Execução contra o Projeto 3 (task-manager-api)

Agora o teste real de agnóstico: um projeto JavaScript vanilla (frontend, sem framework de backend, sem banco de dados).

**Tarefas:**

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `task-manager-api/`
- Invocar a skill:

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

- Verificar que:
  - A Fase 1 detecta corretamente JavaScript como linguagem e identifica que é um frontend vanilla (sem framework)
  - A Fase 2 identifica problemas mesmo sendo um projeto menor (estado global, acoplamento UI/lógica, magic numbers, etc.)
  - A Fase 3 melhora a estrutura sem quebrar a aplicação (o HTML deve abrir no browser e rodar)
- Salvar o relatório em `reports/audit-project-3.md`

> **Nota:** Este projeto é pequeno e não tem backend/banco. A skill deve se adaptar — separando visualização (View) de lógica (Controller/Model). O importante é que ela detecte os problemas reais e não invente pastas desnecessárias.

### 6. Testes de Validação da Skill

O que você deve verificar e documentar:

Para cada projeto refatorado, valide o seguinte checklist:

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [ ] Relatório segue o template definido em report-template.md
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 8 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [ ] Estrutura de diretórios segue mvc-guidelines.md
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
```

## Critério de Aprovação

A skill deve atingir os seguintes mínimos em **todos os 3 projetos**:

| Critério | Requisito |
|---|---|
| Fase 1 detecta stack corretamente | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 encontra >= 5 findings | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 inclui pelo menos 1 CRITICAL ou HIGH | OBRIGATÓRIO (3/3 projetos) |
| Fase 3 aplicação/página funciona após refatoração | OBRIGATÓRIO (3/3 projetos) |

**IMPORTANTE:** Todos os critérios devem ser atingidos nos 3 projetos, não apenas em um!

> **Sobre o projeto 3 (task-manager-api):** "aplicação funciona" significa que o `index.html` abre no browser e a aplicação roda. Não há endpoints HTTP para testar.

## Estrutura obrigatória do projeto

Faça um fork do repositório base contendo os três projetos com code smells.

```
desafio-skills/
├── README.md                              # Sua documentação
│
├── code-smells-project/                   # Projeto 1 — Python/Flask (API genérica)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← SUA SKILL AQUI
│   │           ├── SKILL.md
│   │           └── references/
│   │               ├── analysis-guide.md
│   │               ├── antipatterns-catalog.md
│   │               ├── report-template.md
│   │               ├── mvc-guidelines.md
│   │               └── refactoring-playbook.md
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── ecommerce-api-legacy/                  # Projeto 2 — Node.js/Express (E-commerce API)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── src/
│   │   └── app.js
│   └── package.json
│
├── task-manager-api/                      # Projeto 3 — JavaScript vanilla (Frontend app)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── reports/                               # Relatórios gerados
    ├── audit-project-1.md                 # Saída da Fase 2 no projeto 1
    ├── audit-project-2.md                 # Saída da Fase 2 no projeto 2
    └── audit-project-3.md                 # Saída da Fase 2 no projeto 3
```

**O que você vai criar:**

- `.claude/skills/refactor-arch/` — A skill completa (SKILL.md + 5 arquivos de referência)
- `reports/audit-project-{1,2,3}.md` — Relatório de auditoria de cada projeto
- `README.md` — Documentação do seu processo

**O que já vem pronto:**

- `code-smells-project/` — API genérica Python/Flask com code smells intencionais
- `ecommerce-api-legacy/` — E-commerce API Node.js/Express com problemas de implementação
- `task-manager-api/` — App de tarefas JavaScript vanilla com problemas de design

## Exemplos de problemas nos projetos

Para que você entenda o tipo de problema que a skill deve detectar, aqui estão alguns exemplos. Parte do desafio é descobri-los na sua análise manual.

### code-smells-project (API Genérica — Python/Flask)

| Severidade | Problema |
|---|---|
| CRITICAL | SQL Injection — queries construídas com f-string em vez de parâmetros |
| HIGH | God Class — um único arquivo concentra lógica de múltiplos domínios |
| MEDIUM | `print()` usado para logs em vez do módulo `logging` |

### ecommerce-api-legacy (E-commerce API — Node.js/Express)

| Severidade | Problema |
|---|---|
| CRITICAL | Credenciais e senhas padrão hardcoded no código |
| HIGH | Lógica de negócio pesada implementada diretamente nas definições de rota |
| MEDIUM | Validação ausente no payload de requisições POST |

### task-manager-api (Task Manager — JavaScript vanilla)

| Severidade | Problema |
|---|---|
| HIGH | Estado global mutável controla o fluxo da aplicação inteira |
| MEDIUM | `alert()` para feedback ao usuário — bloqueia a thread |
| LOW | Magic numbers (limites de tarefas) hardcoded sem constantes |

Seu trabalho é ler o código, encontrar estes e os demais problemas, e então construir uma skill capaz de detectá-los automaticamente.

---

## Ordem de execução

**1. Analisar os projetos manualmente**

Leia o código dos três projetos e documente os problemas encontrados.

**2. Criar a skill**

Escreva o SKILL.md e os 5 arquivos de referência.

**3. Executar no projeto 1 (Python/Flask)**

```bash
cd code-smells-project
claude "/refactor-arch"
```

Salve a saída da Fase 2 em `reports/audit-project-1.md`.

**4. Executar no projeto 2 (Node.js/Express)**

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

Salve a saída da Fase 2 em `reports/audit-project-2.md`.

**5. Executar no projeto 3 (JavaScript vanilla)**

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

Salve a saída da Fase 2 em `reports/audit-project-3.md`.

**6. Iterar**

Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

---

## Entregável

Repositório público no GitHub (fork do repositório base) contendo:

- Skill completa em `.claude/skills/refactor-arch/` (dentro dos 3 projetos)
- Relatórios de auditoria em `reports/` (3 arquivos)
- `README.md` atualizado

### README.md deve conter:

**A) Seção "Análise Manual":**

- Lista dos problemas identificados manualmente em cada projeto
- Classificação por severidade
- Justificativa de por que cada problema é relevante

**B) Seção "Construção da Skill":**

- Decisões de design: por que organizou a skill em 3 fases
- Quais anti-patterns incluiu no catálogo e por quê
- Como garantiu que a skill é agnóstica de tecnologia
- Desafios encontrados e como resolveu

**C) Seção "Resultados":**

- Resumo dos relatórios de auditoria dos 3 projetos (quantos findings por severidade em cada)
- Comparação antes/depois da estrutura de cada projeto
- Checklist de validação preenchido para cada projeto
- Screenshots ou logs mostrando as aplicações rodando após refatoração
- Observações sobre como a skill se comportou em stacks diferentes

**D) Seção "Como Executar":**

- Pré-requisitos (Claude Code instalado e configurado)
- Comandos para executar a skill em cada projeto
- Como validar que a refatoração funcionou

---

## Referências úteis

- The Complete Guide to Building Skills for Claude (PDF) (Inserir link correto depois)
- Repositório oficial de Skills da Anthropic (Inserir link correto depois)
- Equipping Agents for the Real World with Agent Skills (Inserir link correto depois)
- Claude Code: Best practices for agentic coding (Inserir link correto depois)

---

## Dicas Finais

- **Comece pela análise manual** — entender os problemas profundamente é essencial para criar uma skill que os detecte.
- **O SKILL.md é um prompt** — ele instrui o Claude sobre o que fazer, enquanto os arquivos de referência fornecem o conhecimento de domínio.
- **Seja específico nos sinais de detecção** — "código ruim" não ajuda; "query SQL dentro de loop for" é acionável.
- **Teste incrementalmente** — não tente criar a skill perfeita de primeira.
- **A skill deve ser copiável** — se ela só funciona em um projeto específico, está acoplada demais. Teste nos 3 projetos para validar.
- **Projetos diferentes exigem adaptação** — a Fase 3 de um frontend JavaScript não vai ter as mesmas pastas de uma API Node. Sua skill deve se adaptar ao contexto.
- **Pedir confirmação na Fase 2 é obrigatório** — o humano deve revisar o relatório antes de qualquer modificação.
