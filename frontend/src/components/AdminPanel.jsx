import { useState, useEffect } from 'react';
import { getPipelineStats, triggerIngest, getHealth } from '../services/api';

const DOC_TYPE_BADGE = {
  case_study:  { bg: '#1d4ed8', label: 'Case Study' },
  proposal:    { bg: '#16a34a', label: 'Proposal' },
  whitepaper:  { bg: '#7c3aed', label: 'Whitepaper' },
  pitch_deck:  { bg: '#d97706', label: 'Pitch Deck' },
};

export default function AdminPanel() {
  const [stats, setStats] = useState(null);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [ingesting, setIngesting] = useState(false);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const [s, h] = await Promise.all([getPipelineStats(), getHealth()]);
      setStats(s);
      setHealth(h);
    } catch (e) {
      setError('Cannot reach backend. Is the server running?');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleIngest = async () => {
    setIngesting(true);
    try {
      await triggerIngest();
      await load();
    } catch (e) {
      setError('Ingestion failed: ' + (e.message || 'unknown error'));
    } finally {
      setIngesting(false);
    }
  };

  const fmt = (iso) => iso ? new Date(iso).toLocaleString() : '—';

  return (
    <div style={{ padding: '28px 32px', color: '#e2e8f0', maxWidth: 1000 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 28 }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: '#f1f5f9' }}>Pipeline Admin</h1>
          <p style={{ color: '#475569', fontSize: 13, marginTop: 4 }}>Ingestion status and document index overview</p>
        </div>
        <button
          onClick={handleIngest}
          disabled={ingesting}
          style={{
            padding: '10px 20px', borderRadius: 10, border: 'none', cursor: ingesting ? 'wait' : 'pointer',
            background: ingesting ? '#374151' : 'linear-gradient(135deg, #1d4ed8, #7c3aed)',
            color: '#fff', fontWeight: 700, fontSize: 14,
          }}
        >
          {ingesting ? '⏳ Ingesting...' : '↻ Re-ingest Documents'}
        </button>
      </div>

      {error && (
        <div style={{ padding: 16, borderRadius: 10, backgroundColor: '#1c0000', border: '1px solid #ef4444', color: '#fca5a5', marginBottom: 24 }}>
          ⚠️ {error}
        </div>
      )}

      {loading ? (
        <div style={{ color: '#475569', fontSize: 14 }}>Loading pipeline stats...</div>
      ) : stats && (
        <>
          {/* Summary cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 28 }}>
            {[
              { label: 'Total Documents', value: stats.total_documents, icon: '📄' },
              { label: 'Total Chunks', value: stats.total_chunks, icon: '🧩' },
              { label: 'Indexed Chunks', value: health?.indexed_chunks ?? '—', icon: '✅' },
            ].map((card, i) => (
              <div key={i} style={{
                padding: 20, borderRadius: 12, backgroundColor: '#1e293b',
                border: '1px solid #334155',
              }}>
                <div style={{ fontSize: 26, marginBottom: 8 }}>{card.icon}</div>
                <div style={{ fontSize: 28, fontWeight: 800, color: '#f1f5f9' }}>{card.value}</div>
                <div style={{ fontSize: 12, color: '#64748b', marginTop: 4 }}>{card.label}</div>
              </div>
            ))}
          </div>

          {/* Last ingestion */}
          {stats.last_ingestion && (
            <div style={{ marginBottom: 20, color: '#64748b', fontSize: 13 }}>
              Last ingestion: <span style={{ color: '#94a3b8' }}>{fmt(stats.last_ingestion)}</span>
            </div>
          )}

          {/* Documents table */}
          <div style={{ borderRadius: 12, border: '1px solid #1e293b', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#1e293b' }}>
                  {['Document', 'Type', 'Year', 'Chunks', 'Regions', 'Status'].map(h => (
                    <th key={h} style={{
                      padding: '12px 16px', textAlign: 'left', fontSize: 11,
                      color: '#64748b', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em',
                    }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {stats.documents?.map((doc, i) => {
                  const badge = DOC_TYPE_BADGE[doc.doc_type] || { bg: '#374151', label: doc.doc_type };
                  return (
                    <tr key={i} style={{ borderTop: '1px solid #0f172a', backgroundColor: i % 2 === 0 ? '#111827' : '#0f172a' }}>
                      <td style={{ padding: '11px 16px', fontSize: 13, color: '#cbd5e1', maxWidth: 280 }}>
                        <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {doc.filename}
                        </div>
                      </td>
                      <td style={{ padding: '11px 16px' }}>
                        <span style={{
                          padding: '2px 8px', borderRadius: 4, fontSize: 11, fontWeight: 600,
                          backgroundColor: badge.bg + '33', color: badge.bg === '#374151' ? '#9ca3af' : badge.bg,
                          border: `1px solid ${badge.bg}55`,
                        }}>
                          {badge.label}
                        </span>
                      </td>
                      <td style={{ padding: '11px 16px', fontSize: 13, color: '#94a3b8' }}>{doc.year || '—'}</td>
                      <td style={{ padding: '11px 16px', fontSize: 13, color: '#94a3b8' }}>{doc.chunks}</td>
                      <td style={{ padding: '11px 16px', fontSize: 12, color: '#64748b' }}>
                        {doc.regions?.join(', ') || '—'}
                      </td>
                      <td style={{ padding: '11px 16px' }}>
                        <span style={{
                          padding: '2px 8px', borderRadius: 4, fontSize: 11, fontWeight: 600,
                          backgroundColor: doc.status === 'indexed' ? '#052e16' : '#1c0e00',
                          color: doc.status === 'indexed' ? '#22c55e' : '#f97316',
                          border: `1px solid ${doc.status === 'indexed' ? '#22c55e' : '#f97316'}44`,
                        }}>
                          {doc.status}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
