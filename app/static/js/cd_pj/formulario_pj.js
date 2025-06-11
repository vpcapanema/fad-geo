import { atualizarValidacaoCampo, checarTodosCamposValidos } from './js_util_validacao.js';
import { formatarCNPJ, validarCNPJ } from '/static/js/formatacao_valores_campos/formatacao_cnpj.js';
import { formatarTelefone, validarTelefone } from '/static/js/formatacao_valores_campos/formatacao_telefone_movel.js';
import { formatarTelefoneFixo, validarTelefoneFixo } from '/static/js/formatacao_valores_campos/formatacao_telefone_fixo.js';
import { formatarCEP, validarCEP } from '/static/js/formatacao_valores_campos/formatacao_cep.js';
import { formatarEmail, validarEmail } from '/static/js/formatacao_valores_campos/formatacao_email.js';
import { validarRazaoSocialPJ, formatarRazaoSocialPJ } from '/static/js/formatacao_valores_campos/formatacao_razao_social_pj.js';

function mascaraCNPJ(v) { return formatarCNPJ(v); }

// Função inteligente para telefone - detecta se é móvel ou fixo
function mascaraTelefoneInteligente(valor) {
  let digitos = valor.replace(/\D/g, '');
  
  // Se tem 11 dígitos, é celular
  if (digitos.length === 11) {
    return formatarTelefone(valor);
  }
  // Se tem 10 dígitos ou menos, é fixo
  else {
    return formatarTelefoneFixo(valor);
  }
}

// Função inteligente para validar telefone - detecta se é móvel ou fixo
function validarTelefoneInteligente(valor) {
  let digitos = valor.replace(/\D/g, '');
  
  // Se tem 11 dígitos, valida como celular
  if (digitos.length === 11) {
    return validarTelefone(valor);
  }
  // Se tem 10 dígitos, valida como fixo
  else if (digitos.length === 10) {
    return validarTelefoneFixo(valor);
  }
  // Se não tem 10 nem 11 dígitos, é inválido
  else {
    return false;
  }
}

function capitalizarNome(str) {
  return str.toUpperCase();
}

// Função para formatar texto padrão ABNT (primeira letra maiúscula, exceto preposições)
function formatarABNT(str) {
  if (!str) return '';
  const preps = ['da','de','do','das','dos','e','em','na','no','nas','nos','a','o','as','os','por','para','com','sem','sob','sobre','após','ante','até','contra','desde'];
  return str.toLowerCase().replace(/\b(\w)(\w*)\b/g, (m, ini, rest) => {
    const palavra = ini + rest;
    return preps.includes(palavra) ? palavra : ini.toUpperCase() + rest;
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('pjForm');
  if (!form) return;  const campos = [
    {id: 'razao_social', custom: validarRazaoSocialPJ, format: v => v.toUpperCase()},
    {id: 'cnpj', mask: mascaraCNPJ, regex: /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/, custom: validarCNPJ},
    {id: 'nome_fantasia', format: v => v.toUpperCase(), regex: /^.{3,}$/},
    {id: 'telefone_institucional', mask: mascaraTelefoneInteligente, custom: validarTelefoneInteligente},
    {id: 'email', regex: /^[\w-.]+@[\w-]+\.[a-z]{2,}$/i},
    {id: 'cep', mask: v => formatarCEP(v), custom: validarCEP},
    {id: 'bairro', format: formatarABNT, regex: /^.{2,}$/},
    {id: 'rua', format: formatarABNT, regex: /^.{3,}$/},
    {id: 'numero', regex: /^.{1,}$/},
    {id: 'complemento', format: formatarABNT, regex: /^.{1,}$/},
    {id: 'uf', regex: /^[A-Z]{2}$/},
    {id: 'cidade', format: formatarABNT, regex: /^.{2,}$/}
  ];  campos.forEach(({id, regex, mask, format, custom}) => {
    const input = document.getElementById(id);
    if (!input) return;
    input.addEventListener('input', function() {
      if (mask) this.value = mask(this.value);
      if (format) this.value = format(this.value);
      
      // Feedback especial para telefone - mostra tipo detectado
      if (id === 'telefone_institucional') {
        const feedbackTipo = document.getElementById('telefone-tipo');
        const digitos = this.value.replace(/\D/g, '');
        
        if (digitos.length >= 10) {
          if (digitos.length === 11) {
            feedbackTipo.textContent = '📱 Celular detectado';
            feedbackTipo.style.color = '#28a745';
          } else if (digitos.length === 10) {
            feedbackTipo.textContent = '📞 Telefone fixo detectado';
            feedbackTipo.style.color = '#007bff';
          }
          feedbackTipo.style.display = 'block';
        } else {
          feedbackTipo.style.display = 'none';
        }
      }
      
      let valido = custom ? custom(this.value) : (regex ? regex.test(this.value) : !!this.value);
      atualizarValidacaoCampo(this, valido);
      checarTodosCamposValidos('#pjForm', 'button[type="submit"]');
    });
    input.addEventListener('blur', function() {
      if (mask) this.value = mask(this.value);
      if (format) this.value = format(this.value);
      let valido = custom ? custom(this.value) : (regex ? regex.test(this.value) : !!this.value);
      atualizarValidacaoCampo(this, valido);
      checarTodosCamposValidos('#pjForm', 'button[type="submit"]');
    });
  });
  // Adiciona evento para campo UF (select) para validação instantânea
  const ufSelect = document.getElementById('uf');
  if (ufSelect) {
    ufSelect.addEventListener('change', function() {
      let valido = this.value !== '';
      atualizarValidacaoCampo(this, valido);
      checarTodosCamposValidos('#pjForm', 'button[type="submit"]');
    });
  }
  
  // Adiciona evento para campo cidade (select) para validação instantânea
  const cidadeSelect = document.getElementById('cidade');
  if (cidadeSelect) {
    cidadeSelect.addEventListener('change', function() {
      let valido = this.value !== '';
      atualizarValidacaoCampo(this, valido);
      checarTodosCamposValidos('#pjForm', 'button[type="submit"]');
    });
  }
  
  checarTodosCamposValidos('#pjForm', 'button[type="submit"]');

  // Padronização visual e envio do formulário PJ
  form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;
    const sucessoBox = document.getElementById('sucessoBox');
    const erroBox = document.getElementById('erroBox');
    const okBtnContainer = document.getElementById('okBtnContainer');
    if (sucessoBox) sucessoBox.style.display = 'none';
    if (erroBox) erroBox.style.display = 'none';
    if (okBtnContainer) okBtnContainer.style.display = 'none';
    // Monta dados
    const formData = new FormData(form);
    const dados = {};
    formData.forEach((v, k) => dados[k] = v);
    try {
      const resp = await fetch('/cadastro/pessoa-juridica', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
      });
      if (resp.ok) {
        if (sucessoBox) {
          sucessoBox.textContent = 'Cadastro realizado com sucesso!';
          sucessoBox.style.display = 'block';
        }
        form.reset();
        document.querySelectorAll('.campo-validado').forEach(e => e.classList.remove('campo-validado'));
      } else {
        const data = await resp.json();
        if (erroBox) {
          erroBox.textContent = data.detail || 'Erro ao cadastrar.';
          erroBox.style.display = 'block';
        }
      }
    } catch (e) {
      if (erroBox) {
        erroBox.textContent = 'Erro de conexão.';
        erroBox.style.display = 'block';
      }
    }
    if (okBtnContainer) okBtnContainer.style.display = 'block';
    if (btn) btn.disabled = false;
  });
  // Botão OK recarrega a página
  const okBtn = document.getElementById('okBtn');
  if (okBtn) {
    okBtn.addEventListener('click', function() {
      window.location.reload();
    });
  }

  // Remove asteriscos duplicados no carregamento
  document.querySelectorAll('.form-field label').forEach(label => {
    const obrigatorios = label.querySelectorAll('.obrigatorio-icone');
    obrigatorios.forEach((el, i) => { if (i > 0) el.remove(); });
  });

  // --- CORRIGE VALIDAÇÃO INSTANTÂNEA E FEEDBACK VISUAL ---
  // Validação e feedback visual automáticos para todos os campos, inclusive após preenchimento automático
  function validarEAtualizarTodosCampos() {
    campos.forEach(({id, regex, mask, format, custom}) => {
      const input = document.getElementById(id);
      if (!input) return;
      let valor = input.value;
      if (mask) valor = mask(valor);
      if (format) valor = format(valor);
      input.value = valor;
      let valido = custom ? custom(valor) : (regex ? regex.test(valor) : !!valor);
      atualizarValidacaoCampo(input, valido);
    });
    checarTodosCamposValidos('#pjForm', 'button[type="submit"]');
  }

  // Chama sempre que qualquer campo muda OU é preenchido automaticamente
  form.addEventListener('input', validarEAtualizarTodosCampos);
  form.addEventListener('change', validarEAtualizarTodosCampos);

  // Após preenchimento automático (CNPJ/CEP), dispara validação instantânea
  function preencherCampo(id, valor) {
    const input = document.getElementById(id);
    if (input) {
      input.value = valor || '';
      input.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }
  // --- BUSCA AUTOMÁTICA CEP COM TRIGGER NO INPUT ---
  const cepInput = document.getElementById('cep');
  if (cepInput) {
    let timeoutCep;
    
    cepInput.addEventListener('input', function() {
      const msg = document.getElementById('cep-erro');
      const cep = this.value.replace(/\D/g, '');
      
      // Limpa timeout anterior
      clearTimeout(timeoutCep);
      
      if (msg) {
        if (!this.value) {
          msg.textContent = '';
        } else if (!validarCEP(this.value)) {
          msg.textContent = 'CEP inválido';
        } else {
          msg.textContent = '';
        }
      }
      
      // Se CEP tem 8 dígitos, agenda busca automática após 500ms
      if (cep.length === 8) {
        timeoutCep = setTimeout(async () => {
          try {
            const resp = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await resp.json();
            if (!data.erro) {
              preencherCampo('rua', data.logradouro);
              preencherCampo('bairro', data.bairro);
              preencherCampo('cidade', data.localidade);
              preencherCampo('uf', data.uf);
            }
          } catch (e) {
            console.log('Erro ao buscar CEP:', e);
          }
        }, 500);
      }
    });
  }
  // --- BUSCA AUTOMÁTICA CNPJ COM TRIGGER NO INPUT ---
  const cnpjInput = document.getElementById('cnpj');
  if (cnpjInput) {
    let timeoutCnpj;
    
    cnpjInput.addEventListener('input', function() {
      const cnpj = this.value.replace(/\D/g, '');
      
      // Limpa timeout anterior
      clearTimeout(timeoutCnpj);
      
      // Se CNPJ tem 14 dígitos, agenda busca automática após 1 segundo
      if (cnpj.length === 14 && validarCNPJ(this.value)) {
        timeoutCnpj = setTimeout(async () => {
          const loadingMsg = document.getElementById('cnpj-loading');
          
          try {
            if (loadingMsg) {
              loadingMsg.innerHTML = '<div class="spinner"></div> Buscando dados da empresa...';
              loadingMsg.style.display = 'flex';
            }
            
            const resp = await fetch(`/proxy/receitaws/cnpj/${cnpj}`);
            const data = await resp.json();
            
            if (data.status === 'OK') {
              preencherCampo('razao_social', data.nome);
              preencherCampo('nome_fantasia', data.fantasia);
              preencherCampo('telefone_institucional', data.telefone);
              preencherCampo('email', data.email);
              preencherCampo('cep', data.cep);
              preencherCampo('rua', data.logradouro);
              preencherCampo('numero', data.numero);
              preencherCampo('complemento', data.complemento);
              preencherCampo('bairro', data.bairro);
              preencherCampo('cidade', data.municipio);
              preencherCampo('uf', data.uf);
              
              if (loadingMsg) {
                loadingMsg.innerHTML = '✅ Dados carregados com sucesso!';
                setTimeout(() => {
                  loadingMsg.style.display = 'none';
                }, 2000);
              }
            } else {
              if (loadingMsg) {
                loadingMsg.innerHTML = '⚠️ CNPJ não encontrado';
                setTimeout(() => {
                  loadingMsg.style.display = 'none';
                }, 3000);
              }
            }
          } catch (e) {
            console.log('Erro ao buscar CNPJ:', e);
            if (loadingMsg) {
              loadingMsg.innerHTML = '❌ Erro ao buscar dados';
              setTimeout(() => {
                loadingMsg.style.display = 'none';
              }, 3000);
            }
          }
        }, 1000);
      }
    });
  }

  // Ajusta estrutura HTML para .campo-validacao sobrepor label
  document.querySelectorAll('.form-field').forEach(field => {
    const label = field.querySelector('label');
    if (!label) return;
    // Remove duplicados antigos
    field.querySelectorAll('.campo-validacao').forEach(e => e.remove());
    // Cria container de validação
    const validacao = document.createElement('span');
    validacao.className = 'campo-validacao';
    // Move check e asterisco para dentro do container
    const check = label.querySelector('.check-icone');
    const obrigatorio = label.querySelector('.obrigatorio-icone');
    if (check) validacao.appendChild(check);
    if (obrigatorio) validacao.appendChild(obrigatorio);
    label.appendChild(validacao);
  });

  // --- CORRIGE ASTERISCO: SEMPRE VISÍVEL, SÓ SOME QUANDO O CAMPO ESTÁ VÁLIDO ---
  // --- LÓGICA DE VALIDAÇÃO VISUAL IGUAL AO USUÁRIO ---
  function atualizarValidacaoCampo(inputElement, isValid) {
    const label = inputElement.closest('.form-field').querySelector('label');
    const check = label ? label.querySelector('.check-icone') : null;
    const asterisco = label ? label.querySelector('.obrigatorio-icone') : null;
    // Campo vazio: só asterisco vermelho, sem erro visual
    if (!inputElement.value) {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      inputElement.classList.remove('erro-campo');
      inputElement.closest('.form-field').classList.remove('campo-validado');
      return;
    }
    // Campo válido: só checkpoint verde
    if (isValid) {
      if (asterisco) asterisco.style.display = 'none';
      if (check) check.style.display = 'inline';
      inputElement.classList.remove('erro-campo');
      inputElement.closest('.form-field').classList.add('campo-validado');
    } else {
      // Campo preenchido errado/incompleto: erro visual e mensagem
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      inputElement.classList.add('erro-campo');
      inputElement.closest('.form-field').classList.remove('campo-validado');
    }
  }
  // Garante que todos os asteriscos estejam visíveis ao carregar a página
  document.querySelectorAll('.form-field label .obrigatorio-icone').forEach(el => {
    el.style.display = 'inline';
  });
});
