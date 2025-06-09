// Formatação e validação dinâmica de e-mail institucional constitucional brasileiro
const emailInstInput = document.getElementById('email_institucional');
const emailInstLabel = document.querySelector('label[for="email_institucional"]');
if (emailInstInput && emailInstLabel) {
  emailInstInput.addEventListener('input', function (e) {
    const v = e.target.value.trim();
    const valido = /^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$/.test(v);
    const check = emailInstLabel.querySelector('.check-icone');
    const asterisco = emailInstLabel.querySelector('.obrigatorio-icone');
    if (!v) {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      emailInstLabel.classList.remove('campo-validado');
      emailInstInput.classList.remove('erro-campo');
      return;
    }
    if (valido) {
      if (asterisco) asterisco.style.display = 'none';
      if (check) check.style.display = 'inline';
      emailInstLabel.classList.add('campo-validado');
      emailInstInput.classList.remove('erro-campo');
    } else {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      emailInstLabel.classList.remove('campo-validado');
      emailInstInput.classList.add('erro-campo');
    }
  });
  emailInstInput.dispatchEvent(new Event('input'));
}

if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}
