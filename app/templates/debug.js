// Script de depuração para o painel de usuário master
document.addEventListener("DOMContentLoaded", function() {
  console.log("Script de depuração carregado");
  
  // Verificar se as tabelas existem
  const tabelaUsuarios = document.getElementById("tabela-usuarios");
  const tabelaAdmins = document.getElementById("tabela-admins");
  
  console.log("Tabela de usuários encontrada:", !!tabelaUsuarios);
  console.log("Tabela de admins encontrada:", !!tabelaAdmins);
  
  // Testar a função de renderização
  const usuarioTeste = {
    id: 999,
    nome: "Usuário Teste",
    cpf: "123.456.789-00",
    email: "teste@exemplo.com",
    telefone: "(00) 00000-0000",
    instituicao: "Instituição Teste",
    tipo_lotacao: "Teste",
    email_institucional: "teste.inst@exemplo.com",
    telefone_institucional: "(00) 0000-0000",
    ramal: "1234",
    criado_em: "01/01/2023",
    aprovado_em: "02/01/2023",
    aprovador_id: "1",
    sede_hierarquia: "Sede",
    sede_coordenadoria: "Coordenadoria",
    sede_setor: "Setor",
    sede_assistencia: "Assistência",
    regional_nome: "Regional",
    regional_coordenadoria: "Coord Regional",
    regional_setor: "Setor Regional",
    status: "Ativo",
    ativo: true,
    pessoa_fisica_id: "123"
  };
  
  // Testar chamadas de API
  fetch("/painel/usuarios")
    .then(res => {
      console.log("Status da resposta /painel/usuarios:", res.status);
      return res.json();
    })
    .then(data => {
      console.log("Dados recebidos de /painel/usuarios:", data);
      if (data && data.length > 0) {
        console.log("Primeiro usuário:", data[0]);
      } else {
        console.log("Nenhum usuário retornado");
      }
    })
    .catch(error => console.error("Erro ao buscar usuários:", error));
    
  fetch("/painel/coordenador/usuarios")
    .then(res => {
      console.log("Status da resposta /painel/coordenador/usuarios:", res.status);
      return res.json();
    })
    .then(data => {
      console.log("Dados recebidos de /painel/coordenador/usuarios:", data);
      if (data && data.length > 0) {
        console.log("Primeiro admin:", data[0]);
      } else {
        console.log("Nenhum admin retornado");
      }
    })
    .catch(error => console.error("Erro ao buscar admins:", error));
    
  // Adicionar usuário de teste à tabela
  if (tabelaUsuarios) {
    try {
      const linha = document.createElement("tr");
      linha.innerHTML = `
        <td>999</td>
        <td>Usuário Teste</td>
        <td>123.456.789-00</td>
        <td>teste@exemplo.com</td>
        <td>(00) 00000-0000</td>
        <td>Instituição Teste</td>
        <td>Teste</td>
        <td>teste.inst@exemplo.com</td>
        <td>(00) 0000-0000</td>
        <td>1234</td>
        <td>01/01/2023</td>
        <td>02/01/2023</td>
        <td>1</td>
        <td>Sede</td>
        <td>Coordenadoria</td>
        <td>Setor</td>
        <td>Assistência</td>
        <td>Regional</td>
        <td>Coord Regional</td>
        <td>Setor Regional</td>
        <td>Ativo</td>
        <td>Sim</td>
        <td>123</td>
        <td>
          <button class="btn-acao" onclick="alert('Teste')">Teste</button>
        </td>
      `;
      tabelaUsuarios.appendChild(linha);
      console.log("Usuário de teste adicionado com sucesso");
    } catch (error) {
      console.error("Erro ao adicionar usuário de teste:", error);
    }
  }
});