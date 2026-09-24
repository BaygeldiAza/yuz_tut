import React from 'react';
import { languages } from '../i18n/strings.js';

export default function TopBar({
  t,
  title,
  lang,
  onLangChange,
  onToggleSidebar,
  isBackendConfigured,
  sidebarToggleLabel,
  theme,
  onToggleTheme
}) {
  return (
    <div className="topbar">
      <div className="topbar-left">
        <button className="icon-btn" onClick={onToggleSidebar} aria-label={sidebarToggleLabel}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
            <rect x="3.5" y="4.5" width="17" height="15" rx="3.5" />
            <line x1="9" y1="4.5" x2="9" y2="19.5" />
          </svg>
        </button>
        <span className="topbar-title">{title}</span>
      </div>
      <div className="topbar-right">
        <span className={`status-pill ${isBackendConfigured ? 'on' : 'off'}`}>
          <span className="status-dot" />
          {isBackendConfigured ? t.onlineNotice : t.offlineNotice}
        </span>
        <button className="icon-btn" onClick={onToggleTheme} aria-label="theme">
          {theme === 'dark' ? (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="4.5" />
              <path d="M12 2.5v2M12 19.5v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2.5 12h2M19.5 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z" />
            </svg>
          )}
        </button>
        <div className="lang-toggle">
          {languages.map((l) => (
            <button
              key={l.code}
              className={lang === l.code ? 'active' : ''}
              onClick={() => onLangChange(l.code)}
            >
              {l.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
