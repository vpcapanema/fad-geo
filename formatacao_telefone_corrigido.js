// Formatação e validação CORRIGIDA de telefone (aceita fixo e móvel)

// Garante que atualizarValidacaoCampo está definida antes de ser usada
if (typeof window.atualizarValidacaoCampo !== 'function') {
  window.atualizarValidacaoCampo = function() {};
}

console.log("🔧 Script de formatação CORRIGIDO carregado!");

// Formatação e validação dinâmica de telefone pessoal (aceita fixo e móvel)
const telInputPessoal = document.getElementById('telefone');
if (telInputPessoal) {
  console.log("✅ Campo #telefone encontrado!");
  
  const msg = document.createElement('div');
  msg.className = 'msg-validacao-telefone';
  msg.style.display = 'none';
  msg.style.fontSize = '12px';
  msg.style.color = '#dc3545';
  msg.style.marginTop = '2px';
  telInputPessoal.parentNode.appendChild(msg);

  telInputPessoal.addEventListener('input', function (e) {
    console.log("📱 Evento input disparado no telefone pessoal:", e.target.value);
    
    let v = e.target.value.replace(/\D/g, '');
    console.log("🧹 Apenas dígitos:", v);
    
    if (v.length > 11) v = v.slice(0, 11);
    console.log("✂️ Limitado a 11:", v);
    
    let formatado = '';
    
    if (v.length === 11) {
      // Celular: (99) 99999-9999
      formatado = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
      console.log("📱 Formatação CELULAR aplicada:", formatado);
    } else if (v.length === 10) {
      // Fixo: (99) 9999-9999
      formatado = v.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
      console.log("☎️ Formatação FIXO aplicada:", formatado);
    } else if (v.length > 6) {
      // Formatação parcial para 7-9 dígitos
      if (v.length >= 7) {
        formatado = v.replace(/(\d{2})(\d{4})(\d{0,5})/, '($1) $2-$3');
      } else {
        formatado = v.replace(/(\d{2})(\d{0,4})/, '($1) $2');
      }
      console.log("🔄 Formatação PARCIAL aplicada:", formatado);
    } else if (v.length > 2) {
      formatado = v.replace(/(\d{2})(\d{0,4})/, '($1) $2');
      console.log("🔢 Formatação DDD aplicada:", formatado);
    } else {
      formatado = v;
      console.log("🔤 Sem formatação:", formatado);
    }
    
    e.target.value = formatado;
    console.log("💾 Valor aplicado no campo:", formatado);
    
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
    
    console.log("🔍 Teste regex fixo:", regexFixo.test(formatado));
    console.log("🔍 Teste regex móvel:", regexMovel.test(formatado));
    console.log("✅ Resultado validação:", valido);
    
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
} else {
  console.log("❌ Campo #telefone NÃO encontrado!");
}

// Formatação e validação dinâmica de telefone institucional (aceita fixo e móvel)
const telInputInst = document.getElementById('telefone_institucional');
if (telInputInst) {
  console.log("✅ Campo #telefone_institucional encontrado!");
  
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
    console.log("🏢 Evento input disparado no telefone institucional:", e.target.value);
    
    let v = e.target.value.replace(/\D/g, '');
    console.log("🧹 Apenas dígitos:", v);
    
    if (v.length > 11) v = v.slice(0, 11);
    console.log("✂️ Limitado a 11:", v);
    
    let formatado = '';
    
    if (v.length === 11) {
      // Celular: (99) 99999-9999
      formatado = v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
      console.log("📱 Formatação CELULAR aplicada:", formatado);
    } else if (v.length === 10) {
      // Fixo: (99) 9999-9999
      formatado = v.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
      console.log("☎️ Formatação FIXO aplicada:", formatado);
    } else if (v.length > 6) {
      // Formatação parcial para 7-9 dígitos
      if (v.length >= 7) {
        formatado = v.replace(/(\d{2})(\d{4})(\d{0,5})/, '($1) $2-$3');
      } else {
        formatado = v.replace(/(\d{2})(\d{0,4})/, '($1) $2');
      }
      console.log("🔄 Formatação PARCIAL aplicada:", formatado);
    } else if (v.length > 2) {
      formatado = v.replace(/(\d{2})(\d{0,4})/, '($1) $2');
      console.log("🔢 Formatação DDD aplicada:", formatado);
    } else {
      formatado = v;
      console.log("🔤 Sem formatação:", formatado);
    }
    
    e.target.value = formatado;
    console.log("💾 Valor aplicado no campo:", formatado);
    
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
    
    console.log("🔍 Teste regex fixo:", regexFixo.test(formatado));
    console.log("🔍 Teste regex móvel:", regexMovel.test(formatado));
    console.log("✅ Resultado validação:", valido);
    
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
} else {
  console.log("❌ Campo #telefone_institucional NÃO encontrado!");
}
