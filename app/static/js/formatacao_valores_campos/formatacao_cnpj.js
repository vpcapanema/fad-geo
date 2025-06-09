// formatacao_cnpj.js como módulo ES6
export function formatarCNPJ(valor) {
  let v = valor.replace(/\D/g, '');
  if (v.length > 14) v = v.slice(0, 14);
  if (v.length > 12) v = v.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{0,2})/, '$1.$2.$3/$4-$5');
  else if (v.length > 8) v = v.replace(/(\d{2})(\d{3})(\d{3})(\d{0,4})/, '$1.$2.$3/$4');
  else if (v.length > 5) v = v.replace(/(\d{2})(\d{3})(\d{0,3})/, '$1.$2.$3');
  else if (v.length > 2) v = v.replace(/(\d{2})(\d{0,3})/, '$1.$2');
  return v;
}
export function validarCNPJ(valor) {
  return /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/.test(valor);
}
