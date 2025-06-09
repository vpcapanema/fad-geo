// Validação e formatação automática dos formulários de elementos rodoviários
// Aplica feedback visual (check, erro, borda, etc) e máscaras

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form[id$="Form"]');
  if (!form) return;
  // Detecta campos comuns
  const campos = Array.from(form.querySelectorAll('input, select')).filter(el => el.name && el.type !== 'hidden');
  function setValidacao(input, valido) {
    const field = input.closest('.form-field');
    if (valido) {
      field.classList.add('campo-validado');
      input.classList.remove('erro-campo');
    } else {
      field.classList.remove('campo-validado');
      input.classList.add('erro-campo');
    }
  }
  function validarCampo(input) {
    if (!input.value) return false;
    if (input.type === 'email') return /^[\w-.]+@[\w-]+\.[a-z]{2,}$/i.test(input.value);
    if (input.name === 'cpf') return /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(input.value);
    if (input.name === 'cnpj') return /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/.test(input.value);
    if (input.name === 'telefone' || input.name === 'celular') return /^\(\d{2}\) \d{4,5}-\d{4}$/.test(input.value);
    if (input.name === 'cep') return /^\d{5}-?\d{3}$/.test(input.value);
    if (input.name === 'uf') return /^[A-Z]{2}$/.test(input.value);
    return !!input.value.trim();
  }
  function aplicarFormatacao(input) {
    if (['denominacao','nome','cidade','bairro','rua','localizacao'].includes(input.name)) {
      input.value = capitalizarNome(input.value);
    }
    if (input.type === 'email') {
      input.value = input.value.toLowerCase();
    }
    if (input.name === 'cpf') {
      let v = input.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      v = v.replace(/(\d{3})(\d)/, "$1.$2");
      v = v.replace(/(\d{3})(\d)/, "$1.$2");
      v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
      input.value = v;
    }
    if (input.name === 'cnpj') {
      let v = input.value.replace(/\D/g, '');
      if (v.length > 14) v = v.slice(0, 14);
      v = v.replace(/(\d{2})(\d)/, "$1.$2");
      v = v.replace(/(\d{3})(\d)/, "$1.$2");
      v = v.replace(/(\d{3})(\d{4})(\d)/, "$1/$2-$3");
      input.value = v;
    }
    if (input.name === 'telefone' || input.name === 'celular') {
      let t = input.value.replace(/\D/g, '');
      if (t.length > 11) t = t.slice(0, 11);
      if (t.length === 11) {
        t = t.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
      } else if (t.length === 10) {
        t = t.replace(/(\d{2})(\d{4})(\d{4})/, "($1) $2-$3");
      }
      input.value = t;
    }
  }
  function capitalizarNome(str) {
    return str.toLowerCase().replace(/(^|\s|\b)([a-záéíóúãõâêîôûç])([a-záéíóúãõâêîôûç]*)/g, function(m, sep, ini, rest) {
      if (["da","de","do","das","dos","e"].includes(ini+rest)) return sep+ini+rest;
      return sep+ini.toUpperCase()+rest;
    });
  }
  campos.forEach(input => {
    input.addEventListener('input', function() {
      aplicarFormatacao(this);
      setValidacao(this, validarCampo(this));
    });
    input.addEventListener('blur', function() {
      aplicarFormatacao(this);
      setValidacao(this, validarCampo(this));
    });
  });
});
