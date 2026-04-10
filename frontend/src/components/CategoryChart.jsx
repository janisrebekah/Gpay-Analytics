import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { formatINR } from '../utils/format';

const COLORS = [
  '#8B5CF6', '#22C55E', '#F59E0B', '#EF4444', '#06B6D4',
  '#A78BFA', '#FB7185', '#2DD4BF', '#FB923C', '#38BDF8',
  '#C084FC', '#A3E635',
];

function CustomTooltip({ active, payload }) {
  if (active && payload?.length) {
    const d = payload[0].payload;
    return (
      <div className="bg-bg-elevated/95 backdrop-blur-lg border border-border rounded-xl px-4 py-3 shadow-2xl">
        <p className="text-[13px] font-semibold text-text-primary">{d.category}</p>
        <p className="text-xs text-text-secondary mt-1">{formatINR(d.total_spend)}</p>
        <p className="text-[11px] text-text-dim mt-0.5">{d.transaction_count} transactions</p>
      </div>
    );
  }
  return null;
}

export default function CategoryChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-bg-card rounded-2xl p-8 border border-border flex items-center justify-center min-h-[440px]">
        <p className="text-text-dim text-sm">No category data available</p>
      </div>
    );
  }

  const total = data.reduce((s, c) => s + c.total_spend, 0);

  return (
    <div className="bg-bg-card rounded-2xl border border-border overflow-hidden">
      <div className="px-7 pt-7 pb-2">
        <h3 className="text-[15px] font-bold text-text-primary">Spending by Category</h3>
        <p className="text-[11px] text-text-dim mt-1 font-medium">Breakdown of your spending across categories</p>
      </div>
      <div className="px-7 pb-7">
        <div className="flex flex-col lg:flex-row items-center gap-4">
          <div className="w-full lg:w-[45%]">
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  innerRadius={68}
                  outerRadius={110}
                  paddingAngle={2}
                  dataKey="total_spend"
                  nameKey="category"
                  strokeWidth={0}
                >
                  {data.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="w-full lg:w-[55%] space-y-1">
            {data.slice(0, 8).map((cat, i) => {
              const pct = total > 0 ? ((cat.total_spend / total) * 100).toFixed(1) : 0;
              const barWidth = total > 0 ? (cat.total_spend / data[0].total_spend) * 100 : 0;
              return (
                <div key={i} className="group flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-bg-hover/50 transition-all duration-200 cursor-default">
                  <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                  <span className="text-[12px] text-text-secondary flex-1 truncate font-medium">{cat.category}</span>
                  <div className="w-16 h-1.5 rounded-full bg-bg-elevated overflow-hidden">
                    <div className="h-full rounded-full transition-all duration-500" style={{ width: `${barWidth}%`, backgroundColor: COLORS[i % COLORS.length], opacity: 0.7 }} />
                  </div>
                  <span className="text-[12px] font-bold text-text-primary w-12 text-right">{pct}%</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
