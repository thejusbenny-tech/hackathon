export default function ConfidenceBadge({ confidence, score }) {
  if (!confidence) return null;

  const config = {
    high:   { dot: '#22c55e', bg: '#052e16', text: '#86efac', label: 'High Confidence' },
    medium: { dot: '#eab308', bg: '#1c1400', text: '#fde047', label: 'Medium Confidence' },
    low:    { dot: '#ef4444', bg: '#1c0000', text: '#fca5a5', label: 'Low Confidence' },
  }[confidence.toLowerCase()] || { dot: '#6b7280', bg: '#111827', text: '#9ca3af', label: confidence };

  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 6,
      padding: '3px 10px', borderRadius: 999, fontSize: 12, fontWeight: 600,
      backgroundColor: config.bg, color: config.text,
      border: `1px solid ${config.dot}44`,
    }}>
      <span style={{ width: 7, height: 7, borderRadius: '50%', backgroundColor: config.dot, flexShrink: 0 }} />
      {config.label}
      {score != null && <span style={{ opacity: 0.7 }}>({Math.round(score * 100)}%)</span>}
    </span>
  );
}
