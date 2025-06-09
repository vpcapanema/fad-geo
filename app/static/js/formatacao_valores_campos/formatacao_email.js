// Garante que atualizarValidacaoCampo está definida antes de ser usada, evitando ReferenceError caso o arquivo unificado ainda não tenha sido carregado.
if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}

// Formatação e validação dinâmica de e-mail
const emailInput = document.getElementById('email');
if (emailInput) {
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-email';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  emailInput.parentNode.appendChild(msg);

  emailInput.addEventListener('input', function (e) {
    const v = e.target.value.trim();
    if (!v) {
      msg.style.display = 'none';
      emailInput.classList.remove('erro-campo');
      atualizarValidacaoCampo(emailInput, false);
      return;
    }
    const valido = /^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$/.test(v);
    if (valido) {
      msg.style.display = 'none';
      emailInput.classList.remove('erro-campo');
    } else {
      msg.textContent = 'E-mail inválido';
      msg.style.display = 'block';
      emailInput.classList.add('erro-campo');
    }
    atualizarValidacaoCampo(emailInput, valido);
  });
  emailInput.dispatchEvent(new Event('input'));

  // Garante que só exista UM asterisco e UM check por campo, removendo duplicados se houver
  const label = emailInput.closest('.form-field').querySelector('label');
  if (label) {
    const obrigatorios = label.querySelectorAll('.obrigatorio-icone');
    const checks = label.querySelectorAll('.check-icone');
    obrigatorios.forEach((el, i) => { if (i > 0) el.remove(); });
    checks.forEach((el, i) => { if (i > 0) el.remove(); });
  }
}

// formatacao_email.js como módulo ES6
export function formatarEmail(valor) {
  return valor.trim().toLowerCase();
}
export function validarEmail(valor) {
  return /^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$/.test(valor.trim());
}
