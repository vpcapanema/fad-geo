// JS de validação visual e máscaras para cadastro de Pessoa Física (padrão FAD)
// Inspirado em formulario_usuario_unificado.js

import { formatarCPF, validarCPF } from '/static/js/formatacao_valores_campos/formatacao_cpf.js';
import { formatarTelefone, validarTelefone } from '/static/js/formatacao_valores_campos/formatacao_telefone_movel.js';
import { formatarTelefoneFixo, validarTelefoneFixo } from '/static/js/formatacao_valores_campos/formatacao_telefone_fixo.js';
import { formatarCEP, validarCEP } from '/static/js/formatacao_valores_campos/formatacao_cep.js';
import { formatarEmail, validarEmail } from '/static/js/formatacao_valores_campos/formatacao_email.js';

document.addEventListener('DOMContentLoaded', function() {  // Função para atualizar visual do campo
  function atualizarValidacaoCampo(inputElement, isValid) {
    const label = inputElement.closest('.form-field').querySelector('label');
    const check = label ? label.querySelector('.check-icone') : null;
    const asterisco = label ? label.querySelector('.obrigatorio-icone') : null;
    
    // Feedback especial para telefone - mostra tipo detectado
    if (inputElement.id === 'telefone') {
      const feedbackTipo = document.getElementById('telefone-tipo');
      const digitos = inputElement.value.replace(/\D/g, '');
      
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
    
    if (!inputElement.value) {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      inputElement.classList.remove('erro-campo');
      inputElement.closest('.form-field').classList.remove('campo-validado');
      return;
    }
    if (isValid) {
      if (asterisco) asterisco.style.display = 'none';
      if (check) check.style.display = 'inline';
      inputElement.classList.remove('erro-campo');
      inputElement.closest('.form-field').classList.add('campo-validado');
    } else {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      inputElement.classList.add('erro-campo');
      inputElement.closest('.form-field').classList.remove('campo-validado');
    }
  }
  // Máscaras e validações
  function mascaraCPF(v) { return formatarCPF(v); }
  
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
    return str.toLowerCase().replace(/(^|\s|\b)([a-záéíóúãõâêîôûç])([a-záéíóúãõâêîôûç]*)/g, function(m, sep, ini, rest) {
      if (["da","de","do","das","dos","e"].includes(ini+rest)) return sep+ini+rest;
      return sep+ini.toUpperCase()+rest;
    });
  }  // Regras de validação
  const regras = {
    nome: v => v && v.length >= 3,
    cpf: v => validarCPF(v),
    email: v => validarEmail(v),
    telefone: v => validarTelefoneInteligente(v),
    rua: v => v && v.length >= 3,
    numero: v => !!v,
    complemento: v => !!v,
    cep: v => validarCEP(v),
    bairro: v => v && v.length >= 2,
    cidade: v => v && v.length >= 2,
    uf: v => /^[A-Z]{2}$/.test(v)
  };  // Aplica eventos - TODOS com 'input' para validação instantânea
  Object.keys(regras).forEach(id => {
    const input = document.getElementById(id);
    if (!input) return;
    input.addEventListener('input', function() {
      // Máscara e formatação
      if (id === 'cpf') this.value = mascaraCPF(this.value);
      if (id === 'telefone') this.value = mascaraTelefoneInteligente(this.value);
      if (['nome','cidade','bairro','rua'].includes(id)) this.value = capitalizarNome(this.value);
      if (id === 'email') this.value = formatarEmail(this.value);
      atualizarValidacaoCampo(this, regras[id](this.value));
      checarTodosCamposValidos();
    });
    // Mantém o blur apenas para garantir validação ao sair do campo
    input.addEventListener('blur', function() {
      atualizarValidacaoCampo(this, regras[id](this.value));
      checarTodosCamposValidos();
    });
  });
  // Adiciona evento de input para o campo UF (select) para validação instantânea
  const ufSelect = document.getElementById('uf');
  if (ufSelect) {
    ufSelect.addEventListener('change', function() {
      atualizarValidacaoCampo(this, regras.uf(this.value));
      checarTodosCamposValidos();
    });
  }
  
  // Checa todos os campos obrigatórios
  // Atualiza o botão para verde quando ativo
  function checarTodosCamposValidos() {
    const obrigatorios = document.querySelectorAll('.form-field input[required], .form-field select[required]');
    let todosValidos = true;
    obrigatorios.forEach(el => {
      if (!el.closest('.campo-validado')) todosValidos = false;
    });
    const btn = document.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = !todosValidos;
      if (todosValidos) btn.classList.add('ativo');
      else btn.classList.remove('ativo');
    }
  }
  checarTodosCamposValidos();

  // ENVIO DO FORMULÁRIO VIA FETCH (PF)
  const form = document.getElementById('pfForm');
  if (form) {
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
        const resp = await fetch('/cadastro/pessoa-fisica', {
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
  }  // Busca automática de endereço ao digitar o CEP
  const cepInput = document.getElementById('cep');
  if (cepInput) {
    // Adiciona formatação instantânea do CEP
    cepInput.addEventListener('input', function() {
      this.value = formatarCEP(this.value);
      atualizarValidacaoCampo(this, validarCEP(this.value));
      checarTodosCamposValidos();
    });
    
    cepInput.addEventListener('blur', async function() {
      const cep = cepInput.value.replace(/\D/g, '');
      if (cep.length === 8) {
        try {
          const resp = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
          const data = await resp.json();
          if (!data.erro) {
            if (document.getElementById('rua')) {
              document.getElementById('rua').value = data.logradouro || '';
              // Dispara evento para validar o campo rua preenchido automaticamente
              document.getElementById('rua').dispatchEvent(new Event('input'));
            }
            if (document.getElementById('bairro')) {
              document.getElementById('bairro').value = data.bairro || '';
              // Dispara evento para validar o campo bairro preenchido automaticamente
              document.getElementById('bairro').dispatchEvent(new Event('input'));
            }
            if (document.getElementById('cidade')) {
              document.getElementById('cidade').value = data.localidade || '';
              // Dispara evento para validar o campo cidade preenchido automaticamente
              document.getElementById('cidade').dispatchEvent(new Event('input'));
            }
            if (document.getElementById('uf')) {
              document.getElementById('uf').value = data.uf || '';
              // Dispara evento para validar o campo uf preenchido automaticamente
              document.getElementById('uf').dispatchEvent(new Event('input'));
            }
          }
        } catch (e) {
          // Silencia erro de rede
        }
      }
    });
  }
});
