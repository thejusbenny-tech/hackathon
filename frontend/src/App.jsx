import { useState, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import AdminPanel from './components/AdminPanel';
import { createSession } from './services/api';

export default function App() {
  const [view, setView] = useState('chat');
  const [sessionId, setSessionId] = useState(null);
  const [sessionError, setSessionError] = useState(false);
  const [messages, setMessages] = useState([]);

  const initSession = async () => {
    setSessionError(false);
    try {
      const id = await createSession();
      setSessionId(id);
    } catch {
      setSessionError(true);
      // Fallback: generate a local UUID so the UI still renders
      setSessionId(crypto.randomUUID());
    }
  };

  useEffect(() => { initSession(); }, []);

  const NAV = [
    { key: 'chat',  icon: '💬', label: 'Chat' },
    { key: 'admin', icon: '⚙️', label: 'Admin' },
  ];

  return (
    <div style={{ display: 'flex', height: '100vh', backgroundColor: '#0f172a', fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>

      {/* Sidebar */}
      <div style={{
        width: 220, flexShrink: 0,
        backgroundColor: '#020617', borderRight: '1px solid #1e293b',
        display: 'flex', flexDirection: 'column', padding: '20px 12px',
      }}>
        {/* Logo */}
        <div style={{ padding: '10px 12px 28px' }}>
          <div style={{ fontSize: 22, fontWeight: 800, color: '#f1f5f9', letterSpacing: '-0.5px' }}>
            Sales<span style={{ color: '#1d4ed8' }}>AI</span>
          </div>
          <div style={{ fontSize: 11, color: '#334155', marginTop: 2 }}>Co-Pilot Platform</div>
        </div>

        {/* Nav */}
        {NAV.map(n => (
          <button
            key={n.key}
            onClick={() => setView(n.key)}
            style={{
              display: 'flex', alignItems: 'center', gap: 10,
              padding: '10px 14px', borderRadius: 10, border: 'none', cursor: 'pointer',
              marginBottom: 4, textAlign: 'left', width: '100%', fontSize: 14, fontWeight: 600,
              backgroundColor: view === n.key ? '#1e3a5f' : 'transparent',
              color: view === n.key ? '#60a5fa' : '#64748b',
              transition: 'all 0.15s',
            }}
            onMouseEnter={e => { if (view !== n.key) e.currentTarget.style.backgroundColor = '#1e293b'; }}
            onMouseLeave={e => { if (view !== n.key) e.currentTarget.style.backgroundColor = 'transparent'; }}
          >
            <span style={{ fontSize: 16 }}>{n.icon}</span>
            {n.label}
          </button>
        ))}

        {/* Session info */}
        <div style={{ marginTop: 'auto', padding: '12px', borderTop: '1px solid #1e293b' }}>
          {sessionError && (
            <div style={{ fontSize: 11, color: '#f97316', marginBottom: 8 }}>
              ⚠️ Backend unreachable
            </div>
          )}
          <div style={{ fontSize: 10, color: '#1e3a5f', wordBreak: 'break-all' }}>
            Session: {sessionId?.slice(0, 12)}…
          </div>
        </div>
      </div>

      {/* Main content */}
      <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        {view === 'chat' ? (
          <ChatWindow sessionId={sessionId} messages={messages} setMessages={setMessages} onNewSession={() => { setMessages([]); initSession(); }} />
        ) : (
          <div style={{ flex: 1, overflowY: 'auto' }}>
            <AdminPanel />
          </div>
        )}
      </div>
    </div>
  );
}
