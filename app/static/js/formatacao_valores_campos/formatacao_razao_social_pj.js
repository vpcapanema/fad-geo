// formatacao_razao_social_pj.js
// Validação especial para razão social de PJ

export function validarRazaoSocialPJ(valor) {
  if (!valor) return false;
  const upper = valor.toUpperCase();
  // Lista de siglas indicadoras de PJ
  const siglas = [
    'LTDA', 'L.T.D.A', 'L T D A', 'S/A', 'S.A.', 'S A', 'EPP', 'MEI', 'ME', 'EIRELI', 'SS', 'S/S', 'SIMPLES', 'SIMPLES NACIONAL', 'SCP', 'SCL', 'SCS', 'SNC', 'SPE', 'SA', 'S.A', 'S.A.', 'S.A', 'S.A.'
  ];
  return siglas.some(sigla => upper.includes(sigla));
}

export function formatarRazaoSocialPJ(valor) {
  return valor ? valor.toUpperCase() : '';
}
