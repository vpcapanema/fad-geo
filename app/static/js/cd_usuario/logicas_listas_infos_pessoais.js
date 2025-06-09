// Lógica das listas dinâmicas do container de informações pessoais (PF)
document.addEventListener('DOMContentLoaded', function() {
  const opcaoPF = document.getElementById('opcaoPF');
  const boxPF = document.getElementById('boxPF');
  const pfSelect = document.getElementById('pfSelect');
  const confirmarBtn = document.getElementById('confirmarPFBtn');
  const atualizarBtn = document.getElementById('atualizarPFBtn');
  const resumoPF = document.getElementById('resumoPF');
  const pfResumoTexto = document.getElementById('pfResumoTexto');
  const pfInputFinal = document.getElementById('pfInputFinal');
  const pfNomeFinal = document.getElementById('pfNomeFinal');

  if (!opcaoPF) return;

  opcaoPF.addEventListener('change', function () {
    if (this.value === 'associar') {
      boxPF.classList.remove('hidden');
      resumoPF.classList.add('hidden');
    } else if (this.value === 'cadastrar') {
      window.open('/cadastro/interessado/pf', '_blank');
      this.value = '';
      boxPF.classList.add('hidden');
      confirmarBtn.classList.add('hidden');
      resumoPF.classList.add('hidden');
    } else {
      boxPF.classList.add('hidden');
      confirmarBtn.classList.add('hidden');
      resumoPF.classList.add('hidden');
    }
  });

  pfSelect.addEventListener('change', function () {
    confirmarBtn.classList.toggle('hidden', !this.value);
  });

  confirmarBtn.addEventListener('click', function () {
    const selected = pfSelect.options[pfSelect.selectedIndex];
    const nome = selected.getAttribute('data-nome');
    const cpf = selected.getAttribute('data-cpf');
    const email = selected.getAttribute('data-email');
    const telefone = selected.getAttribute('data-telefone');
    pfResumoTexto.value = nome;
    pfInputFinal.value = pfSelect.value;
    pfNomeFinal.value = nome;
    document.getElementById('cpf').value = cpf;
    document.getElementById('email').value = email;
    document.getElementById('telefone').value = telefone;
    boxPF.classList.add('hidden');
    opcaoPF.classList.add('hidden');
    resumoPF.classList.remove('hidden');
  });

  document.getElementById('editarPFBtn').addEventListener('click', function () {
    resumoPF.classList.add('hidden');
    opcaoPF.classList.remove('hidden');
    pfSelect.value = '';
    confirmarBtn.classList.add('hidden');
    document.getElementById('cpf').value = '';
    document.getElementById('email').value = '';
    document.getElementById('telefone').value = '';
  });

  atualizarBtn.addEventListener('click', async function () {
    try {
      const response = await fetch('/cadastro/pfs/json');
      const data = await response.json();
      pfSelect.innerHTML = '<option value="">Selecione uma PF</option>';
      data.forEach(pf => {
        const option = document.createElement('option');
        option.value = pf.id;
        option.textContent = `${pf.nome} (${pf.cpf})`;
        option.setAttribute('data-cpf', pf.cpf);
        option.setAttribute('data-email', pf.email);
        option.setAttribute('data-telefone', pf.telefone);
        option.setAttribute('data-nome', pf.nome);
        pfSelect.appendChild(option);
      });
      confirmarBtn.classList.add('hidden');
    } catch (error) {
      alert('Erro ao atualizar a lista de PFs.');
    }
  });

  // Feedback visual individualizado para Nome Completo (PF)
  const pfLabel = document.querySelector('label[for="opcaoPF"]');
  if (confirmarBtn && pfSelect && pfLabel) {
    confirmarBtn.addEventListener('click', function() {
      const check = pfLabel.querySelector('.check-icone');
      const asterisco = pfLabel.querySelector('.obrigatorio-icone');
      if (pfSelect.value) {
        if (asterisco) asterisco.style.display = 'none';
        if (check) check.style.display = 'inline';
        pfLabel.classList.add('campo-validado');
      } else {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        pfLabel.classList.remove('campo-validado');
      }
    });
  }

  // CPF: máscara fixa, validação e feedback visual
  const cpfInput = document.getElementById('cpf');
  const cpfLabel = document.querySelector('label[for="cpf"]');
  if (cpfInput && cpfLabel) {
    cpfInput.placeholder = '___.___.___-__';
    cpfInput.addEventListener('focus', function() {
      if (!cpfInput.value) cpfInput.value = '___.___.___-__';
      setTimeout(() => { cpfInput.setSelectionRange(0, 0); }, 0);
    });
    cpfInput.addEventListener('blur', function() {
      if (cpfInput.value === '___.___.___-__') cpfInput.value = '';
    });
    cpfInput.addEventListener('input', function (e) {
      let v = e.target.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      let formatado = '___.___.___-__';
      for (let i = 0, j = 0; i < formatado.length && j < v.length; i++) {
        if (formatado[i] === '.' || formatado[i] === '-') continue;
        formatado = formatado.substring(0, i) + v[j] + formatado.substring(i + 1);
        j++;
      }
      e.target.value = formatado;
      const completo = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(formatado);
      const check = cpfLabel.querySelector('.check-icone');
      const asterisco = cpfLabel.querySelector('.obrigatorio-icone');
      if (!v) {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        cpfInput.classList.remove('erro-campo');
        cpfLabel.classList.remove('campo-validado');
        return;
      }
      if (completo) {
        if (asterisco) asterisco.style.display = 'none';
        if (check) check.style.display = 'inline';
        cpfInput.classList.remove('erro-campo');
        cpfLabel.classList.add('campo-validado');
      } else {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        cpfInput.classList.add('erro-campo');
        cpfLabel.classList.remove('campo-validado');
      }
    });
    cpfInput.dispatchEvent(new Event('input'));
  }

  // Telefone: máscara, validação e feedback visual
  const telInput = document.getElementById('telefone');
  const telLabel = document.querySelector('label[for="telefone"]');
  if (telInput && telLabel) {
    telInput.placeholder = '(__) _____-____';
    telInput.addEventListener('input', function (e) {
      let v = e.target.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      if (v.length > 6) v = v.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
      else if (v.length > 2) v = v.replace(/(\d{2})(\d{0,5})/, '($1) $2');
      else v = v.replace(/(\d{0,2})/, '$1');
      e.target.value = v;
      const completo = /^\(\d{2}\) \d{4,5}-\d{4}$/.test(v);
      const check = telLabel.querySelector('.check-icone');
      const asterisco = telLabel.querySelector('.obrigatorio-icone');
      if (!e.target.value.replace(/\D/g, '')) {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        telInput.classList.remove('erro-campo');
        telLabel.classList.remove('campo-validado');
        return;
      }
      if (completo) {
        if (asterisco) asterisco.style.display = 'none';
        if (check) check.style.display = 'inline';
        telInput.classList.remove('erro-campo');
        telLabel.classList.add('campo-validado');
      } else {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        telInput.classList.add('erro-campo');
        telLabel.classList.remove('campo-validado');
      }
    });
    telInput.dispatchEvent(new Event('input'));
  }

  // E-mail: validação e feedback visual
  const emailInput = document.getElementById('email');
  const emailLabel = document.querySelector('label[for="email"]');
  if (emailInput && emailLabel) {
    emailInput.placeholder = 'exemplo@email.com';
    emailInput.addEventListener('input', function (e) {
      const v = e.target.value.trim();
      const valido = /^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$/.test(v);
      const check = emailLabel.querySelector('.check-icone');
      const asterisco = emailLabel.querySelector('.obrigatorio-icone');
      if (!v) {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        emailInput.classList.remove('erro-campo');
        emailLabel.classList.remove('campo-validado');
        return;
      }
      if (valido) {
        if (asterisco) asterisco.style.display = 'none';
        if (check) check.style.display = 'inline';
        emailInput.classList.remove('erro-campo');
        emailLabel.classList.add('campo-validado');
      } else {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        emailInput.classList.add('erro-campo');
        emailLabel.classList.remove('campo-validado');
      }
    });
    emailInput.dispatchEvent(new Event('input'));
  }

  // Função para aplicar máscara e feedback visual automático ao preencher campos vindos do banco
  function aplicarFeedbackAutomatico() {
    // CPF
    if (cpfInput && cpfLabel) {
      let v = cpfInput.value.replace(/\D/g, '');
      if (v.length === 11) {
        cpfInput.value = v.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
      }
      const completo = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(cpfInput.value);
      const check = cpfLabel.querySelector('.check-icone');
      const asterisco = cpfLabel.querySelector('.obrigatorio-icone');
      if (completo) {
        if (asterisco) asterisco.style.display = 'none';
        if (check) check.style.display = 'inline';
        cpfInput.classList.remove('erro-campo');
        cpfLabel.classList.add('campo-validado');
      } else {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        cpfInput.classList.add('erro-campo');
        cpfLabel.classList.remove('campo-validado');
      }
    }
    // Telefone
    if (telInput && telLabel) {
      let v = telInput.value.replace(/\D/g, '');
      if (v.length === 11) {
        telInput.value = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
      } else if (v.length === 10) {
        telInput.value = v.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
      }
      const completo = /^\(\d{2}\) \d{4,5}-\d{4}$/.test(telInput.value);
      const check = telLabel.querySelector('.check-icone');
      const asterisco = telLabel.querySelector('.obrigatorio-icone');
      if (completo) {
        if (asterisco) asterisco.style.display = 'none';
        if (check) check.style.display = 'inline';
        telInput.classList.remove('erro-campo');
        telLabel.classList.add('campo-validado');
      } else {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        telInput.classList.add('erro-campo');
        telLabel.classList.remove('campo-validado');
      }
    }
    // E-mail
    if (emailInput && emailLabel) {
      const v = emailInput.value.trim();
      const valido = /^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$/.test(v);
      const check = emailLabel.querySelector('.check-icone');
      const asterisco = emailLabel.querySelector('.obrigatorio-icone');
      if (valido) {
        if (asterisco) asterisco.style.display = 'none';
        if (check) check.style.display = 'inline';
        emailInput.classList.remove('erro-campo');
        emailLabel.classList.add('campo-validado');
      } else {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        emailInput.classList.add('erro-campo');
        emailLabel.classList.remove('campo-validado');
      }
    }
  }

  // Chama feedback automático ao preencher campos vindos do banco
  if (window.preenchendoCamposBanco) aplicarFeedbackAutomatico();
});
