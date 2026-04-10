import { Link, useLocation } from 'react-router-dom';
import { BarChart3, Upload } from 'lucide-react';

export default function Navbar() {
  const { pathname } = useLocation();

  const link = (path, label, Icon) => {
    const active = pathname === path;
    return (
      <Link
        to={path}
        className={`group flex items-center gap-2 px-4 py-2 rounded-xl text-[13px] font-medium transition-all duration-300 ${
          active
            ? 'bg-primary/12 text-primary-light border border-primary/20'
            : 'text-text-muted hover:text-text-secondary hover:bg-bg-hover border border-transparent'
        }`}
      >
        <Icon className={`w-[15px] h-[15px] transition-transform duration-300 group-hover:scale-110`} />
        {label}
      </Link>
    );
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-border bg-bg-base/70 backdrop-blur-2xl backdrop-saturate-150">
      <div className="max-w-[1360px] mx-auto px-6 lg:px-10">
        <div className="flex items-center justify-between h-[60px]">
          <Link to="/" className="flex items-center gap-3 text-text-primary no-underline group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary/20 to-secondary/10 flex items-center justify-center border border-primary/15 group-hover:border-primary/30 transition-all duration-300 group-hover:shadow-[0_0_20px_rgba(139,92,246,0.15)]">
              <BarChart3 className="w-[18px] h-[18px] text-primary-light" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-[15px] tracking-tight leading-tight">GPay Analytics</span>
              <span className="text-[10px] text-text-dim font-medium tracking-wider uppercase">Dashboard</span>
            </div>
          </Link>
          <div className="flex items-center gap-2">
            {link('/upload', 'Upload', Upload)}
            {link('/', 'Dashboard', BarChart3)}
          </div>
        </div>
      </div>
    </nav>
  );
}
