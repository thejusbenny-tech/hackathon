import { useState, useRef } from 'react';

export default function QueryInput({ onSend, disabled }) {
  const [text, setText] = useState('');
  const ref = useRef(null);

  const submit = () => {
    const q = text.trim();
    if (!q || disabled) return;
    setText('');
    onSend(q);
  };

  const onKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div style={{
      padding: '16px 20px',
      borderTop: '1px solid #1e293b',
      backgroundColor: '#0f172a',
    }}>
      <div style={{
        display: 'flex', gap: 10, alignItems: 'flex-end',
        backgroundColor: '#1e293b', borderRadius: 14,
        border: '1px solid #334155', padding: '8px 8px 8px 16px',
      }}>
        <textarea
          ref={ref}
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={onKey}
          placeholder="Ask about proposals, case studies, whitepapers..."
          disabled={disabled}
          rows={1}
          style={{
            flex: 1, background: 'transparent', border: 'none', outline: 'none',
            color: '#f1f5f9', fontSize: 14, lineHeight: 1.6, resize: 'none',
            fontFamily: 'inherit', padding: 0, maxHeight: 120,
          }}
          onInput={e => {
            e.target.style.height = 'auto';
            e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
          }}
        />
        <button
          onClick={submit}
          disabled={disabled || !text.trim()}
          style={{
            width: 38, height: 38, borderRadius: 10, border: 'none',
            cursor: disabled || !text.trim() ? 'not-allowed' : 'pointer',
            backgroundColor: disabled || !text.trim() ? '#1f2937' : '#1d4ed8',
            color: disabled || !text.trim() ? '#374151' : '#fff',
            fontSize: 18, display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0, transition: 'all 0.15s',
          }}
        >
          {disabled ? <span style={{ fontSize: 14 }}>⏳</span> : '↑'}
        </button>
      </div>
      <p style={{ color: '#334155', fontSize: 11, textAlign: 'center', marginTop: 8 }}>
        Enter to send · Shift+Enter for new line
      </p>
    </div>
  );
}
