// Formatação e validação dinâmica de CEP (XXXXX-XXX)
const cepInput = document.getElementById('cep');
if (cepInput) {
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-cep';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  cepInput.parentNode.appendChild(msg);

  cepInput.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 8) v = v.slice(0, 8);
    if (v.length > 5) v = v.replace(/(\d{5})(\d{1,3})/, '$1-$2');
    e.target.value = v;
    if (/^\d{5}-\d{3}$/.test(v)) {
      msg.style.display = 'none';
      cepInput.classList.add('campo-validado');
    } else {
      msg.textContent = 'CEP inválido';
      msg.style.display = 'block';
      cepInput.classList.remove('campo-validado');
    }
    atualizarValidacaoCampo(cepInput, /^\d{5}-\d{3}$/.test(v));
  });
  cepInput.dispatchEvent(new Event('input'));
}

// formatacao_cep.js como módulo ES6
export function formatarCEP(valor) {
  let v = valor.replace(/\D/g, '');
  if (v.length > 8) v = v.slice(0, 8);
  if (v.length > 5) v = v.replace(/(\d{5})(\d{1,3})/, '$1-$2');
  return v;
}
export function validarCEP(valor) {
  if (!valor || valor.trim() === "") return true; // Não mostra erro se vazio
  return /^\d{5}-\d{3}$/.test(valor);
}
