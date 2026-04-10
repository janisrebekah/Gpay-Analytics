export default function StatCard({ title, value, icon: Icon, color = 'text-primary-light', subtext, highlight = false }) {
  return (
    <div className={`group relative rounded-2xl p-5 border transition-all duration-300 overflow-hidden ${
      highlight
        ? 'bg-gradient-to-br from-primary/10 to-primary/[0.03] border-primary/20 hover:border-primary/30 hover:shadow-[0_8px_40px_rgba(139,92,246,0.12)]'
        : 'bg-bg-card border-border hover:border-border-hover hover:shadow-[0_8px_40px_rgba(0,0,0,0.3)]'
    }`}>
      {/* Hover gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      <div className="relative">
        <div className="flex items-center justify-between mb-4">
          <span className="text-[11px] font-semibold text-text-dim uppercase tracking-[0.08em]">{title}</span>
          {Icon && (
            <div className="w-10 h-10 rounded-xl bg-bg-elevated/80 border border-border-subtle flex items-center justify-center group-hover:border-border transition-colors duration-300">
              <Icon className={`w-[18px] h-[18px] ${color} transition-transform duration-300 group-hover:scale-110`} />
            </div>
          )}
        </div>
        <p className={`font-extrabold tracking-tight ${highlight ? 'text-3xl' : 'text-2xl'} text-text-primary`}>{value}</p>
        {subtext && <p className="text-[11px] text-text-dim mt-1.5 font-medium">{subtext}</p>}
      </div>
    </div>
  );
}
