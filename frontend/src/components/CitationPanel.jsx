import { useState } from 'react';

const DOC_TYPE_COLORS = {
  case_study:  { bg: '#0c1a2e', border: '#1d4ed8', text: '#93c5fd', label: 'Case Study' },
  proposal:    { bg: '#0c1a0c', border: '#16a34a', text: '#86efac', label: 'Proposal' },
  whitepaper:  { bg: '#1a0c2e', border: '#7c3aed', text: '#c4b5fd', label: 'Whitepaper' },
  pitch_deck:  { bg: '#1a120c', border: '#d97706', text: '#fcd34d', label: 'Pitch Deck' },
  default:     { bg: '#111827', border: '#374151', text: '#9ca3af', label: 'Document' },
};

function CitationChip({ citation, idx, isExpanded, onToggle }) {
  const colors = DOC_TYPE_COLORS[citation.doc_type] || DOC_TYPE_COLORS.default;
  const shortName = citation.document?.replace(/\.pdf$|\.pptx$/i, '') || `Source ${idx + 1}`;

  return (
    <div style={{ marginBottom: 8 }}>
      <button
        onClick={onToggle}
        style={{
          display: 'inline-flex', alignItems: 'center', gap: 6,
          padding: '4px 12px', borderRadius: 6, cursor: 'pointer',
          backgroundColor: colors.bg, color: colors.text,
          border: `1px solid ${colors.border}`,
          fontSize: 12, fontWeight: 600, transition: 'opacity 0.15s',
        }}
        onMouseEnter={e => e.currentTarget.style.opacity = '0.8'}
        onMouseLeave={e => e.currentTarget.style.opacity = '1'}
      >
        <span style={{ fontSize: 10, opacity: 0.7 }}>[{idx + 1}]</span>
        <span style={{
          padding: '1px 6px', borderRadius: 4, fontSize: 10,
          backgroundColor: colors.border + '44', textTransform: 'uppercase', letterSpacing: '0.05em',
        }}>
          {colors.label}
        </span>
        <span style={{ maxWidth: 260, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {shortName}
        </span>
        {citation.year && <span style={{ opacity: 0.6 }}>{citation.year}</span>}
        <span style={{ opacity: 0.5 }}>{isExpanded ? '▲' : '▼'}</span>
      </button>

      {isExpanded && (
        <div style={{
          marginTop: 6, padding: 14, borderRadius: 8,
          backgroundColor: colors.bg, border: `1px solid ${colors.border}44`,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
            <div>
              <div style={{ color: colors.text, fontWeight: 600, fontSize: 13 }}>{citation.document}</div>
              <div style={{ color: '#6b7280', fontSize: 12, marginTop: 2 }}>
                {[
                  citation.doc_type && colors.label,
                  citation.year && `Year: ${citation.year}`,
                  citation.page != null && `Page ${citation.page}`,
                  citation.relevance_score != null && `Score: ${(citation.relevance_score * 100).toFixed(0)}%`,
                ].filter(Boolean).join('  ·  ')}
              </div>
            </div>
            {citation.drive_link && (
              <a
                href={citation.drive_link}
                target="_blank"
                rel="noreferrer"
                style={{
                  padding: '4px 10px', borderRadius: 6, fontSize: 12, textDecoration: 'none',
                  backgroundColor: '#1e3a5f', color: '#60a5fa', border: '1px solid #1d4ed8',
                  whiteSpace: 'nowrap', flexShrink: 0, marginLeft: 10,
                }}
              >
                Open in Drive ↗
              </a>
            )}
          </div>
          {citation.chunk_text && (
            <blockquote style={{
              margin: 0, padding: '8px 12px',
              borderLeft: `3px solid ${colors.border}`,
              backgroundColor: '#0f172a',
              color: '#cbd5e1', fontSize: 13, lineHeight: 1.6,
              borderRadius: '0 6px 6px 0', fontStyle: 'italic',
            }}>
              "{citation.chunk_text}"
            </blockquote>
          )}
        </div>
      )}
    </div>
  );
}

export default function CitationPanel({ citations }) {
  const [expanded, setExpanded] = useState({});

  if (!citations || citations.length === 0) return null;

  const toggle = (idx) => setExpanded(prev => ({ ...prev, [idx]: !prev[idx] }));

  return (
    <div style={{ marginTop: 12 }}>
      <div style={{ color: '#6b7280', fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 8 }}>
        Sources ({citations.length})
      </div>
      {citations.map((c, i) => (
        <CitationChip key={i} citation={c} idx={i} isExpanded={!!expanded[i]} onToggle={() => toggle(i)} />
      ))}
    </div>
  );
}
