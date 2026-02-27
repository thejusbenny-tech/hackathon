import { useState } from 'react';

export default function FeedbackButtons({ messageId }) {
  const [vote, setVote] = useState(null);

  const handleVote = (v) => {
    if (vote === v) { setVote(null); return; }
    setVote(v);
    // TODO: POST /feedback when backend supports it
  };

  return (
    <div style={{ display: 'flex', gap: 6, marginTop: 8 }}>
      <button
        onClick={() => handleVote('up')}
        title="Helpful"
        style={{
          padding: '3px 10px', borderRadius: 6, fontSize: 14, cursor: 'pointer',
          border: `1px solid ${vote === 'up' ? '#22c55e' : '#1f2937'}`,
          backgroundColor: vote === 'up' ? '#052e16' : 'transparent',
          color: vote === 'up' ? '#22c55e' : '#4b5563',
          transition: 'all 0.15s',
        }}
      >
        👍
      </button>
      <button
        onClick={() => handleVote('down')}
        title="Not helpful"
        style={{
          padding: '3px 10px', borderRadius: 6, fontSize: 14, cursor: 'pointer',
          border: `1px solid ${vote === 'down' ? '#ef4444' : '#1f2937'}`,
          backgroundColor: vote === 'down' ? '#1c0000' : 'transparent',
          color: vote === 'down' ? '#ef4444' : '#4b5563',
          transition: 'all 0.15s',
        }}
      >
        👎
      </button>
    </div>
  );
}
