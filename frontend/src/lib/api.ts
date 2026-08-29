const API_BASE = '/api/proxy';

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE}${endpoint}`;
  
  const headers = new Headers(options.headers || {});
  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(url, { ...options, headers });
  
  if (!response.ok) {
    let errorMsg = 'An error occurred';
    try {
      const errorData = await response.json();
      if (Array.isArray(errorData.detail)) {
        // FastAPI validation errors
        errorMsg = errorData.detail.map((e: any) => `${e.loc?.join('.')} ${e.msg}`).join(", ");
      } else {
        errorMsg = errorData.detail || errorData.message || errorMsg;
      }
    } catch {
      // Ignore json parse error
    }
    throw new Error(errorMsg);
  }

  return response.json();
}
