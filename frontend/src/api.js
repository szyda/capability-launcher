const API_BASE = 'http://localhost:8000';

async function getJson(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail = payload.detail || payload.error || 'Request failed';
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
  }

  return payload;
}

export async function fetchCapabilities() {
  const data = await getJson('/api/capabilities');
  return data.capabilities || [];
}

export async function runCapability(capabilityId, inputs) {
  return getJson(`/api/capabilities/${capabilityId}/run`, {
    method: 'POST',
    body: JSON.stringify({ inputs }),
  });
}
