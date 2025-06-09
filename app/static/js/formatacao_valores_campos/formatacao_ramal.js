// Formatação e validação dinâmica de ramal (mínimo 4 dígitos)
const ramalInput = document.getElementById('ramal');
const ramalLabel = document.querySelector('label[for="ramal"]');
if (ramalInput && ramalLabel) {
  ramalInput.addEventListener('input', function (e) {
    const v = e.target.value.trim();
    const valido = /^\d{4,10}$/.test(v);
    const check = ramalLabel.querySelector('.check-icone');
    const asterisco = ramalLabel.querySelector('.obrigatorio-icone');
    if (!v) {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      ramalLabel.classList.remove('campo-validado');
      ramalInput.classList.remove('erro-campo');
      return;
    }
    if (valido) {
      if (asterisco) asterisco.style.display = 'none';
      if (check) check.style.display = 'inline';
      ramalLabel.classList.add('campo-validado');
      ramalInput.classList.remove('erro-campo');
    } else {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      ramalLabel.classList.remove('campo-validado');
      ramalInput.classList.add('erro-campo');
    }
  });
  ramalInput.dispatchEvent(new Event('input'));
}

if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}
