# 🔍 DIAGNÓSTICO COMPLETO - ELEMENTOS RODOVIÁRIOS
## Correspondência entre Tabelas do Banco, Models.py e Formulários HTML

**Data da Auditoria:** 10 de junho de 2025  
**Sistema:** FAD-GEO - Elementos Rodoviários  

---

## 📊 RESUMO EXECUTIVO

### ✅ **STATUS GERAL:** PARCIALMENTE ALINHADO
- **Tabelas do Banco:** ✅ Existem e estão corretas
- **Models Python:** ⚠️ Precisam de ajustes
- **Templates HTML:** ⚠️ Contêm campos extras não mapeados
- **Endpoints:** ✅ Implementados corretamente

---

## 🗃️ ANÁLISE DETALHADA POR ELEMENTO

### 1. **TRECHO RODOVIÁRIO**

#### 🏛️ Tabela do Banco: `Elementos_rodoviarios.trecho_rodoviario`
```sql
- id (INTEGER, NOT NULL, PK)
- codigo (VARCHAR, NOT NULL)
- denominacao (VARCHAR, NOT NULL)
- municipio (VARCHAR, NOT NULL)
- criado_em (TIMESTAMP, NULL)
- extensao (DOUBLE PRECISION, NULL)
- tipo (VARCHAR(100), NULL)
```

#### 🐍 Model Python: `TrechoEstadualizacao`
```python
- id (Integer, PK)
- codigo (String, NOT NULL, UNIQUE)
- denominacao (String, NOT NULL)
- municipio (String, NOT NULL)
```

#### 📝 Template HTML: `cd_interessado_trecho.html`
```html
- codigo (input, required, pattern)
- denominacao (input, required)
- municipio (select, required)
```

#### ⚠️ **INCONSISTÊNCIAS ENCONTRADAS:**
1. **Model faltando campos:** `criado_em`, `extensao`, `tipo`
2. **Tabela tem nome diferente:** `trecho_rodoviario` vs `trechos_estadualizacao` no model

---

### 2. **RODOVIA**

#### 🏛️ Tabela do Banco: `Elementos_rodoviarios.rodovia`
```sql
- id (INTEGER, NOT NULL, PK)
- codigo (VARCHAR, NOT NULL)
- nome (VARCHAR, NOT NULL)
- uf (VARCHAR(2), NOT NULL)
- extensao_km (DOUBLE PRECISION, NULL)
- criado_em (TIMESTAMP, NULL)
- tipo (VARCHAR(100), NULL)
- municipio (VARCHAR, NULL)
```

#### 🐍 Model Python: `RodoviaEstadualizacao`
```python
- id (Integer, PK)
- codigo (String, NOT NULL, UNIQUE)
- nome (String, NOT NULL)
- uf (String(2), NOT NULL)
- extensao_km (Float, NULL)
- municipio (String, NULL) [DUPLICADO!]
- criado_em (DateTime, NOT NULL, default)
- tipo (String(100), NULL)
```

#### 📝 Template HTML: `cd_interessado_rodovia.html`
```html
- codigo (input, required, pattern)
- nome (input, required)
- uf (input, required, maxlength=2)
- municipio (select, required)
- extensao_km (input number, required)
- tipo (input, required)
```

#### ⚠️ **INCONSISTÊNCIAS ENCONTRADAS:**
1. **Model tem campo duplicado:** `municipio` aparece duas vezes
2. **HTML torna campos opcionais como obrigatórios:** `extensao_km`, `tipo`

---

### 3. **DISPOSITIVO**

#### 🏛️ Tabela do Banco: `Elementos_rodoviarios.dispositivo`
```sql
- id (INTEGER, NOT NULL, PK)
- codigo (VARCHAR, NOT NULL)
- tipo (VARCHAR(100), NOT NULL)
- localizacao (VARCHAR, NULL)
- criado_em (TIMESTAMP, NULL)
- municipio (VARCHAR, NULL)
- denominacao (VARCHAR, NOT NULL)
```

#### 🐍 Model Python: `DispositivoEstadualizacao`
```python
- id (Integer, PK)
- codigo (String, NOT NULL, UNIQUE)
- denominacao (String, NOT NULL)
- tipo (String(100), NOT NULL)
- localizacao (String, NOT NULL)
- municipio (String, NOT NULL)
- criado_em (DateTime, NOT NULL, default)
```

#### 📝 Template HTML: `cd_interessado_dispositivo.html`
```html
- codigo (input, required, pattern)
- denominacao (input, required)
- tipo (input, required)
- municipio (select, required)
- localizacao (input, required)
- telefone (input, required) ⚠️ NÃO MAPEADO
- email (input, required) ⚠️ NÃO MAPEADO
```

#### ⚠️ **INCONSISTÊNCIAS ENCONTRADAS:**
1. **Campos nullability diferentes:** `localizacao`, `municipio`
2. **HTML tem campos extras:** `telefone`, `email` não existem no model/banco
3. **Model mais restritivo que banco:** NOT NULL vs NULL

---

### 4. **OBRA DE ARTE**

#### 🏛️ Tabela do Banco: `Elementos_rodoviarios.obra_arte`
```sql
- id (INTEGER, NOT NULL, PK)
- codigo (VARCHAR, NOT NULL)
- tipo (VARCHAR(100), NOT NULL)
- extensao_m (DOUBLE PRECISION, NULL)
- criado_em (TIMESTAMP, NULL)
- municipio (VARCHAR, NULL)
- denominacao (VARCHAR, NOT NULL)
```

#### 🐍 Model Python: `ObraArteEstadualizacao`
```python
- id (Integer, PK)
- codigo (String, NOT NULL, UNIQUE)
- denominacao (String, NOT NULL)
- tipo (String(100), NOT NULL)
- extensao_m (Float, NOT NULL)
- localizacao (String, NOT NULL)
- municipio (String, NOT NULL)
- criado_em (DateTime, NOT NULL, default)
```

#### 📝 Template HTML: `cd_interessado_obra_arte.html`
```html
- codigo (input, required, pattern)
- denominacao (input, required)
- tipo (input, required)
- municipio (select, required)
- extensao_m (input number, required)
- localizacao (input, required)
- telefone (input, required) ⚠️ NÃO MAPEADO
- email (input, required) ⚠️ NÃO MAPEADO
```

#### ⚠️ **INCONSISTÊNCIAS ENCONTRADAS:**
1. **Campo extra no model:** `localizacao` não existe no banco
2. **HTML tem campos extras:** `telefone`, `email` não existem no model/banco
3. **Nullability diferente:** `extensao_m` NULL no banco, NOT NULL no model

---

## 🚨 PROBLEMAS CRÍTICOS IDENTIFICADOS

### 1. **Desalinhamento Model vs Banco**
- `TrechoEstadualizacao`: Falta 3 campos (`criado_em`, `extensao`, `tipo`)
- `RodoviaEstadualizacao`: Campo `municipio` duplicado
- `DispositivoEstadualizacao`: Nullability incorreta
- `ObraArteEstadualizacao`: Campo `localizacao` extra, nullability incorreta

### 2. **Campos Fantasma nos Templates**
- `telefone` e `email` em dispositivo e obra de arte
- Não existem no banco nem nos models
- Causarão erro 500 nos endpoints

### 3. **Inconsistência de Nomes**
- Model usa `trechos_estadualizacao`, banco usa `trecho_rodoviario`

---

## 📋 PLANO DE CORREÇÃO RECOMENDADO

### **PRIORIDADE ALTA:**

1. **Corrigir Model TrechoEstadualizacao:**
```python
# Adicionar campos faltantes
criado_em = Column(DateTime, nullable=True)
extensao = Column(Float, nullable=True)  
tipo = Column(String(100), nullable=True)
# Corrigir nome da tabela
__tablename__ = "trecho_rodoviario"
```

2. **Corrigir Model RodoviaEstadualizacao:**
```python
# Remover campo municipio duplicado
# Manter apenas: municipio = Column(String, nullable=True)
```

3. **Corrigir Models Dispositivo e ObraArte:**
```python
# Ajustar nullability para coincidir com banco
# Remover campos que não existem no banco
```

4. **Limpar Templates HTML:**
```html
<!-- Remover campos telefone e email dos templates -->
<!-- dispositivo e obra_arte -->
```

### **PRIORIDADE MÉDIA:**

5. **Atualizar Endpoints:** Ajustar validações após correção dos models
6. **Criar Testes:** Validar correspondência após correções

---

## ✅ PONTOS POSITIVOS

1. **Estrutura bem organizada:** Esquema separado, nomes consistentes
2. **Validações HTML adequadas:** Patterns, required, maxlength
3. **Endpoints bem estruturados:** Validação, tratamento de erros
4. **Campos principais alinhados:** id, codigo, denominacao presentes em todos

---

## 🎯 RECOMENDAÇÃO FINAL

**AÇÃO IMEDIATA NECESSÁRIA:** Corrigir os models para corresponder exatamente às tabelas do banco antes de usar os endpoints em produção. Os desalinhamentos atuais causarão falhas de runtime.

**IMPACTO:** Médio - Sistema funcional após correções
**TEMPO ESTIMADO:** 2-3 horas para todas as correções
**RISCO:** Baixo - Correções são diretas e bem definidas
