import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { formatINR } from '../utils/format';

function CustomTooltip({ active, payload, label }) {
  if (active && payload?.length) {
    return (
      <div className="bg-bg-elevated/95 backdrop-blur-lg border border-border rounded-xl px-4 py-3 shadow-2xl">
        <p className="text-[13px] font-semibold text-text-primary">{label}</p>
        <p className="text-xs text-text-secondary mt-1">{formatINR(payload[0].value)}</p>
        <p className="text-[11px] text-text-dim mt-0.5">{payload[0].payload.transaction_count} transactions</p>
      </div>
    );
  }
  return null;
}

export default function MonthlyChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-bg-card rounded-2xl p-8 border border-border flex items-center justify-center min-h-[440px]">
        <p className="text-text-dim text-sm">No monthly data available</p>
      </div>
    );
  }

  return (
    <div className="bg-bg-card rounded-2xl border border-border overflow-hidden">
      <div className="px-7 pt-7 pb-2">
        <h3 className="text-[15px] font-bold text-text-primary">Monthly Trends</h3>
        <p className="text-[11px] text-text-dim mt-1 font-medium">Your spending patterns over time</p>
      </div>
      <div className="px-4 pb-6">
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={data} barSize={16} barGap={6}>
            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#8B5CF6" stopOpacity={1} />
                <stop offset="100%" stopColor="#8B5CF6" stopOpacity={0.3} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.03)" vertical={false} />
            <XAxis
              dataKey="month_label"
              tick={{ fill: '#64748B', fontSize: 10, fontWeight: 500 }}
              axisLine={false}
              tickLine={false}
              dy={8}
            />
            <YAxis
              tick={{ fill: '#64748B', fontSize: 10, fontWeight: 500 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}K`}
              width={48}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(139,92,246,0.05)' }} />
            <Bar dataKey="total_spend" fill="url(#barGradient)" radius={[5, 5, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
