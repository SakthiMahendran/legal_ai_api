const API_BASE = "http://localhost:8000/api/v1";
let authToken = null;

const statusEl = document.getElementById("status-message");
const rawEl = document.getElementById("raw-response");
const btnLogout = document.getElementById("btn-logout");

function showResponse(data, error = false) {
  rawEl.textContent = JSON.stringify(data, null, 2);
  if (error) {
    statusEl.textContent = data.detail || data.error || "Error occurred";
    statusEl.className = "status error";
  }
}

function setStatus(text, success = true) {
  statusEl.textContent = text;
  statusEl.className = success ? "status success" : "status error";
}

async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const headers = { "Content-Type": "application/json", ...options.headers };
  if (authToken) headers["Authorization"] = `Bearer ${authToken}`;

  const res = await fetch(url, { ...options, headers });
  const payload = await res.json();
  if (!res.ok) throw payload;
  return payload;
}

// Register
document.getElementById("btn-register").onclick = async () => {
  try {
    const data = await apiRequest("/auth/register/", {
      method: "POST",
      body: JSON.stringify({
        username: document.getElementById("reg-username").value,
        email: document.getElementById("reg-email").value,
        password: document.getElementById("reg-password").value
      })
    });
    showResponse(data);
    setStatus("Registration successful!", true);
  } catch (err) {
    showResponse(err, true);
    setStatus("Registration failed", false);
  }
};

// Login
document.getElementById("btn-login").onclick = async () => {
  try {
    const data = await apiRequest("/auth/login/", {
      method: "POST",
      body: JSON.stringify({
        email: document.getElementById("login-email").value,
        password: document.getElementById("login-password").value
      })
    });
    authToken = data.access;
    showResponse(data);
    setStatus("Logged in ✓", true);
    btnLogout.disabled = false;
  } catch (err) {
    showResponse(err, true);
    setStatus("Login failed", false);
  }
};

// Logout
btnLogout.onclick = async () => {
  try {
    const data = await apiRequest("/auth/logout/", { method: "POST", body: "{}" });
    authToken = null;
    showResponse(data);
    setStatus("Logged out", true);
    btnLogout.disabled = true;
  } catch (err) {
    showResponse(err, true);
    setStatus("Logout failed", false);
  }
};
