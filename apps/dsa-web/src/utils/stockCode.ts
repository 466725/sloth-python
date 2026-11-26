/**
 * Normalize stock code by stripping exchange prefixes/suffixes.
 *
 * Mirrors the behavior of data_provider.base.normalize_stock_code in the backend.
 *
 *   600519      → 600519     SH600519    → 600519
 *   600519.SH   → 600519     SH.600519   → 600519
 *   SZ000001    → 000001     000001.SZ   → 000001
 *   BJ920748    → 920748     920748.BJ   → 920748
 *   AAPL        → AAPL       TSLA        → TSLA
 */
export function normalizeStockCode(stockCode: string): string {
  const code = stockCode.trim();
  const upper = code.toUpperCase();

  // Strip SH/SZ prefix (e.g. SH600519 → 600519)
  if ((upper.startsWith('SH') || upper.startsWith('SZ')) && !upper.startsWith('SH.') && !upper.startsWith('SZ.')) {
    const candidate = code.slice(2);
    if (/^\d{5,6}$/.test(candidate)) {
      return candidate;
    }
  }

  // Strip dotted SH/SZ prefix (e.g. SH.600519 → 600519)
  if (upper.startsWith('SH.') || upper.startsWith('SZ.')) {
    const candidate = code.slice(3);
    if (/^\d{5,6}$/.test(candidate)) {
      return candidate;
    }
  }

  // Strip BJ prefix (e.g. BJ920748 → 920748)
  if (upper.startsWith('BJ') && !upper.startsWith('BJ.')) {
    const candidate = code.slice(2);
    if (/^\d{6}$/.test(candidate)) {
      return candidate;
    }
  }

  // Strip dotted BJ prefix (e.g. BJ.920748 → 920748)
  if (upper.startsWith('BJ.')) {
    const candidate = code.slice(3);
    if (/^\d{6}$/.test(candidate)) {
      return candidate;
    }
  }

  // Strip supported A-share exchange suffixes.
  if (code.includes('.')) {
    const dotIndex = code.lastIndexOf('.');
    const base = code.slice(0, dotIndex);
    const suffix = code.slice(dotIndex + 1).toUpperCase();

    // 600519.SH → 600519
    if ((suffix === 'SH' || suffix === 'SS' || suffix === 'SZ' || suffix === 'BJ') && /^\d+$/.test(base)) {
      return base;
    }
  }

  return code;
}

function stockCodeMatchKey(stockCode: string): string {
  return normalizeStockCode(stockCode).toUpperCase();
}

export function areStockCodesEquivalent(left: string, right: string): boolean {
  if (!left.trim() || !right.trim()) return false;
  return stockCodeMatchKey(left) === stockCodeMatchKey(right);
}

export function findMatchingStockCode(codes: string[], stockCode: string): string | undefined {
  if (!stockCode.trim()) return undefined;
  const targetKey = stockCodeMatchKey(stockCode);
  return codes.find((code) => code.trim() && stockCodeMatchKey(code) === targetKey);
}

export function includesStockCode(codes: string[], stockCode: string): boolean {
  return findMatchingStockCode(codes, stockCode) !== undefined;
}
