import { get } from './client';

export function fetchMonthlyInsights() {
  return get('/insights/monthly');
}

export function fetchSavingsInsights() {
  return get('/insights/savings');
}

export function fetchSummaryInsight() {
  return get('/insights/summary');
}
