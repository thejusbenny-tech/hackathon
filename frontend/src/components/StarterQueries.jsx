const STARTERS = [
  {
    icon: '🏭',
    text: 'What experience do we have in manufacturing digital transformation?',
  },
  {
    icon: '📋',
    text: 'Show me our strongest proposal for a mid-market manufacturing client',
  },
  {
    icon: '🌿',
    text: 'Do we have whitepapers on ESG or sustainability?',
  },
];

export default function StarterQueries({ onSelect }) {
  return (
    <div style={{ padding: '40px 24px', textAlign: 'center' }}>
      <div style={{ fontSize: 40, marginBottom: 12 }}>💼</div>
      <h2 style={{ color: '#f1f5f9', fontSize: 22, fontWeight: 700, marginBottom: 6 }}>
        Sales Co-Pilot
      </h2>
      <p style={{ color: '#64748b', fontSize: 14, marginBottom: 36 }}>
        AI-Powered Sales Knowledge Assistant — ask about proposals, case studies, and whitepapers.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12, maxWidth: 560, margin: '0 auto' }}>
        {STARTERS.map((s, i) => (
          <button
            key={i}
            onClick={() => onSelect(s.text)}
            style={{
              display: 'flex', alignItems: 'center', gap: 14,
              padding: '14px 18px', borderRadius: 12, cursor: 'pointer', textAlign: 'left',
              backgroundColor: '#1e293b', border: '1px solid #334155', color: '#cbd5e1',
              fontSize: 14, lineHeight: 1.5, transition: 'all 0.15s',
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = '#1d4ed8'; e.currentTarget.style.backgroundColor = '#1e3a5f'; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = '#334155'; e.currentTarget.style.backgroundColor = '#1e293b'; }}
          >
            <span style={{ fontSize: 22, flexShrink: 0 }}>{s.icon}</span>
            <span>{s.text}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
