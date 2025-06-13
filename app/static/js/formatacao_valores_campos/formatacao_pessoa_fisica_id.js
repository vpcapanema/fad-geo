// Formatação e validação dinâmica de ID Pessoa Física
const pfIdInput = document.getElementById('pessoa_fisica_id');
const pfIdLabel = document.querySelector('label[for="pessoa_fisica_id"]');
if (pfIdInput && pfIdLabel) {
  pfIdInput.addEventListener('input', function (e) {
    const v = e.target.value.trim();
    const valido = /^\d+$/.test(v) && parseInt(v) > 0;
    const check = pfIdLabel.querySelector('.check-icone');
    const asterisco = pfIdLabel.querySelector('.obrigatorio-icone');
    
    if (!v) {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      pfIdLabel.closest('.form-field').classList.remove('campo-validado');
      pfIdInput.classList.remove('erro-campo');
      return;
    }
    
    if (valido) {
      if (asterisco) asterisco.style.display = 'none';
      if (check) check.style.display = 'inline';
      pfIdLabel.closest('.form-field').classList.add('campo-validado');
      pfIdInput.classList.remove('erro-campo');
    } else {
      if (asterisco) asterisco.style.display = 'inline';
      if (check) check.style.display = 'none';
      pfIdLabel.closest('.form-field').classList.remove('campo-validado');
      pfIdInput.classList.add('erro-campo');
    }
    
    // Chama a função de validação geral
    if (typeof window.checarTodosCamposValidos === 'function') {
      window.checarTodosCamposValidos();
    }
  });
  
  pfIdInput.dispatchEvent(new Event('input'));
}

if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}
