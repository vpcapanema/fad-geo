// Lógica das listas dinâmicas do container de informações profissionais
// Hierarquia Sede e Regional, selects dinâmicos

// Carrega hierarquia e configurações a partir de JSON
let hierarquiaSede, diretorias, regionais, regionalCoordenadorias, regionalServicos;
function iniciarLogicasProfissionais() {
  function popularSelect(select, opcoes) {
    if (!select) return;
    select.innerHTML = '<option value="">Selecione...</option>';
    opcoes.forEach(opt => {
      if (typeof opt === 'string') select.innerHTML += `<option value="${opt}">${opt}</option>`;
      else select.innerHTML += `<option value="${opt.label}">${opt.label}</option>`;
    });
  }

  // Elementos DOM
  const instituicao = document.getElementById('instituicao');
  const tipoLotacao = document.getElementById('tipo_lotacao');
  const sedeHierarquia = document.getElementById('sede_hierarquia');
  const sedeDiretoria = document.getElementById('sede_diretoria');
  const sedeCoordenadoriaGeral = document.getElementById('sede_coordenadoria_geral');
  const sedeCoordenadoria = document.getElementById('sede_coordenadoria');
  const sedeSetor = document.getElementById('sede_setor');
  const sedeAssistDireta = document.getElementById('sede_assistencia_direta');
  const sedeAssistencia = document.getElementById('sede_assistencia');
  const regionalNome = document.getElementById('regional_nome');
  const regionalCoordenadoria = document.getElementById('regional_coordenadoria');
  const regionalSetor = document.getElementById('regional_setor');

  // Popula iniciais
  popularSelect(sedeHierarquia, hierarquiaSede);
  popularSelect(regionalNome, regionais);

  // Mudança de Instituição
  if (instituicao) instituicao.addEventListener('change', function() {
    const tipoLotacaoContainer = document.getElementById('tipo-lotacao-container');
    if (this.value === 'DER/SP') tipoLotacaoContainer?.classList.remove('hidden');
    else {
      tipoLotacaoContainer?.classList.add('hidden');
      document.getElementById('sede-hierarquia-container')?.classList.add('hidden');
      document.getElementById('regional-nome-container')?.classList.add('hidden');
      tipoLotacao.value = '';
    }
  });

  // Tipo Lotação
  if (tipoLotacao) tipoLotacao.addEventListener('change', function() {
    const sedeContainer = document.getElementById('sede-hierarquia-container');
    const regionalContainer = document.getElementById('regional-nome-container');
    if (this.value === 'sede') {
      sedeContainer?.classList.remove('hidden');
      regionalContainer?.classList.add('hidden');
    } else if (this.value === 'regional') {
      regionalContainer?.classList.remove('hidden');
      sedeContainer?.classList.add('hidden');
    } else {
      sedeContainer?.classList.add('hidden');
      regionalContainer?.classList.add('hidden');
    }
  });

  // Hierarquia Sede
  sedeHierarquia?.addEventListener('change', function() {
    document.getElementById('sede-diretoria-container')?.classList.add('hidden');
    document.getElementById('sede-coordenadoria-geral-container')?.classList.add('hidden');
    document.getElementById('sede-coordenadoria-container')?.classList.add('hidden');
    document.getElementById('sede-assistencia-direta-container')?.classList.add('hidden');
    // Se Diretorias
    if (this.value === 'Diretorias') {
      document.getElementById('sede-diretoria-container')?.classList.remove('hidden');
      popularSelect(sedeDiretoria, diretorias);
    }
    // Se Órgãos de Assistência Direta
    if (this.value === 'Órgãos de Assistência Direta') {
      document.getElementById('sede-assistencia-direta-container')?.classList.remove('hidden');
      const node = hierarquiaSede.find(h => h.label === this.value);
      popularSelect(sedeAssistDireta, (node?.children) || []);
    }
  });

  // Diretoria
  sedeDiretoria?.addEventListener('change', function() {
    document.getElementById('sede-coordenadoria-geral-container')?.classList.add('hidden');
    document.getElementById('sede-coordenadoria-container')?.classList.add('hidden');
    const dir = diretorias.find(d => d.label === this.value);
    if (dir?.children) {
      document.getElementById('sede-coordenadoria-geral-container')?.classList.remove('hidden');
      popularSelect(sedeCoordenadoriaGeral, dir.children);
    }
  });

  // Coordenadoria Geral
  sedeCoordenadoriaGeral?.addEventListener('change', function() {
    document.getElementById('sede-coordenadoria-container')?.classList.add('hidden');
    const dir = diretorias.find(d => d.label === sedeDiretoria.value);
    const cg = dir?.children.find(c => c.label === this.value);
    if (cg?.children) {
      document.getElementById('sede-coordenadoria-container')?.classList.remove('hidden');
      popularSelect(sedeCoordenadoria, cg.children);
    }
  });

  // Coordenadoria
  sedeCoordenadoria?.addEventListener('change', function() {
    document.getElementById('sede-setor-container')?.classList.add('hidden');
    document.getElementById('sede-assistencia-container')?.classList.add('hidden');
    const hier = (document.getElementById('sede-coordenadoria-geral-container')?.classList.contains('hidden'))
      ? hierarquiaSede.find(h => h.label === sedeHierarquia.value)
      : null;
    let opt = hier?.children.find(c => c.label === this.value) ||
      (diretorias.find(d => d.label === sedeDiretoria.value)
        .children.find(cg => cg.label === sedeCoordenadoriaGeral.value)
        .children.find(c => c.label === this.value));
    if (opt?.children) {
      document.getElementById('sede-setor-container')?.classList.remove('hidden');
      popularSelect(sedeSetor, opt.children);
    }
  });

  // Setor
  sedeSetor?.addEventListener('change', function() {
    document.getElementById('sede-assistencia-container')?.classList.add('hidden');
    const hier = hierarquiaSede.find(h => h.label === sedeHierarquia.value);
    let opt = hier?.children.find(s => s.label === this.value) ||
      diretorias.find(d => d.label === sedeDiretoria.value)
        .children.find(cg => cg.label === sedeCoordenadoriaGeral.value)
        .children.find(c => c.label === sedeCoordenadoria.value);
    if (opt?.children) {
      document.getElementById('sede-assistencia-container')?.classList.remove('hidden');
      popularSelect(sedeAssistencia, opt.children);
    }
  });

  // Regional Nome
  regionalNome?.addEventListener('change', function() {
    document.getElementById('regional-coordenadoria-container')?.classList.add('hidden');
    document.getElementById('regional-setor-container')?.classList.add('hidden');
    if (this.value) {
      document.getElementById('regional-coordenadoria-container')?.classList.remove('hidden');
      popularSelect(regionalCoordenadoria, regionalCoordenadorias);
    }
  });

  // Regional Coordenadoria
  regionalCoordenadoria?.addEventListener('change', function() {
    document.getElementById('regional-setor-container')?.classList.add('hidden');
    const serv = regionalServicos[this.value] || [];
    if (serv.length) {
      document.getElementById('regional-setor-container')?.classList.remove('hidden');
      popularSelect(regionalSetor, serv);
    }
  });
  // Validação feedback
  function validarListaProfissional(idSelect) {
    const select = document.getElementById(idSelect);
    if (!select) return;
    const formField = select.closest('.form-field');
    if (!formField) return;
    const label = formField.querySelector('label');
    if (!label) return;
    const check = label.querySelector('.check-icone');
    const astr = label.querySelector('.obrigatorio-icone');
    select.addEventListener('change', function() {
      if (this.value) {
        if (astr) astr.style.display = 'none'; 
        if (check) check.style.display = 'inline'; 
        formField.classList.add('campo-validado');
      } else {
        if (astr) astr.style.display = 'inline'; 
        if (check) check.style.display = 'none'; 
        formField.classList.remove('campo-validado');
      }
    });
    if (select.value) { astr.style.display = 'none'; check.style.display = 'inline'; label.classList.add('campo-validado'); }
  }
  ['instituicao','tipo_lotacao','sede_hierarquia','sede_assistencia_direta','sede_diretoria',
    'sede_coordenadoria_geral','sede_coordenadoria','sede_setor','sede_assistencia',
    'regional_nome','regional_coordenadoria','regional_setor']
    .forEach(validarListaProfissional);
}
// Carrega hierarquia e configurações a partir de JSON após DOM pronto
document.addEventListener('DOMContentLoaded', function() {
  fetch('/static/js/cd_usuario/hierarquia_profissionais.json')
    .then(res => res.json())
    .then(data => {
      hierarquiaSede = data.hierarquiaSede;
      diretorias = data.diretorias;
      regionais = data.regionais;
      regionalCoordenadorias = data.regionalCoordenadorias;
      regionalServicos = data.regionalServicos;
      iniciarLogicasProfissionais();
    })
    .catch(err => console.error('Erro ao carregar hierarquia:', err));
});
