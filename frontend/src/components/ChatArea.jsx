import React, { useEffect, useRef } from 'react';

function ResultCard({ result, t }) {
  return (
    <div className="result-card">
      <div className="result-top">
        <span className="result-name">{result.name}</span>
        {result.distance_km != null && <span className="result-dist">{result.distance_km} km</span>}
      </div>
      {result.address && <div className="result-meta">{result.address}</div>}
      {result.is_open_now != null && (
        <span className={`result-open ${result.is_open_now ? '' : 'closed'}`}>
          {result.is_open_now ? t.open : t.closed}
        </span>
      )}
    </div>
  );
}

function AvatarMark() {
  return (
    <div className="avatar">
      <img src="/logo.svg" alt="" />
    </div>
  );
}

function ThinkingRow({ label }) {
  return (
    <div className="msg-row assistant">
      <AvatarMark />
      <div className="bubble">
        <span className="thinking-shimmer">{label}…</span>
      </div>
    </div>
  );
}

function MessageRow({ message, t }) {
  if (message.role === 'user') {
    return (
      <div className="msg-row user">
        <div className="bubble">{message.text}</div>
      </div>
    );
  }
  return (
    <div className="msg-row assistant">
      <AvatarMark />
      <div className="bubble">
        <span>
          {message.text}
          {message.streaming && <span className="cursor" />}
        </span>
        {message.results && message.results.length > 0 && (
          <div className="result-list">
            {message.results.map((r, i) => (
              <ResultCard key={i} result={r} t={t} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function ChatArea({ t, messages, isThinking, onSuggestion }) {
  const threadRef = useRef(null);

  useEffect(() => {
    if (threadRef.current) {
      threadRef.current.scrollTop = threadRef.current.scrollHeight;
    }
  }, [messages, isThinking]);

  if (messages.length === 0) {
    return (
      <div className="thread thread-empty">
        <div className="hero-glow" aria-hidden="true" />
        <div className="empty-state">
          <div className="empty-mark">
            <img src="/logo.svg" alt="" />
          </div>
          <h1>{t.heroTitle}</h1>
          <p>{t.heroSubtitle}</p>
          <div className="suggestions">
            {t.suggestions.map((s) => (
              <button key={s} className="suggestion-chip" onClick={() => onSuggestion(s)}>
                {s}
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="thread" ref={threadRef}>
      <div className="thread-inner">
        {messages.map((m) => (
          <MessageRow key={m.id} message={m} t={t} />
        ))}
        {isThinking && <ThinkingRow label={t.thinking} />}
      </div>
    </div>
  );
}
