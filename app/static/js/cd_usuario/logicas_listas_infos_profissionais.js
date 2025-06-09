// Lógica das listas dinâmicas do container de informações profissionais
// Hierarquia Sede e Regional, selects dinâmicos

document.addEventListener('DOMContentLoaded', function() {
  // --- HIERARQUIA SEDE ---
  const hierarquiaSede = [
    { label: 'Presidência' },
    { label: 'Vice-Presidência' },
    { label: 'Órgãos de Assistência Direta', children: [
      { label: 'Assessoria de Auditoria' },
      { label: 'Assessoria de Comunicação' },
      { label: 'Assessoria de Correição' },
      { label: 'Assessoria de Gestão da Qualidade' },
      { label: 'Assessoria de Integridade' },
      { label: 'Assessoria de Ouvidoria' },
      { label: 'Gabinete' },
      { label: 'Procuradoria Jurídica' },
    ]},
    { label: 'Consultoria Jurídica' },
    { label: 'Diretorias' }
  ];
  const diretorias = [
    { label: 'Diretoria de Administração', children: [
      { label: 'Coordenadoria Geral de Contabilidade, Finanças e Orçamento', children: [
        { label: 'Coordenadoria de Contabilidade' },
        { label: 'Coordenadoria de Finanças' },
        { label: 'Coordenadoria de Orçamento, Custos e Arrecadação' },
      ]},
      { label: 'Coordenadoria Geral de Gestão Patrimonial, Tecnologia e Serviços', children: [
        { label: 'Coordenadoria de Atividades Gerais' },
        { label: 'Coordenadoria de Patrimônio' },
        { label: 'Coordenadoria de Tecnologia da Informação' },
      ]},
      { label: 'Coordenadoria Geral de Aquisições e Licitações', children: [
        { label: 'Coordenadoria de Aquisições e Licitações de Bens e Serviços' },
        { label: 'Coordenadoria de Licitações e Contratação de Obras e Serviços de Engenharia' },
      ]},
      { label: 'Coordenadoria Geral de Recursos Humanos', children: [
        { label: 'Coordenadoria de Administração de Pessoal, Seleção e Aperfeiçoamento' },
        { label: 'Coordenadoria de Pagamentos' },
      ]},
    ]},
    { label: 'Diretoria de Engenharia', children: [
      { label: 'Coordenadoria Geral de Projetos', children: [
        { label: 'Coordenadoria de Geometria e Sinalização' },
        { label: 'Coordenadoria de Pavimentos' },
        { label: 'Coordenadoria de Drenagem e Geotecnia' },
        { label: 'Coordenadoria de Obras de Arte Especiais' },
      ]},
      { label: 'Coordenadoria Geral de Levantamentos', children: [
        { label: 'Coordenadoria de Estudo de Viabilidade Técnica' },
        { label: 'Coordenadoria de Gestão Técnica' },
      ]},
    ]},
    { label: 'Diretoria de Obras', children: [
      { label: 'Coordenadoria Geral de Obras', children: [
        { label: 'Coordenadoria de Construção' },
        { label: 'Coordenadoria de Restauração' },
      ]},
      { label: 'Coordenadoria Geral de Conservação e Sinalização', children: [
        { label: 'Coordenadoria de Conservação de Rotina' },
        { label: 'Coordenadoria de Sinalização' },
      ]},
    ]},
    { label: 'Diretoria de Operações Viárias', children: [
      { label: 'Coordenadoria Geral de Operação Viária', children: [
        { label: 'Coordenadoria de Operação Viária' },
        { label: 'Coordenadoria de Segurança Viária' },
      ]},
      { label: 'Coordenadoria Geral de Fiscalização', children: [
        { label: 'Coordenadoria de Pátios e Leilões' },
        { label: 'Coordenadoria de Fiscalização, Pedágios e Multas' },
      ]},
    ]},
    { label: 'Diretoria de Planejamento', children: [
      { label: 'Coordenadoria Geral de Planejamento e Pesquisa', children: [
        { label: 'Coordenadoria de Planejamento e Custos' },
        { label: 'Coordenadoria de Estudos e Pesquisas' },
      ]},
      { label: 'Coordenadoria Geral Socioambiental', children: [
        { label: 'Coordenadoria de Meio Ambiente' },
        { label: 'Coordenadoria de Desapropriação, Reassentamento e Faixa de Domínio' },
      ]},
      { label: 'Coordenadoria Geral de Contratos e Convênios', children: [
        { label: 'Coordenadoria de Contratos' },
        { label: 'Coordenadoria de Convênios' },
      ]},
    ]}
  ];
  const regionais = [
    'Coordenadoria Geral Regional de Campinas',
    'Coordenadoria Geral Regional de Ribeirão Preto',
    'Coordenadoria Geral Regional de Bauru',
    'Coordenadoria Geral Regional de Araraquara',
    'Coordenadoria Geral Regional de São José do Rio Preto',
    'Coordenadoria Geral Regional de Presidente Prudente',
    'Coordenadoria Geral Regional de Araçatuba',
    'Coordenadoria Geral Regional de São José dos Campos',
    'Coordenadoria Geral Regional de Itapetininga',
    'Coordenadoria Geral Regional de Registro',
    'Coordenadoria Geral Regional de Santos',
    'Coordenadoria Geral Regional de Sorocaba',
    'Coordenadoria Geral Regional de Barretos',
    'Coordenadoria Geral Regional da Capital'
  ];
  const regionalCoordenadorias = [
    'Coordenadoria Administrativa',
    'Coordenadoria de Conservação e Operações Viárias',
    'Coordenadoria Técnica'
  ];
  const regionalServicos = {
    'Coordenadoria Administrativa': [
      'Serviço de Administração de Pessoal',
      'Serviço de Aquisições e Contratações',
      'Serviço de Finanças',
      'Serviço de Patrimônio, Tecnologia e Atividades Gerais'
    ],
    'Coordenadoria de Conservação e Operações Viárias': [
      'Serviço de Faixa de Domínio, Pedágio, Radar e Balança',
      'Serviço de Unidade Básica de Atendimento (UBA)',
      'Serviço de Conservação de Rotina'
    ],
    'Coordenadoria Técnica': [
      'Serviço de Construção',
      'Serviço de Planejamento e Projetos'
    ]
  };

  function popularSelect(select, opcoes) {
    select.innerHTML = '<option value="">Selecione...</option>';
    opcoes.forEach(opt => {
      if (typeof opt === 'string') {
        select.innerHTML += `<option value="${opt}">${opt}</option>`;
      } else {
        select.innerHTML += `<option value="${opt.label}">${opt.label}</option>`;
      }
    });
  }

  // Elementos DOM
  const instituicao = document.getElementById('instituicao');
  const tipoLotacao = document.getElementById('tipo_lotacao');
  const sedeHierarquia = document.getElementById('sede_hierarquia');
  const sedeCoordenadoria = document.getElementById('sede_coordenadoria');
  const sedeSetor = document.getElementById('sede_setor');
  const sedeAssistencia = document.getElementById('sede_assistencia');
  const regionalNome = document.getElementById('regional_nome');
  const regionalCoordenadoria = document.getElementById('regional_coordenadoria');
  const regionalSetor = document.getElementById('regional_setor');

  // Inicialização
  if (sedeHierarquia) popularSelect(sedeHierarquia, hierarquiaSede);
  if (regionalNome) popularSelect(regionalNome, regionais);

  // Eventos para mostrar/ocultar campos e popular selects
  if (instituicao) {
    instituicao.addEventListener('change', function() {
      const tipoLotacaoContainer = document.getElementById('tipo-lotacao-container');
      if (this.value === 'DER/SP') {
        tipoLotacaoContainer.classList.remove('hidden');
      } else {
        tipoLotacaoContainer.classList.add('hidden');
        document.getElementById('sede-hierarquia-container').classList.add('hidden');
        document.getElementById('regional-nome-container').classList.add('hidden');
        tipoLotacao.value = '';
      }
    });
  }
  if (tipoLotacao) {
    tipoLotacao.addEventListener('change', function() {
      if (this.value === 'sede') {
        document.getElementById('sede-hierarquia-container').classList.remove('hidden');
        document.getElementById('regional-nome-container').classList.add('hidden');
      } else if (this.value === 'regional') {
        document.getElementById('regional-nome-container').classList.remove('hidden');
        document.getElementById('sede-hierarquia-container').classList.add('hidden');
      } else {
        document.getElementById('sede-hierarquia-container').classList.add('hidden');
        document.getElementById('regional-nome-container').classList.add('hidden');
      }
    });
  }

  // Hierarquia Sede
  // Adiciona checagem de existência dos elementos antes de acessar classList
  if (sedeHierarquia) {
    sedeHierarquia.addEventListener('change', function() {
      const diretoriaContainer = document.getElementById('sede-diretoria-container');
      const coordGeralContainer = document.getElementById('sede-coordenadoria-geral-container');
      const coordContainer = document.getElementById('sede-coordenadoria-container');
      if (diretoriaContainer) diretoriaContainer.classList.add('hidden');
      if (coordGeralContainer) coordGeralContainer.classList.add('hidden');
      if (coordContainer) coordContainer.classList.add('hidden');
      if (this.value === 'Diretorias') {
        diretoriaContainer.classList.remove('hidden');
        popularSelect(document.getElementById('sede_diretoria'), diretorias);
      }
    });
  }
  const sedeDiretoria = document.getElementById('sede_diretoria');
  if (sedeDiretoria) {
    sedeDiretoria.addEventListener('change', function() {
      const coordGeralContainer = document.getElementById('sede-coordenadoria-geral-container');
      const coordContainer = document.getElementById('sede-coordenadoria-container');
      if (coordGeralContainer) coordGeralContainer.classList.add('hidden');
      if (coordContainer) coordContainer.classList.add('hidden');
      const dir = diretorias.find(d => d.label === this.value);
      if (dir && dir.children) {
        coordGeralContainer.classList.remove('hidden');
        popularSelect(document.getElementById('sede_coordenadoria_geral'), dir.children);
      }
    });
  }
  const sedeCoordenadoriaGeral = document.getElementById('sede_coordenadoria_geral');
  if (sedeCoordenadoriaGeral) {
    sedeCoordenadoriaGeral.addEventListener('change', function() {
      const coordContainer = document.getElementById('sede-coordenadoria-container');
      if (coordContainer) coordContainer.classList.add('hidden');
      const dir = diretorias.find(d => d.label === document.getElementById('sede_diretoria').value);
      const coordGeral = dir ? dir.children.find(cg => cg.label === this.value) : null;
      if (coordGeral && coordGeral.children) {
        coordContainer.classList.remove('hidden');
        popularSelect(document.getElementById('sede_coordenadoria'), coordGeral.children);
      }
    });
  }
  if (sedeCoordenadoria) {
    sedeCoordenadoria.addEventListener('change', function() {
      document.getElementById('sede-setor-container').classList.add('hidden');
      document.getElementById('sede-assistencia-container').classList.add('hidden');
      let opt = null;
      if (!document.getElementById('sede-diretoria-container').classList.contains('hidden')) {
        const dir = diretorias.find(d => d.label === document.getElementById('sede_diretoria').value);
        const coordGeral = dir ? dir.children.find(cg => cg.label === document.getElementById('sede_coordenadoria_geral').value) : null;
        opt = coordGeral && coordGeral.children ? coordGeral.children.find(s => s.label === this.value) : null;
      } else {
        const hier = hierarquiaSede.find(h => h.label === sedeHierarquia.value);
        opt = hier && hier.children ? hier.children.find(s => s.label === this.value) : null;
      }
      if (opt && opt.children) {
        document.getElementById('sede-setor-container').classList.remove('hidden');
        popularSelect(sedeSetor, opt.children);
      }
    });
  }
  if (sedeSetor) {
    sedeSetor.addEventListener('change', function() {
      document.getElementById('sede-assistencia-container').classList.add('hidden');
      let opt = null;
      if (!document.getElementById('sede-diretoria-container').classList.contains('hidden')) {
        const dir = diretorias.find(d => d.label === document.getElementById('sede_diretoria').value);
        const coordGeral = dir ? dir.children.find(cg => cg.label === document.getElementById('sede_coordenadoria_geral').value) : null;
        opt = coordGeral && coordGeral.children ? coordGeral.children.find(s => s.label === document.getElementById('sede_coordenadoria').value) : null;
      } else {
        const hier = hierarquiaSede.find(h => h.label === sedeHierarquia.value);
        opt = hier && hier.children ? hier.children.find(s => s.label === sedeSetor.value) : null;
      }
      if (opt && opt.children) {
        document.getElementById('sede-assistencia-container').classList.remove('hidden');
        popularSelect(sedeAssistencia, opt.children);
      }
    });
  }
  if (regionalNome) {
    regionalNome.addEventListener('change', function() {
      document.getElementById('regional-coordenadoria-container').classList.add('hidden');
      document.getElementById('regional-setor-container').classList.add('hidden');
      if (this.value) {
        document.getElementById('regional-coordenadoria-container').classList.remove('hidden');
        popularSelect(regionalCoordenadoria, regionalCoordenadorias);
      }
    });
  }
  if (regionalCoordenadoria) {
    regionalCoordenadoria.addEventListener('change', function() {
      document.getElementById('regional-setor-container').classList.add('hidden');
      const servicos = regionalServicos[this.value] || [];
      if (servicos.length) {
        document.getElementById('regional-setor-container').classList.remove('hidden');
        popularSelect(regionalSetor, servicos);
      }
    });
  }

  // Validação simples e feedback visual para listas do container de informações profissionais
  function validarListaProfissional(idSelect) {
    const select = document.getElementById(idSelect);
    if (!select) return;
    const label = select.closest('.form-field').querySelector('label');
    const check = label ? label.querySelector('.check-icone') : null;
    const asterisco = label ? label.querySelector('.obrigatorio-icone') : null;
    select.addEventListener('change', function() {
      if (select.value) {
        if (asterisco) asterisco.style.display = 'none';
        if (check) check.style.display = 'inline';
        label.classList.add('campo-validado');
      } else {
        if (asterisco) asterisco.style.display = 'inline';
        if (check) check.style.display = 'none';
        label.classList.remove('campo-validado');
      }
    });
    // Aplica feedback inicial se já vier preenchido
    if (select.value) {
      if (asterisco) asterisco.style.display = 'none';
      if (check) check.style.display = 'inline';
      label.classList.add('campo-validado');
    }
  }

  // IDs dos selects de listas profissionais (ajuste conforme necessário)
  const listasProfissionais = [
    'instituicao',
    'tipo_lotacao',
    'sede_hierarquia',
    'sede_coordenadoria',
    'sede_setor',
    'sede_assistencia',
    'regional_nome',
    'regional_coordenadoria',
    'regional_setor'
  ];
  listasProfissionais.forEach(validarListaProfissional);
  // Validação simples e feedback visual para listas dinâmicas recém-adicionadas
  ['sede_diretoria', 'sede_coordenadoria_geral', 'sede_coordenadoria'].forEach(validarListaProfissional);
});
