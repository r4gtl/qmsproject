// frontend/src/utils/numberFormat.ts
// Utility per formattare numeri in stile italiano (migliaia + virgola).
// Pensata per DISPLAY (tabelle, badge), non per input controllati.

export type Decimals = 0 | 2 | 3;

const nf0 = new Intl.NumberFormat('it-IT', { maximumFractionDigits: 0 });
const nf2 = new Intl.NumberFormat('it-IT', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const nf3 = new Intl.NumberFormat('it-IT', {
  minimumFractionDigits: 3,
  maximumFractionDigits: 3,
});

export function toNumberOrNull(v: unknown): number | null {
  if (v === null || v === undefined || v === '') return null;
  const s = String(v).trim().replace(',', '.');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/**
 * Formatta un valore come numero in formato IT.
 * Ritorna '' se il valore è nullo/invalid.
 */
export function fmtNumber(v: unknown, decimals: Decimals): string {
  const n = toNumberOrNull(v);
  if (n === null) return '';
  if (decimals === 0) return nf0.format(n);
  if (decimals === 2) return nf2.format(n);
  return nf3.format(n);
}

/**
 * Come fmtNumber, ma ritorna un placeholder (es. '-') se nullo/invalid.
 */
export function fmtNumberOr(
  v: unknown,
  decimals: Decimals,
  placeholder = '-'
): string {
  const out = fmtNumber(v, decimals);
  return out === '' ? placeholder : out;
}
