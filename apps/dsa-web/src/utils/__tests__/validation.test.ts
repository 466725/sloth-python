import { describe, expect, test } from 'vitest';
import {
  isObviouslyInvalidStockQuery,
  looksLikeStockCode,
  validateStockCode,
} from '../validation';

describe('stock code validation', () => {
  test.each(['00700.HK', 'HK00700', '7203.T', '005930.KS', '035720.KQ'])(
    'rejects unsupported market code %s',
    (input) => {
      expect(looksLikeStockCode(input)).toBe(false);
      expect(validateStockCode(input).valid).toBe(false);
      expect(isObviouslyInvalidStockQuery(input)).toBe(true);
    },
  );
});
