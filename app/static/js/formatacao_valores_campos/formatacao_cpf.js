// Garante que atualizarValidacaoCampo está definida antes de ser usada, evitando ReferenceError caso o arquivo unificado ainda não tenha sido carregado.
if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}

// Formatação e validação dinâmica de CPF (abordagem igual telefone)
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
    // Máscara CPF: 999.999.999-99
    if (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{0,2})/, '$1.$2.$3-$4');
    else if (v.length > 6) v = v.replace(/(\d{3})(\d{3})(\d{0,3})/, '$1.$2.$3');
    else if (v.length > 3) v = v.replace(/(\d{3})(\d{0,3})/, '$1.$2');
    else v = v.replace(/(\d{0,3})/, '$1');
    e.target.value = v;
    if (!v) {
      msg.style.display = 'none';
      cpfInput.classList.remove('erro-campo');
      atualizarValidacaoCampo(cpfInput, false);
      return;
    }
    if (/^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(v)) {
      msg.style.display = 'none';
      cpfInput.classList.remove('erro-campo');
    } else {
      msg.textContent = 'CPF inválido';
      msg.style.display = 'block';
      cpfInput.classList.add('erro-campo');
    }
    atualizarValidacaoCampo(cpfInput, /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(v));
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

// Removido export para uso direto em <script>
// export function formatarCPF(valor) {
//   let v = valor.replace(/\D/g, '');
//   if (v.length > 11) v = v.slice(0, 11);
//   v = v.replace(/(\d{3})(\d)/, "$1.$2");
//   v = v.replace(/(\d{3})(\d)/, "$1.$2");
//   v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
//   return v;
// }
// export function validarCPF(valor) {
//   return /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(valor);
// }
