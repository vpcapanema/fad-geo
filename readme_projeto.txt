===============================================================================
                     FAD-GEO - FERRAMENTA DE ANÁLISE DINAMIZADA
                    Sistema de Gestão de Projetos de Estadualização
===============================================================================

DATA DA DOCUMENTAÇÃO: 13 de junho de 2025
VERSÃO: 1.0
AUTOR: Sistema desenvolvido para gestão de projetos de estadualização

===============================================================================
1. VISÃO GERAL DO PROJETO
===============================================================================

O FAD-GEO é um sistema web desenvolvido em FastAPI/Python para gerenciar e 
analisar projetos de estadualização de elementos rodoviários. O sistema 
permite que analistas cadastrem projetos, preencham formulários modulares 
e coordenadores analisem e aprovem esses projetos.

OBJETIVO PRINCIPAL:
- Padronizar o processo de estadualização de elementos rodoviários
- Garantir análise completa através de 5 módulos obrigatórios
- Controlar fluxo de aprovação entre analistas e coordenadores
- Gerar documentação técnica em PDF para processos administrativos

TECNOLOGIAS UTILIZADAS:
- Backend: FastAPI (Python)
- Banco de Dados: PostgreSQL
- Frontend: HTML/CSS/JavaScript
- Templates: Jinja2
- ORM: SQLAlchemy

===============================================================================
2. ARQUITETURA DO SISTEMA
===============================================================================

2.1 ESTRUTURA DE PASTAS
------------------------
FAD-GEO/
├── app/
│   ├── api/endpoints/          # Endpoints da API REST
│   ├── database/              # Configuração do banco de dados
│   ├── models/                # Modelos SQLAlchemy
│   ├── services/              # Lógica de negócio
│   └── modules/               # Módulos específicos
├── static/                    # Arquivos estáticos (CSS, JS, imagens)
├── templates/                 # Templates HTML
├── logs/                      # Arquivos de log
└── main.py                    # Arquivo principal da aplicação

2.2 COMPONENTES PRINCIPAIS
---------------------------
- StatusProjetoService: Gerencia transições de status dos projetos
- ModulosProjetoService: Controla os 5 módulos obrigatórios
- FluxoModularService: Coordena a sequência de execução dos módulos

===============================================================================
3. LÓGICA DE NEGÓCIO
===============================================================================

3.1 TIPOS DE USUÁRIO
---------------------
- ANALISTA: Cria e gerencia projetos, preenche módulos
- COORDENADOR: Analisa, aprova ou reprova projetos
- MASTER: Acesso total, pode corrigir qualquer status

3.2 STATUS DOS PROJETOS
-----------------------
Status possíveis e suas transições:

1. EM CADASTRAMENTO
   - Estado inicial quando analista cria projeto
   - Analista pode editar e preencher módulos
   - Transição: → FINALIZADO (quando todos os 5 módulos estão validados)

2. FINALIZADO
   - Todos os módulos foram preenchidos e validados
   - Projeto pronto para envio
   - Transições: → ENVIADO (analista) ou → EM CADASTRAMENTO (editar)

3. ENVIADO
   - Projeto enviado para análise da coordenação
   - Ninguém pode editar
   - Transições: → EM ANÁLISE (coordenador) ou → EM CADASTRAMENTO (reverter)

4. EM ANÁLISE
   - Coordenador está analisando o projeto
   - Acesso aos formulários em modo visualização/análise
   - Transições: → APROVADO ou → REPROVADO (coordenador)

5. REPROVADO
   - Projeto possui pendências identificadas pelo coordenador
   - Motivo da reprovação é obrigatório
   - Transição: → EM CADASTRAMENTO (para correções)

6. APROVADO
   - Projeto aprovado pela coordenação
   - Segue para outras coordenadorias
   - Status final do fluxo principal

7. ARQUIVADO
   - Projeto inativo por diferentes motivos
   - Apenas MASTER pode arquivar
   - Status terminal

3.3 CONTROLE DE PERMISSÕES
---------------------------
Quem pode alterar cada status:

ANALISTA pode alterar para:
- Em cadastramento ← → Finalizado ← → Enviado

COORDENADOR pode alterar para:
- Enviado → Em análise → Aprovado/Reprovado
- Enviado → Em cadastramento (reverter)

MASTER pode alterar para:
- Qualquer status (incluindo Arquivado)

===============================================================================
4. OS 5 MÓDULOS OBRIGATÓRIOS
===============================================================================

Cada projeto DEVE ter exatamente 5 módulos preenchidos e validados:

4.1 MÓDULO 1: CADASTRO DO PROJETO
----------------------------------
OBJETIVO: Informações básicas e identificação do projeto
CAMPOS OBRIGATÓRIOS:
- Tipo e Nome do projeto
- Interessado (Pessoa jurídica) 
- Representante Legal (Pessoa Física)
- Elemento Rodoviário (obejto do provesso de estadualização)
- Importação e validação da geometria (do elemeto rodoviario)
- Croqui geral de localização (do elemento rodoviário)

4.2 MÓDULO 2: CONFORMIDADE AMBIENTAL
-------------------------------------
OBJETIVO: Análise de impactos e licenças ambientais
CAMPOS OBRIGATÓRIOS:
- Licenças ambientais necessárias
- Impactos ambientais identificados
- Medidas mitigatórias
- Estudos ambientais

4.3 MÓDULO 3: FAVORABILIDADE MULTICRITÉRIO
-------------------------------------------
OBJETIVO: Análise multicritério dos fatores relevantes
CAMPOS OBRIGATÓRIOS:
- Critérios selecionados para análise
- Pesos atribuídos a cada critério
- Matriz de decisão
- Resultado da análise multicritério

4.4 MÓDULO 4: FAVORABILIDADE SOCIOECONÔMICA
--------------------------------------------
OBJETIVO: Análise dos impactos socioeconômicos
CAMPOS OBRIGATÓRIOS:
- Impactos sociais identificados
- Benefícios econômicos esperados
- População afetada
- Indicadores socioeconômicos

4.5 MÓDULO 5: FAVORABILIDADE INFRAESTRUTURAL
---------------------------------------------
OBJETIVO: Análise da infraestrutura existente e necessária
CAMPOS OBRIGATÓRIOS:
- Infraestrutura existente no local
- Obras necessárias para implementação
- Custos estimados
- Cronograma de execução

4.6 LÓGICA SEQUENCIAL DOS MÓDULOS
----------------------------------
- APENAS o Módulo 1 pode ser iniciado quando projeto é criado
- Módulo N+1 só é liberado quando Módulo N está VALIDADO
- Validação é irreversível (garante integridade do processo)
- Quando todos os 5 módulos estão validados → projeto pode ser FINALIZADO

===============================================================================
5. FLUXO COMPLETO DO SISTEMA
===============================================================================

5.1 FLUXO DO ANALISTA
---------------------
1. Cria novo projeto (status: EM CADASTRAMENTO)
2. Sistema inicializa automaticamente os 5 módulos
3. Preenche Módulo 1 (Cadastro) → Valida
4. Sistema libera Módulo 2 (Ambiental) → Preenche → Valida
5. Sistema libera Módulo 3 (Multicritério) → Preenche → Valida
6. Sistema libera Módulo 4 (Socioeconômico) → Preenche → Valida
7. Sistema libera Módulo 5 (Infraestrutural) → Preenche → Valida
8. Sistema permite FINALIZAR projeto
9. Analista clica "Finalizar" (status: FINALIZADO)
10. Analista clica "Enviar para Análise" (status: ENVIADO)

5.2 FLUXO DO COORDENADOR
------------------------
1. Visualiza projetos com status ENVIADO
2. Clica "Analisar" → projeto vai para EM ANÁLISE
3. Revisa todos os 5 módulos em modo visualização
4. Toma decisão:
   - APROVAR: projeto vai para APROVADO
   - REPROVAR: projeto vai para REPROVADO (com motivo obrigatório)
   - REVERTER: projeto volta para EM CADASTRAMENTO

5.3 FLUXO DE CORREÇÃO
---------------------
Se projeto for REPROVADO:
1. Analista recebe projeto de volta (EM CADASTRAMENTO)
2. Pode editar qualquer módulo já validado
3. Após correções, valida módulos novamente
4. Quando todos estão validados → FINALIZAR → ENVIAR

===============================================================================
6. ENDPOINTS DA API
===============================================================================

6.1 GESTÃO DE STATUS (/api/projetos/status/)
---------------------------------------------
POST /finalizar                    # Finaliza projeto (analista)
POST /enviar                       # Envia para análise (analista)  
POST /reverter                     # Reverte para cadastramento (coordenador)
POST /iniciar-analise              # Inicia análise (coordenador)
POST /aprovar                      # Aprova projeto (coordenador)
POST /reprovar                     # Reprova projeto (coordenador)
POST /arquivar                     # Arquiva projeto (master)
GET  /listar/{status}              # Lista projetos por status
GET  /status-permitidos/{tipo}     # Status permitidos por usuário

6.2 GESTÃO DE MÓDULOS (/api/projetos/modulos/)
-----------------------------------------------
POST /inicializar                  # Inicializa os 5 módulos
POST /salvar                       # Salva dados de um módulo
POST /validar                      # Valida módulo e libera próximo
GET  /status/{projeto_id}          # Status de todos os módulos
GET  /formulario/{projeto_id}/{n}  # Dados do formulário do módulo
GET  /html/{projeto_id}/{n}        # HTML para PDF do módulo
POST /autocompletar/{projeto_id}   # Finaliza projeto automaticamente

6.3 INTERFACE WEB
-----------------
GET /projetos/{id}/modulos         # Dashboard visual dos módulos

===============================================================================
7. ESTRUTURA DO BANCO DE DADOS
===============================================================================

7.1 TABELA: projeto
-------------------
- id (PK)
- nome
- status (Em cadastramento, Finalizado, Enviado, etc.)
- usuario_id (FK - analista criador)
- coordenador_id (FK - coordenador responsável)
- modulo_atual (1-5)
- todos_modulos_concluidos (boolean)
- enviado_para_analise_em
- analise_iniciada_em
- analise_finalizada_em
- motivo_reprovacao
- observacao

7.2 TABELA: relatorio_modulo
----------------------------
- id (PK)
- projeto_id (FK)
- modulo_numero (1-5)
- modulo_nome
- status (pendente, em_preenchimento, validado)
- pode_executar (boolean)
- dados_extras (JSONB - dados do formulário)
- html_conteudo (HTML gerado)
- validado_em
- validado_por (FK)

7.3 TABELA: modulo_configuracao
-------------------------------
- id (PK)
- numero (1-5)
- nome
- descricao
- template_html
- endpoint_base
- ordem_execucao

===============================================================================
8. ETAPAS DE IMPLEMENTAÇÃO
===============================================================================

8.1 FASE 1: FUNDAÇÃO (CONCLUÍDA ✅)
-----------------------------------
- [x] Estrutura base do FastAPI
- [x] Configuração do banco PostgreSQL
- [x] Modelos SQLAlchemy básicos
- [x] Sistema de autenticação
- [x] Templates básicos

8.2 FASE 2: CONTROLE DE STATUS (CONCLUÍDA ✅)
----------------------------------------------
- [x] StatusProjetoService implementado
- [x] Todos os 7 status configurados
- [x] Validações de transição por tipo de usuário
- [x] Endpoints REST para controle de status
- [x] Logs de auditoria

8.3 FASE 3: SISTEMA MODULAR (CONCLUÍDA ✅)
-------------------------------------------
- [x] ModulosProjetoService implementado
- [x] Configuração dos 5 módulos obrigatórios
- [x] Controle sequencial de liberação
- [x] Validação irreversível de módulos
- [x] Geração de HTML para PDF

8.4 FASE 4: INTERFACE DE USUÁRIO (CONCLUÍDA ✅)
------------------------------------------------
- [x] Dashboard responsivo para módulos
- [x] Interface visual de progresso
- [x] Botões de ação contextuais
- [x] Feedback visual de status
- [x] Integração com API via JavaScript

8.5 FASE 5: PRÓXIMAS IMPLEMENTAÇÕES (PENDENTE 🔄)
--------------------------------------------------
- [ ] Formulários específicos para cada módulo
- [ ] Geração de PDF completa com ReportLab
- [ ] Sistema de notificações por email
- [ ] Relatórios gerenciais e dashboards
- [ ] Integração com sistema de arquivos
- [ ] Backup automático de dados
- [ ] Testes automatizados
- [ ] Deploy em produção

===============================================================================
9. CONFIGURAÇÃO E INSTALAÇÃO
===============================================================================

9.1 REQUISITOS
---------------
- Python 3.8+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

9.2 INSTALAÇÃO
---------------
1. Clone o repositório
2. Instale dependências: pip install -r requirements.txt
3. Configure banco de dados no arquivo de configuração
4. Execute migrações: python -m alembic upgrade head
5. Inicie servidor: python main.py

9.3 CONFIGURAÇÃO INICIAL
-------------------------
1. Criar usuário MASTER no banco
2. Configurar os 5 módulos na tabela modulo_configuracao
3. Definir permissões por tipo de usuário
4. Configurar SMTP para emails (futuro)

===============================================================================
10. PADRÕES E CONVENÇÕES
===============================================================================

10.1 NOMENCLATURA
-----------------
- Arquivos: snake_case
- Classes: PascalCase
- Métodos: snake_case
- Endpoints: kebab-case
- Status: "Primeira Maiúscula"

10.2 ESTRUTURA DE RESPOSTA API
------------------------------
Sucesso:
{
    "message": "Descrição da ação",
    "data": { ... dados ... }
}

Erro:
{
    "error": "Descrição do erro"
}

10.3 LOGS
---------
- INFO: Ações normais do sistema
- WARNING: Situações que merecem atenção
- ERROR: Erros que impedem funcionamento
- DEBUG: Informações técnicas detalhadas

===============================================================================
11. VALIDAÇÕES E REGRAS DE NEGÓCIO
===============================================================================

11.1 REGRAS CRÍTICAS
--------------------
- Um projeto DEVE ter exatamente 5 módulos
- Módulos DEVEM ser preenchidos em ordem sequencial
- Validação de módulo é IRREVERSÍVEL
- Apenas o criador do projeto pode enviá-lo para análise
- Coordenador NÃO pode analisar próprios projetos
- Motivo é OBRIGATÓRIO para reprovação

11.2 VALIDAÇÕES AUTOMÁTICAS
----------------------------
- Campos obrigatórios por módulo
- Transições de status permitidas
- Permissões por tipo de usuário
- Integridade referencial no banco
- Logs de todas as alterações

===============================================================================
12. SEGURANÇA
===============================================================================

12.1 CONTROLES IMPLEMENTADOS
-----------------------------
- Validação de permissões por endpoint
- Sanitização de inputs
- Logs de auditoria completos
- Validação de integridade de dados

12.2 MELHORIAS FUTURAS
----------------------
- Criptografia de dados sensíveis
- Autenticação com tokens JWT
- Rate limiting por usuário
- Backup automático seguro

===============================================================================
13. MONITORAMENTO E PERFORMANCE
===============================================================================

13.1 MÉTRICAS IMPORTANTES
--------------------------
- Tempo médio por módulo
- Taxa de aprovação/reprovação
- Projetos por status
- Usuários mais ativos
- Erros por endpoint

13.2 OTIMIZAÇÕES
----------------
- Índices no banco de dados
- Cache de consultas frequentes
- Compressão de respostas HTTP
- Lazy loading de dados grandes

===============================================================================
14. CONSIDERAÇÕES FINAIS
===============================================================================

O FAD-GEO foi projetado para ser:
- ESCALÁVEL: Pode crescer com a demanda
- CONFIÁVEL: Validações rigorosas garantem integridade
- AUDITÁVEL: Todos os passos são registrados
- FLEXÍVEL: Fácil de adaptar para novos requisitos
- EFICIENTE: Interface otimizada para produtividade

O sistema implementa com sucesso a lógica de negócio solicitada, garantindo
que todos os projetos passem pelo processo completo de análise através dos
5 módulos obrigatórios, com controle rigoroso de status e permissões.

===============================================================================
DOCUMENTAÇÃO GERADA EM: 13/06/2025
VERSÃO DO SISTEMA: 1.0 
STATUS: IMPLEMENTAÇÃO FASE 4 CONCLUÍDA
PRÓXIMA FASE: Formulários específicos e geração de PDF
===============================================================================
