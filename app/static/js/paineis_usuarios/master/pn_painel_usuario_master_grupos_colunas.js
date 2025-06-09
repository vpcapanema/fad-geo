// JS para alternar visibilidade de grupos de colunas/cabeçalhos no Painel Master FAD
// Para ser incluído em pn_painel_usuario_master.html

function alternarGrupoUsuarios(tipo, grupo) {
  // tipo: 'admin' ou 'usuarios'
  // grupo: 'profissionais' ou 'sistema'
  const tabela = document.getElementById(tipo === 'admin' ? 'tabela-admins' : 'tabela-usuarios');
  if (!tabela) return;
  // Índices dos grupos (ajustar conforme a ordem real das colunas)
  // Linha 1 do thead: 0-pessoais, 1-profissionais, 2-sistema
  // Linha 2 do thead: colunas detalhadas
  const grupoMap = {
    profissionais: { thIdx: 1, colunas: [6,7,8,9,10,11,12,13,14,15,16,17] },
    sistema: { thIdx: 2, colunas: [18,19,20,21,22,23,24] }
  };
  const grupoInfo = grupoMap[grupo];
  if (!grupoInfo) return;
  const colunas = grupoInfo.colunas;
  const thead = tabela.closest('.tabela-scroll').querySelector('thead');
  // Descobrir se está oculto
  const mostrar = thead.rows[1].cells[colunas[0]].style.display === 'none';
  // Alternar cabeçalhos detalhados
  for (let i = 1; i < thead.rows.length; i++) {
    colunas.forEach(idx => {
      if (thead.rows[i].cells[idx])
        thead.rows[i].cells[idx].style.display = mostrar ? '' : 'none';
    });
  }
  // Alternar colunas das linhas
  for (let i = 0; i < tabela.rows.length; i++) {
    colunas.forEach(idx => {
      if (tabela.rows[i].cells[idx])
        tabela.rows[i].cells[idx].style.display = mostrar ? '' : 'none';
    });
  }
  // Alternar cabeçalho de grupo (linha 0 do thead)
  const thGrupo = thead.rows[0].children[grupoInfo.thIdx];
  if (thGrupo) thGrupo.style.display = mostrar ? '' : 'none';
}

function alternarGrupoProjetos(grupo) {
  // grupos: 'geometria', 'ca', 'ifm', 'ifs', 'iqi'
  // Linha 1 do thead: 0-geral, 1-geometria, 2-ca, 3-ifm, 4-ifs, 5-iqi
  // Linha 2 do thead: colunas detalhadas
  const grupoMap = {
    geometria: { thIdx: 1, colunas: [15,16,17] },
    ca: { thIdx: 2, colunas: [18,19] },
    ifm: { thIdx: 3, colunas: [20,21,22] },
    ifs: { thIdx: 4, colunas: [23,24,25] },
    iqi: { thIdx: 5, colunas: [26,27,28] }
  };
  const tabela = document.getElementById('tabela-projetos');
  if (!tabela) return;
  const grupoInfo = grupoMap[grupo];
  if (!grupoInfo) return;
  const colunas = grupoInfo.colunas;
  const thead = tabela.closest('.tabela-scroll').querySelector('thead');
  const mostrar = thead.rows[1].cells[colunas[0]].style.display === 'none';
  // Alternar cabeçalhos detalhados
  for (let i = 1; i < thead.rows.length; i++) {
    colunas.forEach(idx => {
      if (thead.rows[i].cells[idx])
        thead.rows[i].cells[idx].style.display = mostrar ? '' : 'none';
    });
  }
  // Alternar colunas das linhas
  for (let i = 0; i < tabela.rows.length; i++) {
    colunas.forEach(idx => {
      if (tabela.rows[i].cells[idx])
        tabela.rows[i].cells[idx].style.display = mostrar ? '' : 'none';
    });
  }
  // Alternar cabeçalho de grupo (linha 0 do thead)
  const thGrupo = thead.rows[0].children[grupoInfo.thIdx];
  if (thGrupo) thGrupo.style.display = mostrar ? '' : 'none';
}

function mostrarTudo(tipo) {
  // tipo: 'admin', 'usuarios', 'projetos'
  let tabela, thead;
  if (tipo === 'admin') tabela = document.getElementById('tabela-admins');
  else if (tipo === 'usuarios') tabela = document.getElementById('tabela-usuarios');
  else if (tipo === 'projetos') tabela = document.getElementById('tabela-projetos');
  if (!tabela) return;
  thead = tabela.closest('.tabela-scroll').querySelector('thead');
  for (let i = 0; i < thead.rows.length; i++) {
    for (let j = 0; j < thead.rows[i].cells.length; j++) {
      thead.rows[i].cells[j].style.display = '';
    }
  }
  for (let i = 0; i < tabela.rows.length; i++) {
    for (let j = 0; j < tabela.rows[i].cells.length; j++) {
      tabela.rows[i].cells[j].style.display = '';
    }
  }
}

function ocultarTudo(tipo) {
  // tipo: 'admin', 'usuarios', 'projetos'
  let tabela, thead;
  if (tipo === 'admin') tabela = document.getElementById('tabela-admins');
  else if (tipo === 'usuarios') tabela = document.getElementById('tabela-usuarios');
  else if (tipo === 'projetos') tabela = document.getElementById('tabela-projetos');
  if (!tabela) return;
  thead = tabela.closest('.tabela-scroll').querySelector('thead');
  // Para admin/usuarios: ocultar tudo após Pessoa Física ID (índice 5)
  // Para projetos: grupos a partir da 15
  let start, end;
  if (tipo === 'projetos') {
    start = 15;
    end = thead.rows[1].cells.length;
  } else {
    start = 6; // Oculta tudo após Pessoa Física ID (índice 5)
    end = thead.rows[1].cells.length;
  }
  // Oculta todos os cabeçalhos de grupo (linha 0), exceto o primeiro
  for (let j = 1; j < thead.rows[0].cells.length; j++) {
    thead.rows[0].cells[j].style.display = 'none';
  }
  // Oculta cabeçalhos detalhados (linha 1)
  for (let j = start; j < end; j++) {
    thead.rows[1].cells[j].style.display = 'none';
  }
  // Oculta colunas das linhas
  for (let i = 0; i < tabela.rows.length; i++) {
    for (let j = start; j < end; j++) {
      if (tabela.rows[i].cells[j])
        tabela.rows[i].cells[j].style.display = 'none';
    }
  }
}

function alternarGrupo(tipo, grupo) {
  // Compatível com botões antigos
  if (tipo === 'usuarios' || tipo === 'admin') alternarGrupoUsuarios(tipo, grupo);
  else if (tipo === 'projetos') alternarGrupoProjetos(grupo);
}

// Botão "Mostrar Tudo" dos projetos
window.mostrarTudo = mostrarTudo;
window.ocultarTudo = ocultarTudo;
window.alternarGrupoUsuarios = alternarGrupoUsuarios;
window.alternarGrupoProjetos = alternarGrupoProjetos;
window.alternarGrupo = alternarGrupo;
