# Instruções de Correção: Desafio de Refatoração Arquitetural com IA

Este documento serve como guia para a correção do desafio de auditoria e refatoração utilizando `claude.md` e Skills.

## 1. Sobre a Aplicação (Boilerplate)

A aplicação base é uma API RESTful construída em Node.js com Express e SQLite3 (em memória). Ela simula um mini LMS (sistema de gestão de aprendizagem) com compra de cursos.

Seu principal propósito não é a complexidade da regra de negócio, mas sim a **péssima qualidade estrutural** do código. Ela foi construída intencionalmente como um "Frankenstein" para testar a capacidade do aluno de guiar uma IA na identificação e correção de anti-padrões e *Code Smells*.

### Endpoints Disponíveis

* **`POST /api/checkout`**: Realiza a compra de um curso. Recebe dados do usuário, curso e um cartão de crédito simulado. Cria o usuário (se não existir), a matrícula, processa o pagamento e gera um log de auditoria. Tudo em uma única rota cheia de callbacks.
* **`GET /api/admin/financial-report`**: Gera um relatório de faturamento por curso. O código faz loops aninhados que geram um ataque DDoS no próprio banco de dados (N*M Queries).
* **`DELETE /api/users/:id`**: Deleta um usuário, mas não exclui suas matrículas e pagamentos, gerando inconsistência no banco de dados.

---

## 2. Erros Arquiteturais (O que a Skill DEVE resolver)

Após o aluno rodar a Skill de refatoração, a aplicação deve continuar funcionando perfeitamente (os endpoints devem responder da mesma forma nos testes do `api.http`), mas os seguintes problemas do código original devem ter sido eliminados:

### 🚨 God Class e Mistura de Domínios (`GodManager.js`)
* **Problema original:** A classe gerencia rotas, banco de dados e regras de negócio de múltiplos domínios (Usuários, Cursos, Matrículas, Pagamentos e Auditoria).
* **Resolução esperada:** O código deve estar fatiado em camadas seguindo os princípios de Clean Architecture. Cada domínio deve ter suas próprias `Routes`, `Controllers`, `Services`/`UseCases` e `Repositories`. 

[Image of Clean Architecture diagram]


### 🚨 Callback Hell (Pyramid of Doom) e Nomes Ruins
* **Problema original:** O endpoint `/api/checkout` possui 7 níveis de identação (callbacks aninhados) e utiliza variáveis péssimas (`u`, `e`, `p`, `cid`).
* **Resolução esperada:** A IA deve ter reescrito a lógica utilizando `async/await` ou `Promises` encadeadas de forma limpa, extraindo blocos de código para métodos menores e utilizando nomes descritivos.

### 🚨 O Pesadelo das N+1 (e N*M) Queries
* **Problema original:** O endpoint de relatório financeiro faz um `SELECT` de cursos e, dentro de um loop, faz `SELECT` de matrículas e, dentro de outro loop, busca usuários e pagamentos um a um.
* **Resolução esperada:** A IA deve ter refatorado isso no `Repository` utilizando uma query SQL otimizada com `JOIN` ou agrupamento, eliminando as queries dentro de loops de repetição.

### 🚨 Acoplamento Forte e Falta de Injeção de Dependência
* **Problema original:** Instanciação do `sqlite3` injetada diretamente no construtor da classe base. Impossível de mockar para testes.
* **Resolução esperada:** A conexão com o banco deve ser injetada de fora para dentro (Dependency Inversion), facilitando a criação de testes unitários no futuro.

### 🚨 Global State, Hardcoded Envs e Efeitos Colaterais (`utils.js`)
* **Problema original:** Uso de variáveis globais (`globalCache`, `totalRevenue`) que vazam estado entre requisições, além de credenciais e chaves de API *hardcoded* no código. Funções bloqueantes de CPU (`badCrypto`).
* **Resolução esperada:** Remoção total do estado global do escopo da aplicação e uso de variáveis de ambiente (`.env` ou `process.env`) para gerenciar as credenciais.

---

## 3. Critérios de Aceite Rápido

Para aprovar a entrega do aluno, verifique:
1.  **Código Original Mantido:** O repositório enviado tem a pasta `src/` com o código espaguete original (para que você possa rodar a skill localmente durante a correção).
2.  **claude.md Existente:** Há um arquivo detalhando as regras de Clean Architecture e proibindo explicitamente os Code Smells listados.
3.  **Skill Estruturada:** A skill em `skills/` usa *Frontmatter* e *Progressive Disclosure* (primeiro audita e gera relatório, depois refatora).
4.  **Execução:** Ao rodar a skill do aluno no seu ambiente, ela gera o relatório de erros listando os problemas (Callback Hell, N+1, God Class) e cria a estrutura de pastas correta.
5.  **Teste de Regressão:** Após a IA trabalhar, o comando `npm start` funciona e as requisições do `api.http` respondem com sucesso, sem quebrar as regras originais.