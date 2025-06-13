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

  // Mantém apenas a lógica de listas e seleção de PF
  // Toda a formatação, feedback visual e validação de CPF, telefone e e-mail será feita pelos arquivos JS individuais
});
