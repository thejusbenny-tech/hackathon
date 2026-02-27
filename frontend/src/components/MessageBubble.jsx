import ReactMarkdown from 'react-markdown';
import CitationPanel from './CitationPanel';
import ConfidenceBadge from './ConfidenceBadge';
import GuardrailAlert from './GuardrailAlert';
import FeedbackButtons from './FeedbackButtons';

function UserBubble({ content }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 20 }}>
      <div style={{
        maxWidth: '70%', padding: '12px 16px', borderRadius: '18px 18px 4px 18px',
        backgroundColor: '#1d4ed8', color: '#fff', fontSize: 14, lineHeight: 1.6,
      }}>
        {content}
      </div>
    </div>
  );
}

function AssistantBubble({ message, idx }) {
  const { content, citations, confidence, confidence_score, guardrail_triggered, intent } = message;
  const isGuardrail = !!guardrail_triggered;

  return (
    <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: 24 }}>
      <div style={{ display: 'flex', gap: 12, maxWidth: '85%' }}>
        {/* Avatar */}
        <div style={{
          width: 34, height: 34, borderRadius: '50%', flexShrink: 0,
          background: 'linear-gradient(135deg, #1d4ed8, #7c3aed)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 16, marginTop: 2,
        }}>
          🤖
        </div>

        <div style={{ flex: 1 }}>
          {/* Confidence + intent row */}
          {!isGuardrail && (confidence || intent) && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8, flexWrap: 'wrap' }}>
              {confidence && <ConfidenceBadge confidence={confidence} score={confidence_score} />}
              {intent && (
                <span style={{
                  fontSize: 11, color: '#6b7280', padding: '2px 8px',
                  border: '1px solid #1f2937', borderRadius: 4,
                  textTransform: 'uppercase', letterSpacing: '0.05em',
                }}>
                  {intent.replace(/_/g, ' ')}
                </span>
              )}
            </div>
          )}

          {/* Answer bubble */}
          <div style={{
            padding: '14px 18px', borderRadius: '4px 18px 18px 18px',
            backgroundColor: '#1e293b', color: '#e2e8f0',
            fontSize: 14, lineHeight: 1.7,
            border: isGuardrail ? '1px solid #f97316' : '1px solid #1f2937',
          }}>
            {isGuardrail ? (
              <GuardrailAlert guardrail={guardrail_triggered} />
            ) : (
              <ReactMarkdown
                components={{
                  p: ({ children }) => <p style={{ marginBottom: 8 }}>{children}</p>,
                  ul: ({ children }) => <ul style={{ paddingLeft: 20, marginBottom: 8 }}>{children}</ul>,
                  li: ({ children }) => <li style={{ marginBottom: 4 }}>{children}</li>,
                  strong: ({ children }) => <strong style={{ color: '#f1f5f9' }}>{children}</strong>,
                }}
              >
                {content}
              </ReactMarkdown>
            )}
          </div>

          {/* Citations */}
          {!isGuardrail && (
            citations && citations.length > 0
              ? <CitationPanel citations={citations} />
              : (
                <div style={{
                  marginTop: 10, fontSize: 12, color: '#475569',
                  display: 'flex', alignItems: 'center', gap: 6,
                }}>
                  <span style={{ opacity: 0.6 }}>ℹ</span>
                  No source documents found for this response.
                </div>
              )
          )}

          {/* Feedback */}
          {!isGuardrail && <FeedbackButtons messageId={idx} />}
        </div>
      </div>
    </div>
  );
}

export default function MessageBubble({ message, idx }) {
  if (message.role === 'user') return <UserBubble content={message.content} />;
  return <AssistantBubble message={message} idx={idx} />;
}
