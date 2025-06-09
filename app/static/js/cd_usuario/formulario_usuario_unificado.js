// Centralizador de formatação e validação dos campos do cadastro de usuário
// Importa e executa a lógica de cada arquivo de formatação/validação

// Remover imports ES6, pois não são suportados em <script> tradicional
// Em vez disso, garantir que todos os arquivos de formatação/validação estejam importados via <script src="..."> no HTML
// Centralizar apenas a lógica de checagem de campos obrigatórios e liberação do botão

window.checarTodosCamposValidos = function() {
  const obrigatorios = document.querySelectorAll('.form-field input[required], .form-field select[required]');
  let todosValidos = true;
  obrigatorios.forEach(el => {
    if (!el.closest('.campo-validado')) todosValidos = false;
  });
  const btn = document.querySelector('button[type="submit"]');
  if (btn) btn.disabled = !todosValidos;
};

window.atualizarValidacaoCampo = function(inputElement, isValid) {
  const label = inputElement.closest('.form-field').querySelector('label');
  const check = label ? label.querySelector('.check-icone') : null;
  const asterisco = label ? label.querySelector('.obrigatorio-icone') : null;
  // Campo vazio: só asterisco vermelho, sem erro visual
  if (!inputElement.value) {
    if (asterisco) asterisco.style.display = 'inline';
    if (check) check.style.display = 'none';
    inputElement.classList.remove('erro-campo');
    inputElement.closest('.form-field').classList.remove('campo-validado');
    return;
  }
  // Campo válido: só checkpoint verde
  if (isValid) {
    if (asterisco) asterisco.style.display = 'none';
    if (check) check.style.display = 'inline';
    inputElement.classList.remove('erro-campo');
    inputElement.closest('.form-field').classList.add('campo-validado');
  } else {
    // Campo preenchido errado/incompleto: erro visual e mensagem
    if (asterisco) asterisco.style.display = 'inline';
    if (check) check.style.display = 'none';
    inputElement.classList.add('erro-campo');
    inputElement.closest('.form-field').classList.remove('campo-validado');
  }
};

// Validação de senha forte e comparação de confirmação
const senhaInput = document.getElementById('senha');
const confirmarSenhaInput = document.getElementById('confirmar_senha');
const regrasSenha = document.getElementById('regrasSenha');
const msgSenha = document.getElementById('mensagemSenha');

function validarSenhaForte(senha) {
  let regras = 0;
  if (senha.length >= 5) regras++;
  if (/[A-Z]/.test(senha)) regras++;
  if (/[a-z]/.test(senha)) regras++;
  if (/[0-9]/.test(senha)) regras++;
  if (/[^A-Za-z0-9]/.test(senha)) regras++;
  return regras === 5;
}

if (senhaInput && regrasSenha) {
  senhaInput.addEventListener('input', function () {
    const val = senhaInput.value;
    let todas = 0;
    if (val.length >= 5) { document.getElementById('regra1').classList.add('regra-ok'); todas++; }
    else document.getElementById('regra1').classList.remove('regra-ok');
    if (/[A-Z]/.test(val)) { document.getElementById('regra2').classList.add('regra-ok'); todas++; }
    else document.getElementById('regra2').classList.remove('regra-ok');
    if (/[a-z]/.test(val)) { document.getElementById('regra3').classList.add('regra-ok'); todas++; }
    else document.getElementById('regra3').classList.remove('regra-ok');
    if (/[0-9]/.test(val)) { document.getElementById('regra4').classList.add('regra-ok'); todas++; }
    else document.getElementById('regra4').classList.remove('regra-ok');
    if (/[^A-Za-z0-9]/.test(val)) { document.getElementById('regra5').classList.add('regra-ok'); todas++; }
    else document.getElementById('regra5').classList.remove('regra-ok');
    if (todas === 5) regrasSenha.classList.add('regra-ok');
    else regrasSenha.classList.remove('regra-ok');
  });
}

if (senhaInput && confirmarSenhaInput && msgSenha) {
  confirmarSenhaInput.addEventListener('input', function () {
    if (confirmarSenhaInput.value && confirmarSenhaInput.value !== senhaInput.value) {
      msgSenha.textContent = 'As senhas não combinam';
      msgSenha.className = 'senha-msg senha-erro';
    } else if (confirmarSenhaInput.value && confirmarSenhaInput.value === senhaInput.value) {
      msgSenha.textContent = 'As senhas combinam';
      msgSenha.className = 'senha-msg senha-sucesso';
    } else {
      msgSenha.textContent = '';
      msgSenha.className = 'senha-msg';
    }
  });
}

// Corrige feedback visual do tipo de usuário: quadradinho verde no campo, check/asterisco corretos
const tipoUsuario = document.getElementById('tipo_usuario');
if (tipoUsuario) {
  tipoUsuario.addEventListener('change', function () {
    const formField = tipoUsuario.closest('.form-field');
    if (formField) {
      if (tipoUsuario.value) {
        formField.classList.add('campo-validado');
      } else {
        formField.classList.remove('campo-validado');
      }
    }
  });
  tipoUsuario.dispatchEvent(new Event('change'));
}

// Ativa botões de visualizar senha
function toggleSenha(idCampo) {
  const campo = document.getElementById(idCampo);
  if (!campo) return;
  if (campo.type === 'password') {
    campo.type = 'text';
  } else {
    campo.type = 'password';
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.form-field input[required], .form-field select[required]').forEach(el => {
    el.addEventListener('input', window.checarTodosCamposValidos);
    el.addEventListener('blur', window.checarTodosCamposValidos);
  });
  window.checarTodosCamposValidos();
});

// ENVIO DO FORMULÁRIO VIA FETCH (Usuário)
const form = document.querySelector('form');
if (form) {
  form.addEventListener('submit', async function(event) {
    const btn = form.querySelector('button[type="submit"]');
    const sucessoBox = document.getElementById('sucessoBox');
    const erroBox = document.getElementById('erroBox');
    const okBtnContainer = document.getElementById('okBtnContainer');
    if (sucessoBox) sucessoBox.style.display = 'none';
    if (erroBox) erroBox.style.display = 'none';
    if (okBtnContainer) okBtnContainer.style.display = 'none';
    // Se já existe um fetch, não faz nada
    if (btn && btn.disabled) return;
    btn.disabled = true;
    event.preventDefault();
    const formData = new FormData(form);
    const dados = {};
    formData.forEach((v, k) => dados[k] = v);
    try {
      const resp = await fetch('/usuario/cadastrar-usuario', {
        method: 'POST',
        body: new URLSearchParams(dados)
      });
      if (resp.ok) {
        if (sucessoBox) {
          sucessoBox.textContent = 'Cadastro realizado com sucesso!';
          sucessoBox.style.display = 'block';
        }
        form.reset();
        document.querySelectorAll('.campo-validado').forEach(e => e.classList.remove('campo-validado'));
      } else {
        const data = await resp.text();
        if (erroBox) {
          erroBox.textContent = data || 'Erro ao cadastrar.';
          erroBox.style.display = 'block';
        }
      }
    } catch (e) {
      if (erroBox) {
        erroBox.textContent = 'Erro de conexão.';
        erroBox.style.display = 'block';
      }
    }
    if (okBtnContainer) okBtnContainer.style.display = 'block';
    btn.disabled = false;
  });
  // Botão OK recarrega a página
  const okBtn = document.getElementById('okBtn');
  if (okBtn) {
    okBtn.addEventListener('click', function() {
      window.location.reload();
    });
  }
}
