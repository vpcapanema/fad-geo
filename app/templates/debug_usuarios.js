// Script para depurar o problema de exibição de usuários
console.log("Script de depuração carregado");

// Função para adicionar usuários de teste diretamente na tabela
function adicionarUsuariosTeste() {
  console.log("Adicionando usuários de teste");
  
  const tabelaUsuarios = document.getElementById("tabela-usuarios");
  const tabelaAdmins = document.getElementById("tabela-admins");
  
  if (!tabelaUsuarios || !tabelaAdmins) {
    console.error("Tabelas não encontradas:", {
      tabelaUsuarios: !!tabelaUsuarios,
      tabelaAdmins: !!tabelaAdmins
    });
    return;
  }
  
  // Usuário de teste
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
  
  // Adicionar linha diretamente sem usar renderLinhaUsuario
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
    <td><button class="btn-acao">Teste</button></td>
  `;
  
  tabelaUsuarios.appendChild(linha.cloneNode(true));
  tabelaAdmins.appendChild(linha.cloneNode(true));
  
  console.log("Usuários de teste adicionados");
}

// Executar quando o DOM estiver carregado
document.addEventListener("DOMContentLoaded", function() {
  console.log("DOM carregado, adicionando usuários de teste");
  setTimeout(adicionarUsuariosTeste, 1000); // Pequeno atraso para garantir que tudo foi carregado
});