# 📱 MAPEAMENTO COMPLETO: FORMATAÇÃO E VALIDAÇÃO DE TELEFONE

## 🏗️ **ESTRUTURA GERAL**

```
📱 TELEFONE PESSOAL
├── 🏠 HTML: #telefone
├── 🎨 Formatação: formatacao_telefone_movel.js (telInputPessoal)
├── ✅ Validação Frontend: regex fixo + móvel
├── 📤 Limpeza pré-envio: formulario_usuario_unificado.js
└── 🔍 Validação Backend: cd_cadastro_usuario_sistema.py

🏢 TELEFONE INSTITUCIONAL  
├── 🏠 HTML: #telefone_institucional
├── 🎨 Formatação: formatacao_telefone_movel.js (telInputInst)
├── ✅ Validação Frontend: regex fixo + móvel
├── 📤 Limpeza pré-envio: formulario_usuario_unificado.js
└── 🔍 Validação Backend: cd_cadastro_usuario_sistema.py
```

---

## 📄 **1. HTML - CAMPOS DE TELEFONE**

### 🔶 **Telefone Pessoal**
**Arquivo:** `app/templates/cd_cadastro_usuario.html` (linha ~437)

```html
<div class="form-field half">
  <label for="telefone">Telefone:<span class="obrigatorio-icone">*</span><span class="check-icone">&#10003;</span></label>
  <input type="text" id="telefone" name="telefone" required maxlength="16" style="width: 100%; box-sizing: border-box;" />
  <div id="telefone-feedback" style="color: #a80000; font-size: 13px; margin-top: 2px;"></div>
</div>
```

### 🔶 **Telefone Institucional**
**Arquivo:** `app/templates/cd_cadastro_usuario.html` (linha ~513)

```html
<div class="form-field half">
  <label for="telefone_institucional">Telefone Institucional:<span class="obrigatorio-icone">*</span><span class="check-icone">&#10003;</span></label>
  <input type="text" id="telefone_institucional" name="telefone_institucional" required maxlength="16" style="width: 100%; box-sizing: border-box;" />
  <div id="msg-telefone-institucional" style="display:none; color:red; font-size:13px;"></div>
</div>
```

### 🔶 **Importação dos Scripts**
**Arquivo:** `app/templates/cd_cadastro_usuario.html` (linha ~576)

```html
<script type="module" src="/static/js/formatacao_valores_campos/formatacao_telefone_movel.js"></script>
<script src="/static/js/cd_usuario/formulario_usuario_unificado.js"></script>
```

---

## 💻 **2. JAVASCRIPT - FORMATAÇÃO E VALIDAÇÃO**

### 🔶 **Arquivo Principal: formatacao_telefone_movel.js**
**Localização:** `app/static/js/formatacao_valores_campos/formatacao_telefone_movel.js`

#### 📱 **TELEFONE PESSOAL (linhas 9-69)**

```javascript
// Formatação e validação dinâmica de telefone pessoal (aceita fixo e móvel)
const telInputPessoal = document.getElementById('telefone');
if (telInputPessoal) {
  // Cria div de mensagem de erro
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-telefone';
  
  telInputPessoal.addEventListener('input', function (e) {
    // 🧹 LIMPEZA: Remove tudo que não é dígito
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);
    
    // 🎨 FORMATAÇÃO VISUAL
    let formatado = '';
    if (v.length > 10) {
      // Celular: (99) 99999-9999
      formatado = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (v.length > 6) {
      // Fixo: (99) 9999-9999 ou início de celular
      formatado = v.replace(/(\d{2})(\d{4,5})(\d{0,4})/, '($1) $2-$3');
    } else if (v.length > 2) {
      formatado = v.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else {
      formatado = v.replace(/(\d{0,2})/, '$1');
    }
    
    e.target.value = formatado;
    
    // ✅ VALIDAÇÃO FRONTEND
    const regexFixo = /^\(\d{2}\) \d{4}-\d{4}$/;    // 10 dígitos
    const regexMovel = /^\(\d{2}\) \d{5}-\d{4}$/;   // 11 dígitos
    const valido = regexFixo.test(formatado) || regexMovel.test(formatado);
    
    if (valido) {
      msg.style.display = 'none';
      telInputPessoal.classList.remove('erro-campo');
    } else {
      msg.textContent = 'Telefone inválido. Use (XX) XXXX-XXXX ou (XX) XXXXX-XXXX';
      msg.style.display = 'block';
      telInputPessoal.classList.add('erro-campo');
    }
    
    // 🔄 Integração com sistema de validação visual
    if (typeof window.atualizarValidacaoCampo === 'function') {
      atualizarValidacaoCampo(telInputPessoal, valido);
    }
  });
}
```

#### 🏢 **TELEFONE INSTITUCIONAL (linhas 71-155)**

```javascript
// Formatação e validação dinâmica de telefone institucional (aceita fixo e móvel)
const telInputInst = document.getElementById('telefone_institucional');
if (telInputInst) {
  // Busca div de mensagem existente ou cria nova
  let msg = document.getElementById('msg-telefone-institucional');
  
  telInputInst.addEventListener('input', function (e) {
    // 🧹 LIMPEZA: Remove tudo que não é dígito
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);
    
    // 🎨 FORMATAÇÃO VISUAL (mesmo padrão do telefone pessoal)
    let formatado = '';
    if (v.length > 10) {
      formatado = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (v.length > 6) {
      formatado = v.replace(/(\d{2})(\d{4,5})(\d{0,4})/, '($1) $2-$3');
    } else if (v.length > 2) {
      formatado = v.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else {
      formatado = v.replace(/(\d{0,2})/, '$1');
    }
    
    e.target.value = formatado;
    
    // ✅ VALIDAÇÃO FRONTEND (igual ao telefone pessoal)
    const regexFixo = /^\(\d{2}\) \d{4}-\d{4}$/;    // 10 dígitos
    const regexMovel = /^\(\d{2}\) \d{5}-\d{4}$/;   // 11 dígitos
    const valido = regexFixo.test(formatado) || regexMovel.test(formatado);
    
    if (valido) {
      msg.style.display = 'none';
      telInputInst.classList.remove('erro-campo');
    } else {
      msg.textContent = 'Telefone inválido. Use (XX) XXXX-XXXX ou (XX) XXXXX-XXXX';
      msg.style.display = 'block';
      telInputInst.classList.add('erro-campo');
    }
    
    // 🔄 Integração com sistema de validação visual
    if (typeof window.atualizarValidacaoCampo === 'function') {
      atualizarValidacaoCampo(telInputInst, valido);
    }
  });
}
```

### 🔶 **Arquivo de Envio: formulario_usuario_unificado.js**
**Localização:** `app/static/js/cd_usuario/formulario_usuario_unificado.js`

#### 📤 **LIMPEZA PRÉ-ENVIO (linhas 145-153)**

```javascript
// ENVIO DO FORMULÁRIO VIA FETCH (Usuário)
const form = document.querySelector('form');
if (form) {
  form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(form);
    const dados = {};
    
    formData.forEach((v, k) => {
      // 🧹 LIMPA TELEFONES ANTES DE ENVIAR - remove formatação, mantém apenas dígitos
      if (k === 'telefone' || k === 'telefone_institucional') {
        dados[k] = v.replace(/\D/g, ''); // ⚠️ Remove tudo que não é dígito
      } else {
        dados[k] = v;
      }
    });
    
    // Envia dados limpos para o backend
    const resp = await fetch('/usuario/cadastrar-usuario', {
      method: 'POST',
      body: new URLSearchParams(dados)
    });
  });
}
```

### 🔶 **Arquivos Depreciados/Alternativos**

#### ❌ **formatacao_telefone_geral.js (DEPRECIADO)**
**Status:** Arquivo mantido apenas para compatibilidade, não deve ser usado.

#### ⚠️ **formatacao_telefone_fixo.js (ESPECÍFICO)**
**Uso:** Apenas para telefone fixo (10 dígitos), não usado no cadastro de usuário atual.

---

## 🐍 **3. PYTHON - VALIDAÇÃO BACKEND**

### 🔶 **Arquivo Principal: cd_cadastro_usuario_sistema.py**
**Localização:** `app/api/endpoints/cd_cadastro_usuario_sistema.py`

#### 🔍 **VALIDAÇÃO 1 - Endpoint POST (linhas 125-155)**

```python
# Validações adicionais de formato e obrigatoriedade
email_regex = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
# 🔍 Telefone: aceita 10 dígitos (fixo) ou 11 dígitos (móvel) - apenas números
telefone_regex = r"^\d{10,11}$"
cpf_regex = r"^\d{11}$"
ramal_regex = r"^\d{4,10}$"

# ✅ Validação Telefone Pessoal
if not re.match(telefone_regex, telefone):
    log_requisicao(request, "FIM", "Telefone pessoal inválido")
    return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
        "request": request,
        "pfs": pfs,
        "mensagem_erro": "❌ Telefone pessoal inválido. Deve conter 10 ou 11 dígitos."
    })

# ✅ Validação Telefone Institucional
if not re.match(telefone_regex, telefone_institucional):
    log_requisicao(request, "FIM", "Telefone institucional inválido")
    return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
        "request": request,
        "pfs": pfs,
        "mensagem_erro": "❌ Telefone institucional inválido. Deve conter 10 ou 11 dígitos."
    })
```

#### 🔍 **VALIDAÇÃO 2 - Endpoint JSON (linhas 450-470)**

```python
# Validações de formato
email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
# 🔍 Telefone: aceita 10 dígitos (fixo) ou 11 dígitos (móvel) - apenas números
telefone_regex = r"^\d{10,11}$"
cpf_regex = r"^\d{11}$"
ramal_regex = r"^\d{4,}$"

# ✅ Validação Telefone Pessoal
if not re.match(telefone_regex, usuario_data.telefone):
    raise HTTPException(status_code=400, detail="Telefone pessoal inválido. Deve conter 10 ou 11 dígitos.")

# ✅ Validação Telefone Institucional    
if not re.match(telefone_regex, usuario_data.telefone_institucional):
    raise HTTPException(status_code=400, detail="Telefone institucional inválido. Deve conter 10 ou 11 dígitos.")
```

---

## 🔄 **4. FLUXO COMPLETO DE DADOS**

```
👤 USUÁRIO DIGITA: "11987654321"
    ↓
🎨 FRONTEND FORMATA: "(11) 98765-4321" (visual)
    ↓
✅ FRONTEND VALIDA: /^\(\d{2}\) \d{5}-\d{4}$/ → ✅ Válido
    ↓
🧹 PRÉ-ENVIO LIMPA: "11987654321" (apenas dígitos)
    ↓
📤 ENVIA PARA BACKEND: "11987654321"
    ↓
🔍 BACKEND VALIDA: /^\d{10,11}$/ → ✅ Válido (11 dígitos)
    ↓
💾 ARMAZENA NO BANCO: "11987654321"
    ↓
👥 EXIBE NO PAINEL: "(11) 98765-4321" (formatado novamente)
```

---

## ⚠️ **5. PONTOS CRÍTICOS RESOLVIDOS**

### ❌ **PROBLEMA ANTERIOR:**
- Hífen "-" era tratado como dígito constituinte
- Backend esperava formato: `(XX) XXXXX-XXXX`
- Validação: `r"^\(\d{2}\) \d{4,5}-\d{4}$"`

### ✅ **SOLUÇÃO ATUAL:**
- Hífen é apenas separador visual
- Backend recebe apenas dígitos: `11987654321`
- Validação: `r"^\d{10,11}$"`

### 🔧 **ARQUIVOS MODIFICADOS:**
1. ✅ `formatacao_telefone_movel.js` - Formatação unificada
2. ✅ `formulario_usuario_unificado.js` - Limpeza pré-envio
3. ✅ `cd_cadastro_usuario_sistema.py` - Validação backend
4. ✅ `cd_cadastro_usuario.html` - Importação correta dos scripts

---

## 🎯 **6. REGEX UTILIZADAS**

### 🎨 **Frontend (Validação Visual):**
```javascript
const regexFixo = /^\(\d{2}\) \d{4}-\d{4}$/;    // (XX) XXXX-XXXX
const regexMovel = /^\(\d{2}\) \d{5}-\d{4}$/;   // (XX) XXXXX-XXXX
```

### 🧹 **Limpeza (Pré-envio):**
```javascript
v.replace(/\D/g, '');  // Remove tudo que não é dígito
```

### 🔍 **Backend (Validação Final):**
```python
telefone_regex = r"^\d{10,11}$"  # 10 ou 11 dígitos puros
```

---

## ✅ **7. STATUS ATUAL**

- 🎨 **Formatação Visual:** ✅ Funcionando
- 🧹 **Limpeza Pré-envio:** ✅ Funcionando  
- 🔍 **Validação Backend:** ✅ Funcionando
- 💾 **Armazenamento:** ✅ Apenas dígitos
- 👥 **Exibição Painéis:** ✅ Formatação correta
- ⚠️ **Hífen como dígito:** ❌ **RESOLVIDO**
