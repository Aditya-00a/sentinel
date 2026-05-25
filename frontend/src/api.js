const API_BASE = '/api';

export async function fetchDemoProfiles() {
  const res = await fetch(`${API_BASE}/demo-profiles`);
  if (!res.ok) throw new Error('Failed to fetch demo profiles');
  return res.json();
}

export async function fetchDataMode() {
  const res = await fetch(`${API_BASE}/data-mode`);
  if (!res.ok) throw new Error('Failed to fetch data mode');
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${API_BASE}/history`);
  if (!res.ok) throw new Error('Failed to fetch history');
  return res.json();
}

export async function fetchReview(reviewId) {
  const res = await fetch(`${API_BASE}/review/${reviewId}`);
  if (!res.ok) throw new Error('Review not found');
  return res.json();
}

export function streamReview(body, onEvent, onComplete, onError) {
  const url = `${API_BASE}/review`;
  const controller = new AbortController();

  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
    body: JSON.stringify(body),
    signal: controller.signal,
  })
    .then(async (response) => {
      if (!response.ok) {
        const errText = await response.text();
        onError(new Error(errText));
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        let currentEvent = 'message';
        for (const line of lines) {
          if (line.startsWith('event:')) {
            currentEvent = line.slice(6).trim();
          } else if (line.startsWith('data:')) {
            const dataStr = line.slice(5).trim();
            if (dataStr) {
              try {
                const data = JSON.parse(dataStr);
                if (currentEvent === 'complete') {
                  onComplete(data);
                } else {
                  onEvent(currentEvent, data);
                }
              } catch (e) {
                // skip malformed JSON
              }
            }
            currentEvent = 'message';
          }
        }
      }
    })
    .catch((err) => {
      if (err.name !== 'AbortError') {
        onError(err);
      }
    });

  return () => controller.abort();
}

export function streamDemoReview(profileId, onEvent, onComplete, onError) {
  const url = `${API_BASE}/review-demo/${profileId}`;
  const controller = new AbortController();

  fetch(url, {
    method: 'POST',
    headers: { 'Accept': 'text/event-stream' },
    signal: controller.signal,
  })
    .then(async (response) => {
      if (!response.ok) {
        const errText = await response.text();
        onError(new Error(errText));
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        let currentEvent = 'message';
        for (const line of lines) {
          if (line.startsWith('event:')) {
            currentEvent = line.slice(6).trim();
          } else if (line.startsWith('data:')) {
            const dataStr = line.slice(5).trim();
            if (dataStr) {
              try {
                const data = JSON.parse(dataStr);
                if (currentEvent === 'complete') {
                  onComplete(data);
                } else {
                  onEvent(currentEvent, data);
                }
              } catch (e) {
                // skip
              }
            }
            currentEvent = 'message';
          }
        }
      }
    })
    .catch((err) => {
      if (err.name !== 'AbortError') {
        onError(err);
      }
    });

  return () => controller.abort();
}
