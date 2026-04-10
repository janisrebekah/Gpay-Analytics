import { useState, useEffect } from 'react';
import {
  Zap, TrendingDown, FileText, AlertTriangle,
  Info, Lightbulb, Loader2, ArrowUpRight,
} from 'lucide-react';
import { fetchMonthlyInsights, fetchSavingsInsights, fetchSummaryInsight } from '../api/insights';

const TABS = [
  { id: 'summary', label: 'Overview', icon: FileText },
  { id: 'monthly', label: 'Insights', icon: Zap },
  { id: 'savings', label: 'Savings', icon: TrendingDown },
];

const TYPE_CONFIG = {
  info: { border: 'border-accent-blue/15', bg: 'bg-accent-blue/[0.03]', icon: Info, color: 'text-accent-blue', dot: 'bg-accent-blue' },
  warning: { border: 'border-accent-amber/15', bg: 'bg-accent-amber/[0.03]', icon: AlertTriangle, color: 'text-accent-amber', dot: 'bg-accent-amber' },
  tip: { border: 'border-accent-green/15', bg: 'bg-accent-green/[0.03]', icon: Lightbulb, color: 'text-accent-green', dot: 'bg-accent-green' },
};

const PRIORITY_STYLE = {
  high: { text: 'text-accent-red', bg: 'bg-accent-red/8', border: 'border-accent-red/15' },
  medium: { text: 'text-accent-amber', bg: 'bg-accent-amber/8', border: 'border-accent-amber/15' },
  low: { text: 'text-accent-green', bg: 'bg-accent-green/8', border: 'border-accent-green/15' },
};

export default function InsightsPanel() {
  const [activeTab, setActiveTab] = useState('summary');
  const [data, setData] = useState({});
  const [loading, setLoading] = useState({});
  const [errors, setErrors] = useState({});

  const fetchTab = async (tab) => {
    if (data[tab]) return;
    setLoading((p) => ({ ...p, [tab]: true }));
    setErrors((p) => ({ ...p, [tab]: null }));
    try {
      const fetchers = { summary: fetchSummaryInsight, monthly: fetchMonthlyInsights, savings: fetchSavingsInsights };
      const result = await fetchers[tab]();
      setData((p) => ({ ...p, [tab]: result }));
    } catch (err) {
      setErrors((p) => ({ ...p, [tab]: err.message || 'Failed to load' }));
    } finally {
      setLoading((p) => ({ ...p, [tab]: false }));
    }
  };

  useEffect(() => { fetchTab(activeTab); }, [activeTab]);

  const renderSummary = () => {
    const d = data.summary;
    if (!d) return null;
    return (
      <div className="space-y-5">
        <p className="text-[13px] text-text-secondary leading-[1.7]">{d.summary}</p>
        {d.highlights?.length > 0 && (
          <div className="grid grid-cols-3 gap-2.5">
            {d.highlights.map((h, i) => (
              <div key={i} className="bg-bg-elevated/60 rounded-xl p-3.5 border border-border-subtle hover:border-border transition-colors duration-200">
                <p className="text-[10px] text-text-dim font-semibold uppercase tracking-wider">{h.label}</p>
                <p className="text-[14px] font-bold text-text-primary mt-1">{h.value}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderMonthly = () => {
    const d = data.monthly;
    if (!d?.insights) return null;
    return (
      <div className="space-y-2.5">
        {d.insights.map((insight, i) => {
          const cfg = TYPE_CONFIG[insight.type] || TYPE_CONFIG.info;
          const IconComp = cfg.icon;
          return (
            <div key={i} className={`${cfg.border} ${cfg.bg} border rounded-xl p-4 flex items-start gap-3.5 transition-all duration-200 hover:bg-bg-hover/30`}>
              <div className="w-1 h-full min-h-[40px] rounded-full shrink-0 self-stretch" style={{ backgroundColor: `var(--color-${insight.type === 'tip' ? 'accent-green' : insight.type === 'warning' ? 'accent-amber' : 'accent-blue'})`, opacity: 0.4 }} />
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <IconComp className={`w-3.5 h-3.5 ${cfg.color}`} />
                  <p className="text-[13px] font-bold text-text-primary">{insight.title}</p>
                </div>
                <p className="text-[11px] text-text-muted mt-1.5 leading-relaxed">{insight.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  const renderSavings = () => {
    const d = data.savings;
    if (!d?.recommendations) return null;
    return (
      <div className="space-y-2.5">
        {d.recommendations.map((rec, i) => {
          const ps = PRIORITY_STYLE[rec.priority] || PRIORITY_STYLE.medium;
          return (
            <div key={i} className="border border-border rounded-xl p-4 bg-bg-elevated/30 hover:bg-bg-hover/30 transition-all duration-200 group">
              <div className="flex items-start justify-between gap-3 mb-2">
                <div className="flex items-center gap-2">
                  <ArrowUpRight className="w-3.5 h-3.5 text-primary-light opacity-50 group-hover:opacity-100 transition-opacity" />
                  <p className="text-[13px] font-bold text-text-primary">{rec.title}</p>
                </div>
                <span className={`text-[9px] font-bold uppercase tracking-[0.1em] px-2 py-0.5 rounded-md border ${ps.text} ${ps.bg} ${ps.border}`}>
                  {rec.priority}
                </span>
              </div>
              <p className="text-[11px] text-text-muted leading-relaxed pl-5">{rec.description}</p>
              <p className="text-[11px] font-bold text-accent-green mt-2.5 pl-5">
                Potential: {rec.potential_savings}
              </p>
            </div>
          );
        })}
      </div>
    );
  };

  const renderers = { summary: renderSummary, monthly: renderMonthly, savings: renderSavings };

  return (
    <div className="bg-bg-card rounded-2xl border border-border overflow-hidden">
      <div className="px-7 pt-7 pb-5">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary/15 to-secondary/10 border border-primary/15 flex items-center justify-center">
            <Zap className="w-[16px] h-[16px] text-primary-light" />
          </div>
          <div>
            <h3 className="text-[15px] font-bold text-text-primary">Smart Insights</h3>
            <p className="text-[10px] text-text-dim font-medium uppercase tracking-wider">Powered by Analytics</p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="px-5 mb-5">
        <div className="flex gap-1 bg-bg-base/60 rounded-xl p-1 border border-border-subtle">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-[11px] font-semibold transition-all duration-300 flex-1 justify-center ${
                activeTab === id
                  ? 'bg-primary/12 text-primary-light border border-primary/20 shadow-[0_0_15px_rgba(139,92,246,0.08)]'
                  : 'text-text-dim hover:text-text-muted border border-transparent'
              }`}
            >
              <Icon className="w-3 h-3" />
              {label}
            </button>
          ))}
        </div>
      </div>

      <div className="px-7 pb-7">
        {loading[activeTab] && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-5 h-5 text-primary-light animate-spin" />
            <span className="text-text-dim text-[12px] ml-2.5">Analyzing…</span>
          </div>
        )}

        {errors[activeTab] && !loading[activeTab] && (
          <div className="border border-accent-red/15 bg-accent-red/[0.03] rounded-xl p-4 text-center">
            <p className="text-[12px] text-accent-red">{errors[activeTab]}</p>
            <button
              onClick={() => { setData(p => ({...p, [activeTab]: null})); fetchTab(activeTab); }}
              className="mt-2 text-[11px] text-primary-light hover:underline font-medium"
            >
              Try again
            </button>
          </div>
        )}

        {!loading[activeTab] && !errors[activeTab] && renderers[activeTab]?.()}
      </div>
    </div>
  );
}
