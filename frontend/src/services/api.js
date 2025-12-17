// API client for 6 backend endpoints
const API = "http://127.0.0.1:5050";

export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);
  return fetch(`${API}/upload`, { method: "POST", body: form }).then(r => r.json());
}

export async function analyze(data) {
  return fetch(`${API}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  }).then(r => r.json());
}

export async function chat(payload) {
  return fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  }).then(r => r.json());
}

export async function captureLead(data) {
  return fetch(`${API}/lead`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
}
