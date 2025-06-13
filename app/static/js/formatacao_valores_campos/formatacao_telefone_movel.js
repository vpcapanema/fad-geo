// Formatação e validação dinâmica de telefone (aceita fixo e móvel)

// Garante que atualizarValidacaoCampo está definida antes de ser usada
if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}

// Formatação e validação dinâmica de telefone pessoal (aceita fixo e móvel)
const telInputPessoal = document.getElementById('telefone');
if (telInputPessoal) {
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-telefone';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  telInputPessoal.parentNode.appendChild(msg);
  telInputPessoal.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);
    
    let formatado = '';
    if (v.length === 11) {
      // Celular: (99) 99999-9999
      formatado = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (v.length === 10) {
      // Fixo: (99) 9999-9999
      formatado = v.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    } else if (v.length > 6) {
      // Formatação parcial para 7-9 dígitos
      formatado = v.replace(/(\d{2})(\d{4})(\d{0,3})/, '($1) $2-$3');
    } else if (v.length > 2) {
      formatado = v.replace(/(\d{2})(\d{0,4})/, '($1) $2');
    } else {
      formatado = v;
    }
    
    e.target.value = formatado;
    
    if (!v) {
      msg.style.display = 'none';
      telInputPessoal.classList.remove('erro-campo');
      if (typeof window.atualizarValidacaoCampo === 'function') {
        atualizarValidacaoCampo(telInputPessoal, false);
      }
      return;
    }
    
    // Validação: aceita telefone fixo (10 dígitos) ou móvel (11 dígitos)
    const regexFixo = /^\(\d{2}\) \d{4}-\d{4}$/;
    const regexMovel = /^\(\d{2}\) \d{5}-\d{4}$/;
    const valido = regexFixo.test(formatado) || regexMovel.test(formatado);
    
    if (valido) {
      msg.style.display = 'none';
      telInputPessoal.classList.remove('erro-campo');
    } else {
      msg.textContent = 'Telefone inválido. Use (XX) XXXX-XXXX ou (XX) XXXXX-XXXX';
      msg.style.display = 'block';
      telInputPessoal.classList.add('erro-campo');
    }
    
    if (typeof window.atualizarValidacaoCampo === 'function') {
      atualizarValidacaoCampo(telInputPessoal, valido);
    }
  });
  
  telInputPessoal.dispatchEvent(new Event('input'));

  // Garante que só exista UM asterisco e UM check por campo
  const label = telInputPessoal.closest('.form-field').querySelector('label');
  if (label) {
    const obrigatorios = label.querySelectorAll('.obrigatorio-icone');
    const checks = label.querySelectorAll('.check-icone');
    obrigatorios.forEach((el, i) => { if (i > 0) el.remove(); });    checks.forEach((el, i) => { if (i > 0) el.remove(); });
  }
}

// Formatação e validação dinâmica de telefone institucional (aceita fixo e móvel)
const telInputInst = document.getElementById('telefone_institucional');
if (telInputInst) {
  // Busca a div de mensagem já existente no HTML ou cria uma nova
  let msg = document.getElementById('msg-telefone-institucional');
  if (!msg) {
    msg = document.createElement('div');
    msg.id = 'msg-telefone-institucional';
    msg.className = 'msg-validacao-telefone';
    msg.style.display = 'none';
    msg.style.fontSize = '12px';
    msg.style.color = '#dc3545';
    msg.style.marginTop = '2px';
    telInputInst.parentNode.appendChild(msg);
  }
  telInputInst.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);
    
    let formatado = '';
    if (v.length === 11) {
      // Celular: (99) 99999-9999
      formatado = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (v.length === 10) {
      // Fixo: (99) 9999-9999
      formatado = v.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    } else if (v.length > 6) {
      // Formatação parcial para 7-9 dígitos
      formatado = v.replace(/(\d{2})(\d{4})(\d{0,3})/, '($1) $2-$3');
    } else if (v.length > 2) {
      formatado = v.replace(/(\d{2})(\d{0,4})/, '($1) $2');
    } else {
      formatado = v;
    }
    
    e.target.value = formatado;
    
    if (!v) {
      msg.style.display = 'none';
      telInputInst.classList.remove('erro-campo');
      if (typeof window.atualizarValidacaoCampo === 'function') {
        atualizarValidacaoCampo(telInputInst, false);
      }
      return;
    }
    
    // Validação: aceita telefone fixo (10 dígitos) ou móvel (11 dígitos)
    const regexFixo = /^\(\d{2}\) \d{4}-\d{4}$/;
    const regexMovel = /^\(\d{2}\) \d{5}-\d{4}$/;
    const valido = regexFixo.test(formatado) || regexMovel.test(formatado);
    
    if (valido) {
      msg.style.display = 'none';
      telInputInst.classList.remove('erro-campo');
    } else {
      msg.textContent = 'Telefone inválido. Use (XX) XXXX-XXXX ou (XX) XXXXX-XXXX';
      msg.style.display = 'block';
      telInputInst.classList.add('erro-campo');
    }
    
    if (typeof window.atualizarValidacaoCampo === 'function') {
      atualizarValidacaoCampo(telInputInst, valido);
    }
  });
  
  telInputInst.dispatchEvent(new Event('input'));

  // Garante que só exista UM asterisco e UM check por campo
  const label = telInputInst.closest('.form-field').querySelector('label');
  if (label) {
    const obrigatorios = label.querySelectorAll('.obrigatorio-icone');
    const checks = label.querySelectorAll('.check-icone');
    obrigatorios.forEach((el, i) => { if (i > 0) el.remove(); });
    checks.forEach((el, i) => { if (i > 0) el.remove(); });
  }
}

// Removido export para uso direto em <script>
// export function formatarTelefone(valor) { ... }
// export function validarTelefone(valor) { ... }
