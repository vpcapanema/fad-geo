// Garante que atualizarValidacaoCampo está definida antes de ser usada, evitando ReferenceError caso o arquivo unificado ainda não tenha sido carregado.
if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}

// Formatação e validação dinâmica de CPF
const cpfInput = document.getElementById('cpf');
if (cpfInput) {
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-cpf';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  cpfInput.parentNode.appendChild(msg);

  cpfInput.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);
    // Aplica a máscara fixa
    let formatado = '___.___.___-__';
    for (let i = 0, j = 0; i < formatado.length && j < v.length; i++) {
      if (formatado[i] === '.' || formatado[i] === '-') continue;
      formatado = formatado.substring(0, i) + v[j] + formatado.substring(i + 1);
      j++;
    }
    e.target.value = formatado;
    // Verifica se está completo e só tem dígitos
    const completo = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(formatado);
    if (!v) {
      msg.style.display = 'none';
      cpfInput.classList.remove('erro-campo');
      atualizarValidacaoCampo(cpfInput, false);
      return;
    }
    if (completo) {
      msg.style.display = 'none';
      cpfInput.classList.remove('erro-campo');
    } else {
      msg.textContent = 'CPF inválido';
      msg.style.display = 'block';
      cpfInput.classList.add('erro-campo');
    }
    atualizarValidacaoCampo(cpfInput, completo);
  });
  cpfInput.dispatchEvent(new Event('input'));

  // Garante que só exista UM asterisco e UM check por campo, removendo duplicados se houver
  const label = cpfInput.closest('.form-field').querySelector('label');
  if (label) {
    const obrigatorios = label.querySelectorAll('.obrigatorio-icone');
    const checks = label.querySelectorAll('.check-icone');
    obrigatorios.forEach((el, i) => { if (i > 0) el.remove(); });
    checks.forEach((el, i) => { if (i > 0) el.remove(); });
  }
}

// formatacao_cpf.js como módulo ES6
export function formatarCPF(valor) {
  let v = valor.replace(/\D/g, '');
  if (v.length > 11) v = v.slice(0, 11);
  v = v.replace(/(\d{3})(\d)/, "$1.$2");
  v = v.replace(/(\d{3})(\d)/, "$1.$2");
  v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  return v;
}
export function validarCPF(valor) {
  return /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(valor);
}
