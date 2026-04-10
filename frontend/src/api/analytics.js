import { get } from './client';

export function fetchSummary() {
  return get('/analytics/summary');
}

export function fetchCategoryBreakdown() {
  return get('/analytics/category-breakdown');
}

export function fetchMonthlyTrends() {
  return get('/analytics/monthly-trends');
}

export function fetchTopMerchants() {
  return get('/analytics/top-merchants');
}
