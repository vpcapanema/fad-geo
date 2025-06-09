// pn_meus_dados_profissionais.js
// Lógica dinâmica do contêiner de informações profissionais da página Meus Dados

document.addEventListener("DOMContentLoaded", function () {
  // Elementos DOM
  const instituicao = document.getElementById("instituicao");
  const tipoLotacao = document.getElementById("tipo_lotacao");
  const sedeHierarquia = document.getElementById("sede_hierarquia");
  const sedeCoordenadoria = document.getElementById("sede_coordenadoria");
  const sedeSetor = document.getElementById("sede_setor");
  const sedeAssistencia = document.getElementById("sede_assistencia");
  const regionalNome = document.getElementById("regional_nome");
  const regionalCoordenadoria = document.getElementById("regional_coordenadoria");
  const regionalSetor = document.getElementById("regional_setor");

  // Containers
  const tipoLotacaoContainer = document.getElementById("tipo-lotacao-container");
  const sedeHierarquiaContainer = document.getElementById("sede-hierarquia-container");
  const sedeCoordenadoriaContainer = document.getElementById("sede-coordenadoria-container");
  const sedeSetorContainer = document.getElementById("sede-setor-container");
  const sedeAssistenciaContainer = document.getElementById("sede-assistencia-container");
  const regionalNomeContainer = document.getElementById("regional-nome-container");
  const regionalCoordenadoriaContainer = document.getElementById("regional-coordenadoria-container");
  const regionalSetorContainer = document.getElementById("regional-setor-container");

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
        { label: 'Coordenadoria de Benefícios e Pagamentos' },
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

  // --- HIERARQUIA REGIONAL ---
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
  // Criação dinâmica dos selects extras para Sede
  let diretoriaContainer = document.getElementById('sede-diretoria-container');
  if (!diretoriaContainer) {
    diretoriaContainer = document.createElement('div');
    diretoriaContainer.className = 'hidden';
    diretoriaContainer.id = 'sede-diretoria-container';
    diretoriaContainer.innerHTML = '<label for="sede_diretoria">Diretoria:</label><select id="sede_diretoria" name="sede_diretoria"></select>';
    sedeHierarquiaContainer.insertAdjacentElement('afterend', diretoriaContainer);
  }
  const sedeDiretoria = document.getElementById('sede_diretoria');

  let coordGeralContainer = document.getElementById('sede-coordenadoria-geral-container');
  if (!coordGeralContainer) {
    coordGeralContainer = document.createElement('div');
    coordGeralContainer.className = 'hidden';
    coordGeralContainer.id = 'sede-coordenadoria-geral-container';
    coordGeralContainer.innerHTML = '<label for="sede_coordenadoria_geral">Coordenadoria Geral:</label><select id="sede_coordenadoria_geral" name="sede_coordenadoria_geral"></select>';
    diretoriaContainer.insertAdjacentElement('afterend', coordGeralContainer);
  }
  const sedeCoordenadoriaGeral = document.getElementById('sede_coordenadoria_geral');

  // --- Função para popular selects ---
  function popularSelect(select, opcoes) {
    if (!select) return;
    select.innerHTML = '<option value="">Selecione...</option>';
    opcoes.forEach(opt => {
      if (typeof opt === 'string') {
        select.innerHTML += `<option value="${opt}">${opt}</option>`;
      } else {
        select.innerHTML += `<option value="${opt.label}">${opt.label}</option>`;
      }
    });
  }

  // Função para ocultar todos os containers
  function ocultarTodosContainers() {
    [tipoLotacaoContainer, sedeHierarquiaContainer, diretoriaContainer, coordGeralContainer, 
     sedeCoordenadoriaContainer, sedeSetorContainer, sedeAssistenciaContainer,
     regionalNomeContainer, regionalCoordenadoriaContainer, regionalSetorContainer].forEach(container => {
      if (container) container.classList.add('hidden');
    });
  }

  // Inicialização
  popularSelect(sedeHierarquia, hierarquiaSede);
  popularSelect(regionalNome, regionais);
  ocultarTodosContainers();

  // --- Eventos ---
  
  // 1. Instituição
  instituicao.addEventListener("change", function () {
    ocultarTodosContainers();
    if (this.value === "DER/SP") {
      tipoLotacaoContainer.classList.remove("hidden");
    } else {
      tipoLotacaoContainer.classList.add("hidden");
    }
  });

  // 2. Tipo de Lotação
  tipoLotacao.addEventListener("change", function () {
    [sedeHierarquiaContainer, diretoriaContainer, coordGeralContainer, 
     sedeCoordenadoriaContainer, sedeSetorContainer, sedeAssistenciaContainer,
     regionalNomeContainer, regionalCoordenadoriaContainer, regionalSetorContainer].forEach(container => {
      if (container) container.classList.add('hidden');
    });
    
    if (this.value === "sede") {
      sedeHierarquiaContainer.classList.remove("hidden");
    } else if (this.value === "regional") {
      regionalNomeContainer.classList.remove("hidden");
    }
  });

  // 3. Hierarquia Sede
  sedeHierarquia.addEventListener('change', function() {
    [diretoriaContainer, coordGeralContainer, sedeCoordenadoriaContainer, 
     sedeSetorContainer, sedeAssistenciaContainer].forEach(container => {
      if (container) container.classList.add('hidden');
    });
    
    const opt = hierarquiaSede.find(h => h.label === this.value);
    if (this.value === 'Diretorias') {
      diretoriaContainer.classList.remove('hidden');
      popularSelect(sedeDiretoria, diretorias);
    } else if (opt && opt.children) {
      sedeSetorContainer.classList.remove('hidden');
      popularSelect(sedeSetor, opt.children);
    }
  });

  // 4. Diretoria (Sede)
  if (sedeDiretoria) {
    sedeDiretoria.addEventListener('change', function() {
      [coordGeralContainer, sedeCoordenadoriaContainer, sedeSetorContainer, sedeAssistenciaContainer].forEach(container => {
        if (container) container.classList.add('hidden');
      });
      
      const dir = diretorias.find(d => d.label === this.value);
      if (dir && dir.children) {
        coordGeralContainer.classList.remove('hidden');
        popularSelect(sedeCoordenadoriaGeral, dir.children);
      }
    });
  }

  // 5. Coordenadoria Geral (Sede)
  if (sedeCoordenadoriaGeral) {
    sedeCoordenadoriaGeral.addEventListener('change', function() {
      [sedeCoordenadoriaContainer, sedeSetorContainer, sedeAssistenciaContainer].forEach(container => {
        if (container) container.classList.add('hidden');
      });
      
      const dir = diretorias.find(d => d.label === sedeDiretoria.value);
      const coordGeral = dir ? dir.children.find(cg => cg.label === this.value) : null;
      if (coordGeral && coordGeral.children) {
        sedeCoordenadoriaContainer.classList.remove('hidden');
        popularSelect(sedeCoordenadoria, coordGeral.children);
      }
    });
  }

  // 6. Coordenadoria (Sede)
  sedeCoordenadoria.addEventListener('change', function() {
    [sedeSetorContainer, sedeAssistenciaContainer].forEach(container => {
      if (container) container.classList.add('hidden');
    });
    
    let opt = null;
    if (!diretoriaContainer.classList.contains('hidden')) {
      const dir = diretorias.find(d => d.label === sedeDiretoria.value);
      const coordGeral = dir ? dir.children.find(cg => cg.label === sedeCoordenadoriaGeral.value) : null;
      opt = coordGeral && coordGeral.children ? coordGeral.children.find(s => s.label === this.value) : null;
    } else {
      const hier = hierarquiaSede.find(h => h.label === sedeHierarquia.value);
      opt = hier && hier.children ? hier.children.find(s => s.label === this.value) : null;
    }
    if (opt && opt.children) {
      sedeSetorContainer.classList.remove('hidden');
      popularSelect(sedeSetor, opt.children);
    }
  });

  // 7. Setor (Sede)
  sedeSetor.addEventListener('change', function() {
    sedeAssistenciaContainer.classList.add('hidden');
    
    let opt = null;
    if (!diretoriaContainer.classList.contains('hidden')) {
      const dir = diretorias.find(d => d.label === sedeDiretoria.value);
      const coordGeral = dir ? dir.children.find(cg => cg.label === sedeCoordenadoriaGeral.value) : null;
      opt = coordGeral && coordGeral.children ? coordGeral.children.find(s => s.label === sedeCoordenadoria.value) : null;
    } else {
      const hier = hierarquiaSede.find(h => h.label === sedeHierarquia.value);
      opt = hier && hier.children ? hier.children.find(s => s.label === this.value) : null;
    }
    if (opt && opt.children) {
      sedeAssistenciaContainer.classList.remove('hidden');
      popularSelect(sedeAssistencia, opt.children);
    }
  });

  // 8. Regional Nome
  regionalNome.addEventListener('change', function() {
    [regionalCoordenadoriaContainer, regionalSetorContainer].forEach(container => {
      if (container) container.classList.add('hidden');
    });
    
    if (this.value) {
      regionalCoordenadoriaContainer.classList.remove('hidden');
      popularSelect(regionalCoordenadoria, regionalCoordenadorias);
    }
  });

  // 9. Regional Coordenadoria
  regionalCoordenadoria.addEventListener('change', function() {
    regionalSetorContainer.classList.add('hidden');
    
    const servicos = regionalServicos[this.value] || [];
    if (servicos.length) {
      regionalSetorContainer.classList.remove('hidden');
      popularSelect(regionalSetor, servicos);
    }
  });

  // Inicialização: se já houver valores, exibe os campos corretos
  if (instituicao.value === "DER/SP") {
    tipoLotacaoContainer.classList.remove("hidden");
    if (tipoLotacao.value === "sede") {
      sedeHierarquiaContainer.classList.remove("hidden");
    } else if (tipoLotacao.value === "regional") {
      regionalNomeContainer.classList.remove("hidden");
    }
  }
});
