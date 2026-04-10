import { formatINR } from '../utils/format';

const CAT_COLORS = {
  'Education': '#8B5CF6',
  'Food & Dining': '#F59E0B',
  'Groceries': '#22C55E',
  'Shopping': '#EF4444',
  'Bills & Utilities': '#3B82F6',
  'Entertainment': '#A78BFA',
  'Transportation': '#FB923C',
  'Health & Fitness': '#06B6D4',
  'Personal Care': '#FB7185',
  'Other': '#64748B',
};

export default function TopMerchants({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-bg-card rounded-2xl p-8 border border-border flex items-center justify-center min-h-[400px]">
        <p className="text-text-dim text-sm">No merchant data available</p>
      </div>
    );
  }

  const max = data[0]?.total_spend || 1;

  return (
    <div className="bg-bg-card rounded-2xl border border-border overflow-hidden">
      <div className="px-7 pt-7 pb-5">
        <h3 className="text-[15px] font-bold text-text-primary">Top Merchants</h3>
        <p className="text-[11px] text-text-dim mt-1 font-medium">Where your money goes most</p>
      </div>
      <div className="px-5 pb-5 space-y-1">
        {data.map((m, i) => {
          const pct = (m.total_spend / max) * 100;
          const catColor = CAT_COLORS[m.category] || '#64748B';
          return (
            <div key={i} className="group relative rounded-xl overflow-hidden transition-all duration-200 hover:bg-bg-hover/40">
              {/* Spend proportion bar */}
              <div
                className="absolute inset-0 opacity-[0.04] group-hover:opacity-[0.08] transition-opacity duration-300"
                style={{ background: `linear-gradient(90deg, ${catColor} ${pct}%, transparent ${pct}%)` }}
              />
              <div className="relative flex items-center gap-4 px-4 py-3.5">
                <div className="w-7 h-7 rounded-lg bg-bg-elevated border border-border-subtle flex items-center justify-center">
                  <span className="text-[10px] font-bold text-text-dim">{i + 1}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-[13px] font-semibold text-text-primary truncate">{m.merchant_name}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span
                      className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-md border"
                      style={{
                        color: catColor,
                        backgroundColor: `${catColor}10`,
                        borderColor: `${catColor}20`,
                      }}
                    >
                      {m.category || 'Other'}
                    </span>
                    <span className="text-[10px] text-text-dim">·</span>
                    <span className="text-[10px] text-text-dim font-medium">{m.transaction_count} txns</span>
                  </div>
                </div>
                <p className="text-[14px] font-bold text-text-primary shrink-0">{formatINR(m.total_spend)}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
