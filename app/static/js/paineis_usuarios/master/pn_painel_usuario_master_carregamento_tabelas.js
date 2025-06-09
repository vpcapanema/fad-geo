// Carregamento automático das tabelas do Painel Master FAD
// Este arquivo deve ser incluído no template pn_painel_usuario_master.html

document.addEventListener("DOMContentLoaded", () => {
  // Coordenadores
  fetch("/painel/master/es")
    .then(res => res.json())
    .then(admins => {
      const tabela = document.getElementById("tabela-admins");
      tabela.innerHTML = "";
      ordenarPorId(admins).forEach(u => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
          <td class="grupo-pessoais">${u.id}</td>
          <td class="grupo-pessoais">${u.nome}</td>
          <td class="grupo-pessoais">${formatarCPF(u.cpf)}</td>
          <td class="grupo-pessoais">${u.email}</td>
          <td class="grupo-pessoais">${formatarTelefone(u.telefone)}</td>
          <td class="grupo-pessoais">${u.pessoa_fisica_id || ''}</td>
          <td class="grupo-profissionais">${u.instituicao || ''}</td>
          <td class="grupo-profissionais">${u.tipo_lotacao || ''}</td>
          <td class="grupo-profissionais">${u.email_institucional || ''}</td>
          <td class="grupo-profissionais">${formatarTelefone(u.telefone_institucional)}</td>
          <td class="grupo-profissionais">${u.ramal || ''}</td>
          <td class="grupo-profissionais">${u.sede_hierarquia || ''}</td>
          <td class="grupo-profissionais">${u.sede_coordenadoria || ''}</td>
          <td class="grupo-profissionais">${u.sede_setor || ''}</td>
          <td class="grupo-profissionais">${u.sede_assistencia || ''}</td>
          <td class="grupo-profissionais">${u.regional_nome || ''}</td>
          <td class="grupo-profissionais">${u.regional_coordenadoria || ''}</td>
          <td class="grupo-profissionais">${u.regional_setor || ''}</td>
          <td class="grupo-sistema">${formatarData(u.criado_em)}</td>
          <td class="grupo-sistema">${formatarData(u.aprovado_em)}</td>
          <td class="grupo-sistema">${u.aprovador_id || ''}</td>
          <td class="grupo-sistema"><span class="status-badge ${u.status === 'aprovado' ? 'status-aprovado' : u.status === 'aguardando aprovação' ? 'status-aguardando' : u.status === 'reprovado' ? 'status-reprovado' : ''}"><b>${u.status || ''}</b></span></td>
          <td class="grupo-sistema"><span class="ativo-badge ${u.ativo ? 'ativo-sim' : 'ativo-nao'}"><b>${u.ativo ? 'Sim' : 'Não'}</b></span></td>
          <td class="grupo-sistema" style="display:flex;gap:2px;justify-content:center;align-items:center;">
            <button class="btn-icone grupo-sistema btn-aprovar" title="Aprovar" onclick="aprovarUsuario(${u.id})"><i class="fa-solid fa-circle-check"></i></button>
            <button class="btn-icone grupo-sistema btn-reprovar" title="Reprovar" onclick="reprovarUsuario(${u.id})"><i class="fa-solid fa-circle-xmark"></i></button>
            <button class="btn-icone grupo-sistema btn-ativar" title="Ativar" onclick="ativarUsuario && ativarUsuario(${u.id})"><i class="fa-solid fa-user-check"></i></button>
          </td>
          <td class="grupo-sistema"><button class="btn-icone btn-icone-padrao grupo-sistema" title="Auditoria" onclick="abrirAuditoriaUsuario && abrirAuditoriaUsuario(${u.id})"><i class="fa-solid fa-clock-rotate-left"></i></button></td>
        `;
        tabela.appendChild(linha);
      });
    })
    .catch(() => mostrarMensagem('erro', 'Erro ao carregar coordenadores.'));

  // Usuários comuns
  fetch("/painel/master/usuarios")
    .then(res => res.json())
    .then(usuarios => {
      const tabela = document.getElementById("tabela-usuarios");
      tabela.innerHTML = "";
      ordenarPorId(usuarios).forEach(u => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
          <td class="grupo-pessoais">${u.id}</td>
          <td class="grupo-pessoais">${u.nome}</td>
          <td class="grupo-pessoais">${formatarCPF(u.cpf)}</td>
          <td class="grupo-pessoais">${u.email}</td>
          <td class="grupo-pessoais">${formatarTelefone(u.telefone)}</td>
          <td class="grupo-pessoais">${u.pessoa_fisica_id || ''}</td>
          <td class="grupo-profissionais">${u.instituicao || ''}</td>
          <td class="grupo-profissionais">${u.tipo_lotacao || ''}</td>
          <td class="grupo-profissionais">${u.email_institucional || ''}</td>
          <td class="grupo-profissionais">${formatarTelefone(u.telefone_institucional)}</td>
          <td class="grupo-profissionais">${u.ramal || ''}</td>
          <td class="grupo-profissionais">${u.sede_hierarquia || ''}</td>
          <td class="grupo-profissionais">${u.sede_coordenadoria || ''}</td>
          <td class="grupo-profissionais">${u.sede_setor || ''}</td>
          <td class="grupo-profissionais">${u.sede_assistencia || ''}</td>
          <td class="grupo-profissionais">${u.regional_nome || ''}</td>
          <td class="grupo-profissionais">${u.regional_coordenadoria || ''}</td>
          <td class="grupo-profissionais">${u.regional_setor || ''}</td>
          <td class="grupo-sistema">${formatarData(u.criado_em)}</td>
          <td class="grupo-sistema">${formatarData(u.aprovado_em)}</td>
          <td class="grupo-sistema">${u.aprovador_id || ''}</td>
          <td class="grupo-sistema"><span class="status-badge ${u.status === 'aprovado' ? 'status-aprovado' : u.status === 'aguardando aprovação' ? 'status-aguardando' : u.status === 'reprovado' ? 'status-reprovado' : ''}"><b>${u.status || ''}</b></span></td>
          <td class="grupo-sistema"><span class="ativo-badge ${u.ativo ? 'ativo-sim' : 'ativo-nao'}">${u.ativo ? 'Sim' : 'Não'}</span></td>
          <td class="grupo-sistema" style="display:flex;gap:2px;justify-content:center;align-items:center;">
            <button class="btn-icone grupo-sistema btn-aprovar" title="Aprovar" onclick="aprovarUsuario && aprovarUsuario(${u.id})"><i class="fa-solid fa-circle-check"></i></button>
            <button class="btn-icone grupo-sistema btn-reprovar" title="Reprovar" onclick="reprovarUsuario && reprovarUsuario(${u.id})"><i class="fa-solid fa-circle-xmark"></i></button>
            <button class="btn-icone grupo-sistema btn-ativar" title="Ativar" onclick="ativarUsuario && ativarUsuario(${u.id})"><i class="fa-solid fa-user-check"></i></button>
          </td>
          <td class="grupo-sistema"><button class="btn-icone btn-icone-padrao grupo-sistema" title="Auditoria" onclick="abrirAuditoriaUsuario(${u.id})"><i class="fa-solid fa-clock-rotate-left"></i></button></td>
        `;
        tabela.appendChild(linha);
      });
    })
    .catch(() => mostrarMensagem('erro', 'Erro ao carregar usuários.'));

  // Pessoa Física
  fetch("/cadastro/pfs/json")
    .then(res => res.json())
    .then(pfs => {
      const tabela = document.getElementById("tabela-pessoa-fisica");
      tabela.innerHTML = "";
      ordenarPorId(pfs).forEach(pf => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
          <td>${pf.id}</td>
          <td>${pf.nome}</td>
          <td>${formatarCPF(pf.cpf)}</td>
          <td>${pf.email}</td>
          <td>${formatarTelefone(pf.telefone)}</td>
          <td>${pf.rua || ''}</td>
          <td>${pf.numero || ''}</td>
          <td>${pf.complemento || ''}</td>
          <td>${pf.bairro || ''}</td>
          <td>${pf.cep || ''}</td>
          <td>${pf.cidade || ''}</td>
          <td>${pf.uf || ''}</td>
          <td>${formatarData(pf.criado_em)}</td>
          <td>${formatarData(pf.atualizado_em)}</td>
          <td><button class='btn-icone btn-icone-padrao' title='Auditoria' onclick='abrirAuditoriaPF(${pf.id})'><i class='fa-solid fa-clock-rotate-left'></i></button></td>
        `;
        tabela.appendChild(linha);
      });
    })
    .catch(() => mostrarMensagem('erro', 'Erro ao carregar pessoas físicas.'));

  // Pessoa Jurídica
  fetch("/cadastro/pjs/json")
    .then(res => res.json())
    .then(pjs => {
      const tabela = document.getElementById("tabela-pessoa-juridica");
      tabela.innerHTML = "";
      ordenarPorId(pjs).forEach(pj => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
          <td>${pj.id}</td>
          <td>${pj.razao_social}</td>
          <td>${formatarCNPJ(pj.cnpj)}</td>
          <td>${pj.nome_fantasia || ''}</td>
          <td>${pj.email || ''}</td>
          <td>${formatarTelefone(pj.telefone)}</td>
          <td>${formatarTelefone(pj.celular)}</td>
          <td>${pj.rua || ''}</td>
          <td>${pj.numero || ''}</td>
          <td>${pj.complemento || ''}</td>
          <td>${pj.bairro || ''}</td>
          <td>${pj.cep || ''}</td>
          <td>${pj.cidade || ''}</td>
          <td>${pj.uf || ''}</td>
          <td>${formatarData(pj.criado_em)}</td>
          <td>${formatarData(pj.atualizado_em)}</td>
          <td><button class='btn-icone btn-icone-padrao' title='Auditoria' onclick='abrirAuditoriaPJ(${pj.id})'><i class='fa-solid fa-clock-rotate-left'></i></button></td>
        `;
        tabela.appendChild(linha);
      });
    })
    .catch(() => mostrarMensagem('erro', 'Erro ao carregar pessoas jurídicas.'));

  // Projetos
  fetch("/painel/projetos")
    .then(res => res.json())
    .then(projetos => {
      const tabela = document.getElementById("tabela-projetos");
      tabela.innerHTML = "";
      projetos.forEach(p => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
          <td>${p.id || p.Id}</td>
          <td>${p.nome || p.Nome}</td>
          <td>${p.interessado || p.Interessado || ''}</td>
          <td>${formatarCNPJ(p.cnpj || p.CNPJ || '')}</td>
          <td>${p.representante_legal || p['Representante legal'] || ''}</td>
          <td>${formatarCPF(p.cpf || p.CPF || '')}</td>
          <td>${p.email || p['E-mail'] || ''}</td>
          <td>${formatarTelefone(p.telefone || p.Telefone || '')}</td>
          <td>${p.trecho || p.Trecho || ''}</td>
          <td>${p.municipio_uf || p['Município/UF'] || ''}</td>
          <td>${p.extensao || p['Extensão'] || ''}</td>
          <td>${p.extensao_calculada || p['Extensão calculada'] || ''}</td>
          <td>${p.analista_responsavel || p['Analista responsável'] || ''}</td>
          <td>${formatarData(p.criado_em || p['Criado em'] || '')}</td>
          <td>${p.situacao_projeto || p['Situação do projeto'] || ''}</td>
          <td>${p.situacao_upload || p['Situação do upload'] || ''}</td>
          <td>${p.situacao_geometria || p['Situação da geometria'] || ''}</td>
          <td>${formatarData(p.validada_em || p['Validada em'] || '')}</td>
          <td>${p.situacao_ca || p['Situação da CA'] || ''}</td>
          <td>${formatarData(p.ca_aprovada_em || p['CA aprovada em'] || '')}</td>
          <td>${p.situacao_ifm || p['Situação do IFM'] || ''}</td>
          <td>${p.ifm_trecho || p['IFM trecho'] || ''}</td>
          <td>${formatarData(p.ifm_aprovado_em || p['IFM aprovado em'] || '')}</td>
          <td>${p.situacao_ifs || p['Situação do IFS'] || ''}</td>
          <td>${p.ifs_trecho || p['IFS trecho'] || ''}</td>
          <td>${formatarData(p.ifs_aprovado_em || p['IFS aprovado em'] || '')}</td>
          <td>${p.situacao_iqi || p['Situação do IQI'] || ''}</td>
          <td>${p.iqi_trecho || p['IQI trecho'] || ''}</td>
          <td>${formatarData(p.iqi_aprovado_em || p['IQI aprovado em'] || '')}</td>
        `;
        tabela.appendChild(linha);
      });
    })
    .catch(() => mostrarMensagem('erro', 'Erro ao carregar projetos.'));
});

// Funções utilitárias para formatação
function formatarCPF(cpf) {
  if (!cpf) return '';
  cpf = cpf.replace(/\D/g, '');
  return cpf.length === 11 ? cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4') : cpf;
}
function formatarCNPJ(cnpj) {
  if (!cnpj) return '';
  cnpj = cnpj.replace(/\D/g, '');
  return cnpj.length === 14 ? cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5') : cnpj;
}
function formatarTelefone(tel) {
  if (!tel) return '';
  tel = tel.replace(/\D/g, '');
  if (tel.length === 11) return tel.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  if (tel.length === 10) return tel.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
  return tel;
}
function formatarData(data) {
  if (!data) return '';
  const d = new Date(data);
  if (isNaN(d)) return data;
  return d.toLocaleDateString('pt-BR');
}

// Função utilitária para ordenar por id
function ordenarPorId(arr) {
  return arr.slice().sort((a, b) => (a.id || a.Id) - (b.id || b.Id));
}
