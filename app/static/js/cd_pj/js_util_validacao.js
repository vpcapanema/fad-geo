// js_util_validacao.js
// Utilitários de validação e feedback visual para formulários FAD

export function atualizarValidacaoCampo(inputElement, isValid) {
  const label = inputElement.closest('.form-field').querySelector('label');
  let check = label ? label.querySelector('.check-icone') : null;
  let asterisco = label ? label.querySelector('.obrigatorio-icone') : null;
  if (!check) {
    check = document.createElement('span');
    check.className = 'check-icone';
    check.innerHTML = '&#10003;';
    label.appendChild(check);
  }
  if (!asterisco) {
    asterisco = document.createElement('span');
    asterisco.className = 'obrigatorio-icone';
    asterisco.innerHTML = '*';
    label.appendChild(asterisco);
  }
  if (!inputElement.value) {
    asterisco.style.display = 'inline';
    check.style.display = 'none';
    inputElement.classList.remove('erro-campo');
    inputElement.closest('.form-field').classList.remove('campo-validado');
    return;
  }
  if (isValid) {
    asterisco.style.display = 'none';
    check.style.display = 'inline';
    inputElement.classList.remove('erro-campo');
    inputElement.closest('.form-field').classList.add('campo-validado');
  } else {
    asterisco.style.display = 'inline';
    check.style.display = 'none';
    inputElement.classList.add('erro-campo');
    inputElement.closest('.form-field').classList.remove('campo-validado');
  }
}

export function checarTodosCamposValidos(formSelector, submitBtnSelector) {
  const obrigatorios = document.querySelectorAll(formSelector + ' .form-field input[required]');
  let todosValidos = true;
  obrigatorios.forEach(el => {
    if (!el.closest('.campo-validado')) todosValidos = false;
  });
  const btn = document.querySelector(submitBtnSelector);
  if (btn) {
    btn.disabled = !todosValidos;
    if (todosValidos) btn.classList.add('ativo');
    else btn.classList.remove('ativo');
  }
}
