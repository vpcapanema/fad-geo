// Garante que atualizarValidacaoCampo está definida antes de ser usada, evitando ReferenceError caso o arquivo unificado ainda não tenha sido carregado.
if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}

// Formatação e validação dinâmica de telefone
const telInput = document.getElementById('telefone_institucional');
if (telInput) {
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-telefone';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  telInput.parentNode.appendChild(msg);

  telInput.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);
    if (v.length > 6) v = v.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
    else if (v.length > 2) v = v.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    else v = v.replace(/(\d{0,2})/, '$1');
    e.target.value = v;
    if (!v) {
      msg.style.display = 'none';
      telInput.classList.remove('erro-campo');
      atualizarValidacaoCampo(telInput, false);
      return;
    }
    if (/^\(\d{2}\) \d{4,5}-\d{4}$/.test(v)) {
      msg.style.display = 'none';
      telInput.classList.remove('erro-campo');
    } else {
      msg.textContent = 'Telefone inválido';
      msg.style.display = 'block';
      telInput.classList.add('erro-campo');
    }
    atualizarValidacaoCampo(telInput, /^\(\d{2}\) \d{4,5}-\d{4}$/.test(v));
  });
  telInput.dispatchEvent(new Event('input'));
}

// Telefone institucional: aceita fixo (10 dígitos) ou celular (11 dígitos)
const telInputInst = document.getElementById('telefone_institucional');
const telInstLabel = document.querySelector('label[for="telefone_institucional"]');
// Corrige: só mostra check se não houver erro visual/mensagem
if (telInputInst && telInstLabel) {
  // Busca a div de mensagem já existente no HTML
  const msg = document.getElementById('msg-telefone-institucional');
  telInputInst.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);
    let formatado = '';
    let tipo = '';
    if (v.length === 11) {
      // Celular
      formatado = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
      tipo = 'celular';
    } else if (v.length === 10) {
      // Fixo
      formatado = v.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
      tipo = 'fixo';
    } else if (v.length > 2) {
      formatado = v.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else {
      formatado = v.replace(/(\d{0,2})/, '$1');
    }
    e.target.value = formatado;
    const check = telInstLabel.querySelector('.check-icone');
    const asterisco = telInstLabel.querySelector('.obrigatorio-icone');
    let valido = false;
    let erroVisual = false;
    if (!v) {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      telInstLabel.classList.remove('campo-validado');
      telInputInst.classList.remove('erro-campo');
      if (msg) msg.style.display = 'none';
      return;
    }
    if (tipo === 'celular' && /^\(\d{2}\) \d{5}-\d{4}$/.test(formatado)) {
      valido = true;
    } else if (tipo === 'fixo' && /^\(\d{2}\) \d{4}-\d{4}$/.test(formatado)) {
      valido = true;
    }
    if (valido) {
      if (asterisco) asterisco.style.display = 'none';
      if (check) check.style.display = 'inline';
      telInstLabel.classList.add('campo-validado');
      telInputInst.classList.remove('erro-campo');
      if (msg) msg.style.display = 'none';
    } else {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      telInstLabel.classList.remove('campo-validado');
      telInputInst.classList.add('erro-campo');
      if (msg) {
        msg.textContent = 'Telefone inválido';
        msg.style.display = 'block';
      }
    }
  });
  telInputInst.dispatchEvent(new Event('input'));
}

// Formatação e validação dinâmica de telefone pessoal
const telInputPessoal = document.getElementById('telefone');
if (telInputPessoal) {
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-telefone';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  telInputPessoal.parentNode.appendChild(msg);

  telInputPessoal.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);
    if (v.length > 6) v = v.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
    else if (v.length > 2) v = v.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    else v = v.replace(/(\d{0,2})/, '$1');
    e.target.value = v;
    if (!v) {
      msg.style.display = 'none';
      telInputPessoal.classList.remove('erro-campo');
      atualizarValidacaoCampo(telInputPessoal, false);
      return;
    }
    if (/^\(\d{2}\) \d{4,5}-\d{4}$/.test(v)) {
      msg.style.display = 'none';
      telInputPessoal.classList.remove('erro-campo');
    } else {
      msg.textContent = 'Telefone inválido';
      msg.style.display = 'block';
      telInputPessoal.classList.add('erro-campo');
    }
    atualizarValidacaoCampo(telInputPessoal, /^\(\d{2}\) \d{4,5}-\d{4}$/.test(v));
  });
  telInputPessoal.dispatchEvent(new Event('input'));

  // Garante que só exista UM asterisco e UM check por campo, removendo duplicados se houver
  const label = telInputPessoal.closest('.form-field').querySelector('label');
  if (label) {
    const obrigatorios = label.querySelectorAll('.obrigatorio-icone');
    const checks = label.querySelectorAll('.check-icone');
    obrigatorios.forEach((el, i) => { if (i > 0) el.remove(); });
    checks.forEach((el, i) => { if (i > 0) el.remove(); });
  }
}

// formatacao_telefone.js como módulo ES6
export function formatarTelefone(valor) {
  let v = valor.replace(/\D/g, '');
  if (v.length > 11) v = v.slice(0, 11);
  if (v.length === 11) {
    v = v.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
  } else if (v.length === 10) {
    v = v.replace(/(\d{2})(\d{4})(\d{4})/, "($1) $2-$3");
  }
  return v;
}
export function validarTelefone(valor) {
  return /^\(\d{2}\) \d{4,5}-\d{4}$/.test(valor);
}
