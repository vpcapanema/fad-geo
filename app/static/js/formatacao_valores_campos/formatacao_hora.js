// Formatação e validação dinâmica de hora (HH:MM)
const horaInputs = document.querySelectorAll('input[type="time"], .input-hora');
horaInputs.forEach(function(horaInput) {
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-hora';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  horaInput.parentNode.appendChild(msg);

  function validarHora(v) {
    return /^([01]?\d|2[0-3]):[0-5]\d$/.test(v);
  }

  horaInput.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 4) v = v.slice(0, 4);
    if (v.length > 2) v = v.replace(/(\d{2})(\d{1,2})/, '$1:$2');
    e.target.value = v;
    if (validarHora(v)) {
      msg.style.display = 'none';
      horaInput.classList.add('campo-validado');
    } else {
      msg.textContent = 'Hora inválida';
      msg.style.display = 'block';
      horaInput.classList.remove('campo-validado');
    }
    atualizarValidacaoCampo(horaInput, validarHora(v));
  });
  horaInput.dispatchEvent(new Event('input'));
});
