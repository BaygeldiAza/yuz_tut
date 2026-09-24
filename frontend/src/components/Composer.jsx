import React, { useRef } from 'react';

export default function Composer({ t, value, onChange, onSend, disabled }) {
  const textareaRef = useRef(null);

  const grow = (el) => {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="composer-wrap">
      <div className="composer">
        <textarea
          ref={textareaRef}
          rows={1}
          placeholder={t.placeholder}
          value={value}
          onChange={(e) => {
            onChange(e.target.value);
            grow(e.target);
          }}
          onKeyDown={handleKeyDown}
        />
        <button className="send-btn" onClick={onSend} disabled={disabled || !value.trim()}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 12h14M13 6l6 6-6 6" />
          </svg>
        </button>
      </div>
      <div className="composer-hint">{t.hint}</div>
    </div>
  );
}
