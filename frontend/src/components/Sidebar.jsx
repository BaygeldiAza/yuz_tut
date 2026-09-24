import React from 'react';

export default function Sidebar({ t, open, onClose, chats, activeChatId, onNewChat, onSelectChat }) {
  return (
    <>
      <div className={`sidebar-scrim ${open ? 'visible' : ''}`} onClick={onClose} />
      <aside className={`sidebar ${open ? 'open' : ''}`}>
        <div className="sidebar-head">
          <div className="brand">
            <span className="brand-mark">
              <img src="/logo.svg" alt="" />
            </span>
            <span className="brand-name">{t.appName}</span>
          </div>
        </div>

        <button className="new-chat-btn" onClick={onNewChat}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 5v14M5 12h14" strokeLinecap="round" />
          </svg>
          {t.newChat}
        </button>

        <div className="history-panel">
          <div className="history-label">{t.historyTitle}</div>
          {chats.length === 0 && <div className="history-empty">{t.historyEmpty}</div>}
          {chats.map((chat) => (
            <button
              key={chat.id}
              className={`history-item ${chat.id === activeChatId ? 'active' : ''}`}
              onClick={() => onSelectChat(chat.id)}
              title={chat.title}
            >
              {chat.title}
            </button>
          ))}
        </div>

        <div className="sidebar-footer">
          <div className="account-avatar">G</div>
          <div className="account-meta">
            <div className="account-name">{t.guest}</div>
            <div className="account-sub">{t.signIn}</div>
          </div>
        </div>
      </aside>
    </>
  );
}
