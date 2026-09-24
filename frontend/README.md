# Yuzztut frontend

Node.js/Vite + React chat interface for the Yuzztut AI pipeline. TM/RU languages,
collapsible chat history sidebar (hidden by default), streaming answer rendering,
and a light green/white theme with a soft animated gradient behind the empty state.

## Run it

```bash
npm install
npm run dev
```

Opens on `http://localhost:5173`.

## Connecting to the backend

The UI currently runs in **offline demo mode**: it simulates a "thinking" pause and
word-by-word streaming with a placeholder reply, and never calls a real server.

To connect it to the AI pipeline's API:

1. Copy `.env.example` to `.env` and set `VITE_API_BASE` to the backend URL, e.g.
   `VITE_API_BASE=http://localhost:8000`.
2. Implement `POST {VITE_API_BASE}/api/query` on the backend. Request/response
   contract is documented at the top of `src/api/client.js`:
   - Request: `{ query, lang, session_id, lat, lng }`
   - Best: a streamed response (SSE-style `data: {...}` lines), one token per line,
     ending with `data: {"done":true,"results":[...]}`.
   - Also supported: a single non-streamed JSON body `{ reply, results }` — the UI
     will simulate the streaming reveal client-side in that case.
3. Restart `npm run dev`. The status pill in the top bar switches from
   "Backend birikdirilmedi" to "Birikdirildi" automatically once `VITE_API_BASE`
   is set — no other code changes needed.

`vite.config.js` also proxies `/api` to `VITE_API_PROXY_TARGET` (defaults to
`http://localhost:8000`) for local dev if you'd rather call a relative path.

## Structure

```
src/
  api/client.js       backend contract + streaming/offline logic
  i18n/strings.js      TM/RU strings — edit here to change copy or add a language
  components/
    Sidebar.jsx         new chat, chat history, account (hidden by default, toggled)
    TopBar.jsx          sidebar toggle, chat title, language switch, connection status
    ChatArea.jsx        empty-state hero, message list, thinking indicator, result cards
    Composer.jsx         input bar
  App.jsx               state: active chat, chat history, streaming orchestration
  styles.css            theme tokens + layout (light green / white, Gemini-style glow)
```

## Rebranding

- **Icon/logo**: replace `public/logo.svg` with the real Yuzztut icon (same
  filename, or update the two references below if you rename it). It's used as
  the browser favicon (`index.html`) and as the mark in the sidebar header,
  chat avatar, and empty-state hero (all pull from `/logo.svg` automatically —
  one file, no other code changes needed).
- **App name**: `appName` in `src/i18n/strings.js` (both `tm` and `ru`).
- **Colors**: `--green-*` tokens in `src/styles.css`, light theme at the top of
  the file, dark theme under `[data-theme="dark"]`.

## Dark mode

Toggled with the sun/moon icon in the top bar. Defaults to the OS color-scheme
preference on first load, then remembers the user's choice in `localStorage`
(`yuzztut-theme`). Dark theme uses deep green/near-black tokens instead of the
light green/white ones — same layout, just the `[data-theme="dark"]` variable
overrides in `src/styles.css`.
- Auth/account section in the sidebar is a static placeholder (`Myhman` / `Hasaba gir`).
- Chat history currently lives only in memory (React state) and resets on reload;
  persistence (backend-side or local) is not implemented yet.
