import React, { useState, useCallback, useEffect } from 'react';
import Sidebar from './components/Sidebar.jsx';
import TopBar from './components/TopBar.jsx';
import ChatArea from './components/ChatArea.jsx';
import Composer from './components/Composer.jsx';
import { strings } from './i18n/strings.js';
import { streamQuery, isBackendConfigured } from './api/client.js';

function newId() {
  return crypto.randomUUID();
}

function makeChat() {
  return { id: newId(), title: null, messages: [] };
}

export default function App() {
  const [lang, setLang] = useState('tm');
  const [theme, setTheme] = useState(() => {
    if (typeof window === 'undefined') return 'light';
    const saved = localStorage.getItem('yuzztut-theme');
    if (saved) return saved;
    return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  });
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(makeChat());
  const [inputValue, setInputValue] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [isSending, setIsSending] = useState(false);

  const t = strings[lang];

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('yuzztut-theme', theme);
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  const startNewChat = useCallback(() => {
    setActiveChat(makeChat());
    setSidebarOpen(false);
  }, []);

  const selectChat = useCallback(
    (id) => {
      const found = chats.find((c) => c.id === id);
      if (found) {
        setActiveChat(found);
        setSidebarOpen(false);
      }
    },
    [chats]
  );

  const sendMessage = useCallback(
    async (text) => {
      const trimmed = text.trim();
      if (!trimmed || isSending) return;

      setIsSending(true);
      setInputValue('');

      const userMsg = { id: newId(), role: 'user', text: trimmed };
      const assistantId = newId();

      let workingChat = {
        ...activeChat,
        title: activeChat.title || trimmed,
        messages: [...activeChat.messages, userMsg]
      };
      setActiveChat(workingChat);
      setIsThinking(true);

      const wasNew = !chats.find((c) => c.id === workingChat.id);
      if (wasNew) {
        setChats((prev) => [{ id: workingChat.id, title: workingChat.title }, ...prev]);
      } else {
        setChats((prev) => prev.map((c) => (c.id === workingChat.id ? { ...c, title: workingChat.title } : c)));
      }

      let streamedText = '';
      const appendAssistantPlaceholder = () => {
        setIsThinking(false);
        workingChat = {
          ...workingChat,
          messages: [...workingChat.messages, { id: assistantId, role: 'assistant', text: '', streaming: true, results: [] }]
        };
        setActiveChat(workingChat);
      };

      const onToken = (token) => {
        streamedText += token;
        workingChat = {
          ...workingChat,
          messages: workingChat.messages.map((m) =>
            m.id === assistantId ? { ...m, text: streamedText } : m
          )
        };
        setActiveChat(workingChat);
      };

      try {
        const { results } = await streamQuery({
          query: trimmed,
          lang,
          sessionId: workingChat.id,
          onToken,
          onThinkingDone: appendAssistantPlaceholder,
          offlineReply: t.offlineReply
        });

        workingChat = {
          ...workingChat,
          messages: workingChat.messages.map((m) =>
            m.id === assistantId ? { ...m, streaming: false, results } : m
          )
        };
        setActiveChat(workingChat);
      } catch (err) {
        setIsThinking(false);
        workingChat = {
          ...workingChat,
          messages: [
            ...workingChat.messages.filter((m) => m.id !== assistantId),
            { id: assistantId, role: 'assistant', text: t.errorReply, streaming: false, results: [] }
          ]
        };
        setActiveChat(workingChat);
      } finally {
        setIsSending(false);
      }
    },
    [activeChat, chats, isSending, lang, t]
  );

  return (
    <div className="app">
      <Sidebar
        t={t}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        chats={chats}
        activeChatId={activeChat.id}
        onNewChat={startNewChat}
        onSelectChat={selectChat}
      />
      <main className="main">
        <TopBar
          t={t}
          title={activeChat.title || t.newChat}
          lang={lang}
          onLangChange={setLang}
          onToggleSidebar={() => setSidebarOpen((v) => !v)}
          sidebarToggleLabel={t.sidebarToggle}
          isBackendConfigured={isBackendConfigured()}
          theme={theme}
          onToggleTheme={toggleTheme}
        />
        <ChatArea
          t={t}
          messages={activeChat.messages}
          isThinking={isThinking}
          onSuggestion={(s) => sendMessage(s)}
        />
        <Composer
          t={t}
          value={inputValue}
          onChange={setInputValue}
          onSend={() => sendMessage(inputValue)}
          disabled={isSending}
        />
      </main>
    </div>
  );
}
