// Backend contract this client expects once VITE_API_BASE is set:
//
//   POST {API_BASE}/api/query
//   body: { query: string, lang: "tm" | "ru", session_id: string, lat: number|null, lng: number|null }
//
//   Preferred: a streamed response (text/event-stream or chunked text) where each
//   chunk is a token/word of the answer, followed by a final JSON line describing
//   matched locations:
//     data: {"token":"Golaýda "}
//     data: {"token":"iň gowy "}
//     ...
//     data: {"done":true,"results":[{"name":"...","address":"...","distance_km":1.2,"is_open_now":true,"rating":4.6}]}
//
//   Fallback (non-streaming): a plain JSON body
//     { reply: string, results: [...] }
//   is also handled — the UI will simulate word-by-word reveal client-side.

const API_BASE = import.meta.env.VITE_API_BASE || '';

export const isBackendConfigured = () => Boolean(API_BASE);

async function simulateStream(text, onToken) {
  const words = text.split(' ');
  for (const word of words) {
    await new Promise((r) => setTimeout(r, 35 + Math.random() * 40));
    onToken(word + ' ');
  }
}

export async function streamQuery({ query, lang, sessionId, onToken, onThinkingDone, offlineReply }) {
  if (!API_BASE) {
    await new Promise((r) => setTimeout(r, 600 + Math.random() * 400));
    onThinkingDone?.();
    await simulateStream(offlineReply, onToken);
    return { results: [] };
  }

  const res = await fetch(`${API_BASE}/api/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, lang, session_id: sessionId, lat: null, lng: null })
  });

  if (!res.ok || !res.body) {
    onThinkingDone?.();
    throw new Error(`backend responded ${res.status}`);
  }

  const contentType = res.headers.get('content-type') || '';

  if (!contentType.includes('stream') && !res.body.getReader) {
    const data = await res.json();
    onThinkingDone?.();
    await simulateStream(data.reply || '', onToken);
    return { results: data.results || [] };
  }

  onThinkingDone?.();
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let results = [];

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split('\n');
    buffer = lines.pop();

    for (const line of lines) {
      const trimmed = line.replace(/^data:\s*/, '').trim();
      if (!trimmed) continue;
      try {
        const parsed = JSON.parse(trimmed);
        if (parsed.token) onToken(parsed.token);
        if (parsed.done) results = parsed.results || [];
      } catch {
        // non-JSON chunk: treat as raw token text
        onToken(trimmed);
      }
    }
  }

  return { results };
}
