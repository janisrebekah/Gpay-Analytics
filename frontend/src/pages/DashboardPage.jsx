import { useState, useEffect } from 'react';
import {
  Activity, CheckCircle2, Clock, XCircle, IndianRupee,
} from 'lucide-react';
import StatCard from '../components/StatCard';
import CategoryChart from '../components/CategoryChart';
import MonthlyChart from '../components/MonthlyChart';
import TopMerchants from '../components/TopMerchants';
import InsightsPanel from '../components/InsightsPanel';
import { formatINR } from '../utils/format';
import {
  fetchSummary, fetchCategoryBreakdown,
  fetchMonthlyTrends, fetchTopMerchants,
} from '../api/analytics';

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [categories, setCategories] = useState(null);
  const [trends, setTrends] = useState(null);
  const [merchants, setMerchants] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const [s, c, t, m] = await Promise.all([
          fetchSummary(),
          fetchCategoryBreakdown(),
          fetchMonthlyTrends(),
          fetchTopMerchants(),
        ]);
        setSummary(s);
        setCategories(c.items);
        setTrends(t.items);
        setMerchants(m.items);
      } catch (err) {
        setError(err.message || 'Failed to load analytics');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[70vh]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 border-2 border-primary/20 border-t-primary rounded-full animate-spin" />
          <p className="text-text-dim text-[13px] font-medium">Loading analytics…</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-md mx-auto mt-24 bg-accent-red/[0.04] border border-accent-red/15 rounded-2xl p-8 text-center">
        <XCircle className="w-8 h-8 text-accent-red mx-auto mb-3" />
        <p className="text-accent-red text-[13px]">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-[1360px] mx-auto py-10 px-6 lg:px-10">
      {/* Page header */}
      <div className="mb-10">
        <h1 className="text-[28px] font-extrabold text-text-primary tracking-tight">Dashboard</h1>
        <p className="text-[13px] text-text-dim mt-1.5 font-medium">Your complete spending overview</p>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-10">
        <StatCard
          title="Total Txns"
          value={summary.total_transactions}
          icon={Activity}
          color="text-accent-blue"
        />
        <StatCard
          title="Completed"
          value={summary.completed_transactions}
          icon={CheckCircle2}
          color="text-accent-green"
        />
        <StatCard
          title="Pending"
          value={summary.pending_transactions}
          icon={Clock}
          color="text-accent-amber"
        />
        <StatCard
          title="Failed"
          value={summary.failed_transactions}
          icon={XCircle}
          color="text-accent-red"
        />
        <StatCard
          title="Total Spend"
          value={formatINR(summary.total_completed_spend_excluding_self_transfers)}
          icon={IndianRupee}
          color="text-primary-light"
          subtext="Excluding self transfers"
          highlight
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-5">
        <CategoryChart data={categories} />
        <MonthlyChart data={trends} />
      </div>

      {/* Bottom: merchants + insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <TopMerchants data={merchants} />
        <InsightsPanel />
      </div>
    </div>
  );
}
