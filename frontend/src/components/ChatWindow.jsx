import { useState, useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import QueryInput from './QueryInput';
import StarterQueries from './StarterQueries';
import { sendQuery } from '../services/api';

export default function ChatWindow({ sessionId, onNewSession }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (query) => {
    if (!sessionId) return;

    const userMsg = { role: 'user', content: query };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const data = await sendQuery(sessionId, query);

      const assistantMsg = {
        role: 'assistant',
        content: data.answer || '',
        citations: data.citations || [],
        confidence: data.confidence,
        confidence_score: data.confidence_score,
        intent: data.intent,
        guardrail_triggered: data.guardrail_triggered || null,
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I could not reach the backend. Please check that the server is running.',
        citations: [],
        guardrail_triggered: null,
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    onNewSession();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{
        padding: '14px 20px', borderBottom: '1px solid #1e293b',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        backgroundColor: '#0f172a',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: 20 }}>💼</span>
          <div>
            <div style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 15 }}>Sales Co-Pilot</div>
            <div style={{ color: '#475569', fontSize: 11 }}>AI-Powered Sales Knowledge Assistant</div>
          </div>
        </div>
        <button
          onClick={handleNewConversation}
          style={{
            padding: '6px 14px', borderRadius: 8, border: '1px solid #334155',
            backgroundColor: 'transparent', color: '#94a3b8', cursor: 'pointer',
            fontSize: 12, fontWeight: 600, transition: 'all 0.15s',
          }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = '#1d4ed8'; e.currentTarget.style.color = '#60a5fa'; }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = '#334155'; e.currentTarget.style.color = '#94a3b8'; }}
        >
          + New Chat
        </button>
      </div>

      {/* Messages area */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '24px 20px' }}>
        {messages.length === 0 ? (
          <StarterQueries onSelect={handleSend} />
        ) : (
          <>
            {messages.map((msg, i) => (
              <MessageBubble key={i} message={msg} idx={i} />
            ))}
            {loading && (
              <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
                <div style={{
                  width: 34, height: 34, borderRadius: '50%', flexShrink: 0,
                  background: 'linear-gradient(135deg, #1d4ed8, #7c3aed)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16,
                }}>
                  🤖
                </div>
                <div style={{
                  padding: '14px 18px', borderRadius: '4px 18px 18px 18px',
                  backgroundColor: '#1e293b', border: '1px solid #1f2937',
                  display: 'flex', alignItems: 'center', gap: 8,
                }}>
                  <span style={{ color: '#60a5fa', fontSize: 13 }}>Searching knowledge base</span>
                  <span style={{ display: 'flex', gap: 4 }}>
                    {[0, 1, 2].map(i => (
                      <span key={i} style={{
                        width: 6, height: 6, borderRadius: '50%', backgroundColor: '#1d4ed8',
                        animation: `pulse 1.2s ease-in-out ${i * 0.2}s infinite`,
                      }} />
                    ))}
                  </span>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <QueryInput onSend={handleSend} disabled={loading} />

      <style>{`
        @keyframes pulse {
          0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
          40% { opacity: 1; transform: scale(1); }
        }
      `}</style>
    </div>
  );
}
