const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Lightweight fetch wrapper with error handling.
 */
async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, options);
  if (!res.ok) {
    const body = await res.text();
    // Try to extract a friendly detail from FastAPI's {detail: ...} responses
    try {
      const parsed = JSON.parse(body);
      if (parsed.detail) throw new Error(parsed.detail);
    } catch (e) {
      if (e.message && e.message !== body) throw e;
    }
    throw new Error(`API error ${res.status}`);
  }
  return res.json();
}

export function get(path) {
  return request(path);
}

export function postFile(path, file, fieldName = 'file') {
  const formData = new FormData();
  formData.append(fieldName, file);
  return request(path, { method: 'POST', body: formData });
}
