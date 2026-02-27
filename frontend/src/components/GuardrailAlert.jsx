const ICONS = {
  off_topic: '🚫',
  prompt_injection: '🛡️',
  pii_detected: '🔒',
  query_too_long: '📏',
  hallucination: '⚠️',
  low_confidence: '⚠️',
  default: '⚠️',
};

const TYPE_LABELS = {
  off_topic: 'Off-Topic Query',
  prompt_injection: 'Prompt Injection Blocked',
  pii_detected: 'PII Detected',
  query_too_long: 'Query Too Long',
  hallucination: 'Hallucination Suppressed',
  low_confidence: 'Low Confidence',
};

export default function GuardrailAlert({ guardrail }) {
  if (!guardrail) return null;
  const icon = ICONS[guardrail.type] || ICONS.default;
  const label = TYPE_LABELS[guardrail.type] || guardrail.type;

  return (
    <div style={{
      border: '1px solid #f97316',
      borderLeft: '4px solid #f97316',
      borderRadius: 8,
      backgroundColor: '#1c0e00',
      padding: '14px 16px',
      marginTop: 8,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
        <span style={{ fontSize: 18 }}>{icon}</span>
        <span style={{ color: '#fb923c', fontWeight: 700, fontSize: 14 }}>{label}</span>
      </div>
      <p style={{ color: '#fed7aa', fontSize: 14, lineHeight: 1.5 }}>{guardrail.message}</p>
    </div>
  );
}
