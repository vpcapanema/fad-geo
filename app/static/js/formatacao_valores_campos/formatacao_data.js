// Formatação e validação dinâmica de data (DD/MM/AAAA)
const dataInputs = document.querySelectorAll('input[type="date"], .input-data');
dataInputs.forEach(function(dataInput) {
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-data';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  dataInput.parentNode.appendChild(msg);

  function validarData(v) {
    return /^\d{2}\/\d{2}\/\d{4}$/.test(v);
  }

  dataInput.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 8) v = v.slice(0, 8);
    if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{1,4})/, '$1/$2/$3');
    else if (v.length > 2) v = v.replace(/(\d{2})(\d{1,2})/, '$1/$2');
    e.target.value = v;
    if (validarData(v)) {
      msg.style.display = 'none';
      dataInput.classList.add('campo-validado');
    } else {
      msg.textContent = 'Data inválida';
      msg.style.display = 'block';
      dataInput.classList.remove('campo-validado');
    }
    atualizarValidacaoCampo(dataInput, validarData(v));
  });
  dataInput.dispatchEvent(new Event('input'));
});
