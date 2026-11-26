/**
 * Query Normalization Utility Functions
 *
 * For processing user input stock codes or names
 */

/**
 * Normalize query string
 * - Remove leading/trailing spaces
 * - Convert to lowercase
 * - Remove internal extra spaces
 */
export function normalizeQuery(query: string): string {
  return query
    .normalize('NFKC')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, '');
}

/**
 * Check if character is Chinese
 */
export function isChineseChar(char: string): boolean {
  return /[\u4e00-\u9fa5]/.test(char);
}

/**
 * Check if string contains Chinese characters
 */
export function containsChinese(query: string): boolean {
  return Array.from(query).some(isChineseChar);
}

/**
 * Extract market suffix from stock code
 * Example: 600519.SH -> SH, AAPL.US -> US
 */
export function extractMarketSuffix(code: string): string | null {
  const match = code.match(/\.([A-Z]+)$/);
  return match ? match[1] : null;
}

/**
 * Remove market suffix from stock code
 * Example: 600519.SH -> 600519, AAPL.US -> AAPL
 */
export function removeMarketSuffix(code: string): string {
  return code.replace(/\.[A-Z]+$/, '');
}

/**
 * Normalize stock code
 * - Convert to uppercase
 * - Remove spaces
 * - Keep market suffix
 */
export function normalizeStockCode(code: string): string {
  return code.trim().toUpperCase().replace(/\s+/g, '');
}

/**
 * Check if query looks like a stock code
 * By detecting if it contains numbers or letter combinations
 */
export function isStockCodeLike(query: string): boolean {
  const normalized = normalizeQuery(query);
  return /^(?:\d{6}(?:\.(?:SH|SZ|SS|BJ))?|(?:SH|SZ|BJ)\d{6})$/i.test(normalized);
}

/**
 * Check if query looks like a stock name
 * By detecting if it contains Chinese
 */
export function isStockNameLike(query: string): boolean {
  return containsChinese(query);
}

/**
 * Check if query looks like pinyin
 * By detecting if it only contains letters and no Chinese
 */
export function isPinyinLike(query: string): boolean {
  const normalized = normalizeQuery(query);
  return /^[a-z]+$/.test(normalized) && !containsChinese(query);
}
