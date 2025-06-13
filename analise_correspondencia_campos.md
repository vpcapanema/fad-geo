"""
ANÁLISE DE CORRESPONDÊNCIA DE CAMPOS - FORMULARIO_SERVICE.PY
============================================================

ANÁLISE REALIZADA EM: 11/06/2025

1. ESTRUTURA DE DADOS NO FORMULARIO_SERVICE:
=============================================

Dados passados para o template:
```python
dados_template = {
    'usuario': usuario,                    # Objeto UsuarioSistema
    'pessoa_fisica': pessoa_fisica or {},  # Objeto PessoaFisica ou dict vazio
    'data_geracao': datetime.now()         # Data de geração
}
```

2. CAMPOS DO MODELO UsuarioSistema (app/models/cd_usuario_sistema.py):
======================================================================

CAMPOS PRINCIPAIS:
- id (Integer, Primary Key)
- nome (String, NOT NULL)
- cpf (String, NOT NULL)
- email (String, NOT NULL)
- telefone (String)
- pessoa_fisica_id (Integer, FK)
- instituicao (String)
- tipo_lotacao (String)
- email_institucional (String)
- telefone_institucional (String)
- ramal (String)
- sede_hierarquia (String)
- sede_coordenadoria (String)
- sede_setor (String)
- sede_assistencia (String)
- regional_nome (String)
- regional_coordenadoria (String)
- regional_setor (String)
- senha_hash (String, NOT NULL)
- tipo (String, NOT NULL, default="analista")
- criado_em (DateTime)
- aprovado_em (DateTime)
- aprovador_id (Integer, FK)
- status (String, default="aguardando aprovacao")
- ativo (Boolean, default=True)

3. CAMPOS DO MODELO PessoaFisica (app/models/cd_pessoa_fisica.py):
==================================================================

CAMPOS DE ENDEREÇO:
- id (Integer, Primary Key)
- nome (String, NOT NULL)
- cpf (String, NOT NULL, UNIQUE)
- email (String, NOT NULL)
- telefone (String, NOT NULL)
- rua (String, NOT NULL)
- numero (String, NOT NULL)
- complemento (String)
- bairro (String, NOT NULL)
- cep (String, NOT NULL)
- cidade (String, NOT NULL)  # Nota: era 'municipio', foi alterado para 'cidade'
- uf (String, NOT NULL)
- criado_em (DateTime)
- atualizado_em (DateTime)

4. CAMPOS USADOS NO TEMPLATE (app/templates/formularios_cadastro_usuarios/cadastro_usuario_template.html):
==========================================================================================================

SEÇÃO 1 - INFORMAÇÕES PESSOAIS ({{ usuario.campo }}):
✅ {{ usuario.nome }}                  → UsuarioSistema.nome
✅ {{ usuario.id }}                    → UsuarioSistema.id
✅ {{ usuario.cpf }}                   → UsuarioSistema.cpf
✅ {{ usuario.telefone }}              → UsuarioSistema.telefone
✅ {{ usuario.email }}                 → UsuarioSistema.email
✅ {{ usuario.pessoa_fisica_id }}      → UsuarioSistema.pessoa_fisica_id

SEÇÃO 2 - ENDEREÇO ({{ pessoa_fisica.campo }}):
✅ {{ pessoa_fisica.rua }}             → PessoaFisica.rua
✅ {{ pessoa_fisica.numero }}          → PessoaFisica.numero
✅ {{ pessoa_fisica.bairro }}          → PessoaFisica.bairro
✅ {{ pessoa_fisica.cep }}             → PessoaFisica.cep
✅ {{ pessoa_fisica.cidade }}          → PessoaFisica.cidade
✅ {{ pessoa_fisica.uf }}              → PessoaFisica.uf

SEÇÃO 3 - INFORMAÇÕES PROFISSIONAIS ({{ usuario.campo }}):
✅ {{ usuario.instituicao }}           → UsuarioSistema.instituicao
❌ {{ usuario.lotacao }}               → ERRO! Campo não existe! Deveria ser 'tipo_lotacao'
✅ {{ usuario.email_institucional }}   → UsuarioSistema.email_institucional
✅ {{ usuario.telefone_institucional }} → UsuarioSistema.telefone_institucional
✅ {{ usuario.ramal }}                 → UsuarioSistema.ramal
✅ {{ usuario.sede_hierarquia }}       → UsuarioSistema.sede_hierarquia
✅ {{ usuario.sede_coordenadoria }}    → UsuarioSistema.sede_coordenadoria
✅ {{ usuario.sede_setor }}            → UsuarioSistema.sede_setor
✅ {{ usuario.sede_assistencia }}     → UsuarioSistema.sede_assistencia
✅ {{ usuario.regional_nome }}         → UsuarioSistema.regional_nome
✅ {{ usuario.regional_coordenadoria }} → UsuarioSistema.regional_coordenadoria
✅ {{ usuario.regional_setor }}        → UsuarioSistema.regional_setor

SEÇÃO 4 - INFORMAÇÕES DO USUÁRIO ({{ usuario.campo }}):
✅ {{ usuario.tipo }}                  → UsuarioSistema.tipo
✅ {{ usuario.status }}                → UsuarioSistema.status
✅ {{ usuario.ativo }}                 → UsuarioSistema.ativo
✅ {{ usuario.criado_em }}             → UsuarioSistema.criado_em

DADOS AUXILIARES:
✅ {{ data_geracao }}                  → Variável local datetime.now()

5. PROBLEMAS IDENTIFICADOS:
===========================

❌ ERRO CRÍTICO: Campo 'lotacao' no template não existe no modelo
   - Template usa: {{ usuario.lotacao }}
   - Deveria ser: {{ usuario.tipo_lotacao }}
   - Localização: Linha ~125 do template

⚠️  CAMPOS FALTANTES NO TEMPLATE (não exibidos mas existem no banco):
   - usuario.aprovado_em
   - usuario.aprovador_id
   - pessoa_fisica.complemento
   - pessoa_fisica.criado_em
   - pessoa_fisica.atualizado_em

6. VERIFICAÇÃO DA LÓGICA DE PESSOA_FÍSICA:
==========================================

✅ Correta: O serviço verifica se usuario.pessoa_fisica_id existe
✅ Correta: Busca PessoaFisica pelo ID quando existe
✅ Correta: Usa dict vazio {} quando pessoa_fisica é None
✅ Protegida: Template não quebra se pessoa_fisica for vazio

7. POSSÍVEL CAUSA DO PROBLEMA NO ENDPOINT:
==========================================

O problema do campo 'formulario_html' retornando None pode estar relacionado a:

1. Erro no template por causa do campo 'lotacao' inexistente
2. Exception silenciosa durante renderização do template
3. Falha na criação de diretórios
4. Problema de permissões de escrita

8. RECOMENDAÇÕES:
=================

CORREÇÃO IMEDIATA:
1. Corrigir o campo 'lotacao' no template para 'tipo_lotacao'

MELHORIAS SUGERIDAS:
2. Adicionar campos faltantes no template (se necessário)
3. Adicionar tratamento de erro mais específico no FormularioService
4. Adicionar logs mais detalhados para debug
5. Validar se diretórios têm permissão de escrita

9. CONCLUSÃO:
=============

O erro principal está no template HTML que referencia um campo 'lotacao' 
que não existe no modelo UsuarioSistema. Isso provavelmente está causando 
erro durante a renderização do template, que pode estar sendo capturado 
e resultando em formulario_html = None.

A correção deste campo deve resolver o problema do endpoint retornando None.
"""
