// Teste automático de feedback visual dos campos obrigatórios do cadastro de usuário FAD
(function(){
  const resultados = [];
  const debug = [];
  const campos = [
    {id: 'cpf', nome: 'CPF', valido: '123.456.789-09', invalido: '123'},
    {id: 'telefone', nome: 'Telefone', valido: '(11) 91234-5678', invalido: '123'},
    {id: 'email', nome: 'E-mail', valido: 'teste@teste.com', invalido: 'teste@'},
    {id: 'email_institucional', nome: 'E-mail Institucional', valido: 'teste@org.gov.br', invalido: 'teste@'},
    {id: 'telefone_institucional', nome: 'Telefone Institucional', valido: '(11) 91234-5678', invalido: '123'},
    {id: 'ramal', nome: 'Ramal', valido: '1234', invalido: '12'}
  ];
  campos.forEach(campo => {
    const input = document.getElementById(campo.id);
    if (!input) { resultados.push(`${campo.nome}: campo não encontrado!`); debug.push({campo: campo.nome, motivo: 'input não encontrado'}); return; }
    // Teste campo vazio
    input.value = '';
    input.dispatchEvent(new Event('input', {bubbles:true}));
    let asterisco = input.closest('.form-field').querySelector('.obrigatorio-icone');
    let check = input.closest('.form-field').querySelector('.check-icone');
    let erro = input.classList.contains('erro-campo');
    debug.push({campo: campo.nome, etapa: 'vazio', asterisco: asterisco?.style.display, check: check?.style.display, erro});
    if (!(asterisco && asterisco.style.display !== 'none' && !erro && check.style.display === 'none'))
      resultados.push(`${campo.nome}: FALHA no feedback de campo vazio`);
    // Teste campo inválido
    input.value = campo.invalido;
    input.dispatchEvent(new Event('input', {bubbles:true}));
    erro = input.classList.contains('erro-campo');
    asterisco = input.closest('.form-field').querySelector('.obrigatorio-icone');
    check = input.closest('.form-field').querySelector('.check-icone');
    debug.push({campo: campo.nome, etapa: 'inválido', asterisco: asterisco?.style.display, check: check?.style.display, erro});
    if (!(erro && asterisco.style.display !== 'none' && check.style.display === 'none'))
      resultados.push(`${campo.nome}: FALHA no feedback de campo inválido`);
    // Teste campo válido
    input.value = campo.valido;
    input.dispatchEvent(new Event('input', {bubbles:true}));
    erro = input.classList.contains('erro-campo');
    asterisco = input.closest('.form-field').querySelector('.obrigatorio-icone');
    check = input.closest('.form-field').querySelector('.check-icone');
    debug.push({campo: campo.nome, etapa: 'válido', asterisco: asterisco?.style.display, check: check?.style.display, erro});
    if (!(check.style.display !== 'none' && asterisco.style.display === 'none' && !erro))
      resultados.push(`${campo.nome}: FALHA no feedback de campo válido`);
  });
  console.table(debug);
  if (resultados.length === 0) {
    alert('Teste automático FAD: TODOS OS CAMPOS PASSARAM!');
  } else {
    alert('Teste automático FAD:\n' + resultados.join('\n'));
  }
})();
