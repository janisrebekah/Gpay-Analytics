import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, CheckCircle2, XCircle, FileUp, ArrowRight, Shield, Zap, Database } from 'lucide-react';
import { uploadHtml } from '../api/upload';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef();
  const navigate = useNavigate();

  const handleFile = (f) => {
    if (f && f.name.endsWith('.html')) {
      setFile(f);
      setError(null);
      setResult(null);
    } else {
      setError('Please select an .html file');
    }
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await uploadHtml(file);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const features = [
    { icon: Shield, label: 'Secure', desc: 'Data stays on your machine' },
    { icon: Zap, label: 'Instant', desc: 'Parsed in seconds' },
    { icon: Database, label: 'Smart', desc: 'Auto-categorized' },
  ];

  return (
    <div className="max-w-xl mx-auto py-16 px-6">
      {/* Hero */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/15 to-secondary/10 border border-primary/15 mb-6">
          <Upload className="w-7 h-7 text-primary-light" />
        </div>
        <h1 className="text-[28px] font-extrabold text-text-primary tracking-tight">Upload Transactions</h1>
        <p className="text-[13px] text-text-dim mt-2 font-medium max-w-sm mx-auto">
          Import your Google Takeout{' '}
          <code className="bg-bg-elevated/80 px-1.5 py-0.5 rounded-md text-[11px] text-primary-light font-semibold border border-border-subtle">
            My Activity.html
          </code>{' '}
          file to get started
        </p>
      </div>

      {/* Feature chips */}
      <div className="flex items-center justify-center gap-3 mb-8">
        {features.map(({ icon: Icon, label, desc }) => (
          <div key={label} className="flex items-center gap-2 px-3 py-2 rounded-xl bg-bg-card border border-border-subtle">
            <Icon className="w-3.5 h-3.5 text-primary-light" />
            <div>
              <p className="text-[10px] font-bold text-text-primary uppercase tracking-wider">{label}</p>
              <p className="text-[9px] text-text-dim">{desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Upload card */}
      <div className="bg-bg-card rounded-2xl border border-border p-8">
        {/* Drop zone */}
        <div
          className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 cursor-pointer ${
            dragOver
              ? 'border-primary/50 bg-primary/[0.04] shadow-[0_0_50px_rgba(139,92,246,0.08)]'
              : 'border-border hover:border-border-hover hover:bg-bg-hover/20'
          }`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => { e.preventDefault(); setDragOver(false); handleFile(e.dataTransfer.files[0]); }}
          onClick={() => fileRef.current?.click()}
        >
          <div className="w-12 h-12 rounded-xl bg-bg-elevated border border-border-subtle flex items-center justify-center mx-auto mb-4">
            <FileUp className="w-5 h-5 text-text-dim" />
          </div>
          <p className="text-[13px] text-text-secondary font-medium">
            {file ? (
              <span className="text-primary-light">{file.name}</span>
            ) : (
              'Drag & drop or click to select'
            )}
          </p>
          <p className="text-[10px] text-text-dim mt-1">Supports .html files from Google Takeout</p>
          <input
            type="file"
            accept=".html"
            ref={fileRef}
            className="hidden"
            onChange={(e) => handleFile(e.target.files[0])}
          />
        </div>

        {/* Upload button */}
        <button
          onClick={handleSubmit}
          disabled={!file || loading}
          className="mt-5 w-full py-3.5 rounded-xl bg-gradient-to-r from-primary to-primary-dark text-white font-bold text-[13px] transition-all duration-300 disabled:opacity-25 disabled:cursor-not-allowed hover:shadow-[0_8px_30px_rgba(139,92,246,0.25)] hover:translate-y-[-1px] active:translate-y-0"
        >
          {loading ? 'Processing…' : 'Upload & Parse'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="mt-6 border border-accent-red/15 bg-accent-red/[0.04] rounded-xl p-4 flex items-start gap-3">
          <XCircle className="w-5 h-5 text-accent-red shrink-0 mt-0.5" />
          <p className="text-[13px] text-accent-red">{error}</p>
        </div>
      )}

      {/* Success */}
      {result && (
        <div className="mt-6 bg-bg-card border border-accent-green/15 rounded-2xl p-7">
          <div className="flex items-center gap-2.5 mb-5">
            <div className="w-8 h-8 rounded-lg bg-accent-green/10 flex items-center justify-center">
              <CheckCircle2 className="w-4 h-4 text-accent-green" />
            </div>
            <div>
              <p className="text-[14px] font-bold text-accent-green">Upload Successful</p>
              <p className="text-[10px] text-text-dim font-medium">Your transactions have been processed</p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {[
              ['Blocks Scanned', result.total_blocks_scanned],
              ['Valid Transactions', result.valid_transactions],
              ['Failed Entries', result.failed_entries],
              ['Saved to DB', result.saved_transactions_count],
            ].map(([label, val]) => (
              <div key={label} className="bg-bg-elevated/60 rounded-xl p-3.5 border border-border-subtle">
                <p className="text-[10px] text-text-dim font-semibold uppercase tracking-wider">{label}</p>
                <p className="text-[20px] font-extrabold text-text-primary mt-1">{val}</p>
              </div>
            ))}
          </div>
          <button
            onClick={() => navigate('/')}
            className="mt-5 w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-primary/10 text-primary-light font-semibold text-[13px] hover:bg-primary/15 transition-all duration-200 border border-primary/15"
          >
            View Dashboard
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}
