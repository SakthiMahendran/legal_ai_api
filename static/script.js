// Legal AI API Test Frontend JavaScript

const API_BASE = "http://localhost:8000/api/v1";
let authToken = null;
let currentSessionId = null;

// Utility Functions
function showResponse(data, isError = false) {
  const responseElement = document.getElementById("api-response");
  responseElement.textContent = JSON.stringify(data, null, 2);
  responseElement.className = isError ? "error" : "";
}

function updateAuthStatus(message, isSuccess = true) {
  const statusElement = document.getElementById("auth-status");
  statusElement.textContent = message;
  statusElement.className = `status ${isSuccess ? "success" : "error"}`;
}

function updateCurrentSession(sessionId) {
  currentSessionId = sessionId;
  document.getElementById("current-session-id").textContent =
    sessionId || "None";
}

function showTab(tabName) {
  // Hide all tabs
  document.querySelectorAll(".tab-content").forEach((tab) => {
    tab.classList.remove("active");
  });
  document.querySelectorAll(".tab-button").forEach((button) => {
    button.classList.remove("active");
  });

  // Show selected tab
  document.getElementById(`${tabName}-tab`).classList.add("active");
  event.target.classList.add("active");
}

function setLoading(buttonElement, isLoading) {
  if (isLoading) {
    buttonElement.classList.add("loading");
    buttonElement.disabled = true;
  } else {
    buttonElement.classList.remove("loading");
    buttonElement.disabled = false;
  }
}

// API Request Helper
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (authToken) {
    defaultOptions.headers["Authorization"] = `Bearer ${authToken}`;
  }

  const finalOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, finalOptions);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error("API Request failed:", error);
    throw error;
  }
}

// Authentication Functions
async function register() {
  const button = event.target;
  setLoading(button, true);

  try {
    const data = await apiRequest("/auth/register/", {
      method: "POST",
      body: JSON.stringify({
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
      }),
    });

    showResponse(data);
    updateAuthStatus("Registration successful!");
  } catch (error) {
    showResponse({ error: error.message }, true);
    updateAuthStatus("Registration failed", false);
  } finally {
    setLoading(button, false);
  }
}

async function login() {
  const button = event.target;
  setLoading(button, true);

  try {
    const data = await apiRequest("/auth/login/", {
      method: "POST",
      body: JSON.stringify({
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
      }),
    });

    authToken = data.access;
    showResponse(data);
    updateAuthStatus(
      `Logged in successfully! Token: ${authToken.substring(0, 20)}...`
    );
  } catch (error) {
    showResponse({ error: error.message }, true);
    updateAuthStatus("Login failed", false);
  } finally {
    setLoading(button, false);
  }
}

async function logout() {
  const button = event.target;
  setLoading(button, true);

  try {
    const data = await apiRequest("/auth/logout/", {
      method: "POST",
      body: JSON.stringify({}),
    });

    authToken = null;
    currentSessionId = null;
    showResponse(data);
    updateAuthStatus("Logged out successfully");
    updateCurrentSession(null);
  } catch (error) {
    showResponse({ error: error.message }, true);
    updateAuthStatus("Logout failed", false);
  } finally {
    setLoading(button, false);
  }
}

// Session Functions
async function createSession() {
  const button = event.target;
  setLoading(button, true);

  try {
    const data = await apiRequest("/sessions/", {
      method: "POST",
      body: JSON.stringify({
        title: document.getElementById("session-title").value,
        status: document.getElementById("session-status").value,
      }),
    });

    updateCurrentSession(data.id);
    showResponse(data);
    await listSessions(); // Refresh sessions list
  } catch (error) {
    showResponse({ error: error.message }, true);
  } finally {
    setLoading(button, false);
  }
}

async function listSessions() {
  const button = event.target;
  if (button) setLoading(button, true);

  try {
    const data = await apiRequest("/sessions/");
    showResponse(data);

    // Update sessions tab
    const sessionsList = document.getElementById("sessions-list");
    sessionsList.innerHTML = "";

    if (data.length === 0) {
      sessionsList.innerHTML = "<p>No sessions found.</p>";
    } else {
      data.forEach((session) => {
        const sessionDiv = document.createElement("div");
        sessionDiv.className = "session-item";
        sessionDiv.innerHTML = `
                    <h4>${session.title}</h4>
                    <p><strong>Status:</strong> ${session.status}</p>
                    <p><strong>ID:</strong> ${session.id}</p>
                    <div class="meta">
                        Created: ${new Date(
                          session.created_at
                        ).toLocaleString()}<br>
                        Updated: ${new Date(
                          session.updated_at
                        ).toLocaleString()}
                    </div>
                    <button onclick="updateCurrentSession(${
                      session.id
                    })" class="btn btn-primary" style="margin-top: 10px;">
                        Select Session
                    </button>
                `;
        sessionsList.appendChild(sessionDiv);
      });
    }
  } catch (error) {
    showResponse({ error: error.message }, true);
  } finally {
    if (button) setLoading(button, false);
  }
}

// Message Functions
async function sendMessage() {
  const button = event.target;
  setLoading(button, true);

  if (!currentSessionId) {
    alert("Please create or select a session first!");
    setLoading(button, false);
    return;
  }

  try {
    const data = await apiRequest("/messages/", {
      method: "POST",
      body: JSON.stringify({
        session_id: currentSessionId,
        role: document.getElementById("message-role").value,
        content: document.getElementById("message-content").value,
      }),
    });

    showResponse(data);
    await listMessages(); // Refresh messages list
  } catch (error) {
    showResponse({ error: error.message }, true);
  } finally {
    setLoading(button, false);
  }
}

async function listMessages() {
  const button = event.target;
  if (button) setLoading(button, true);

  try {
    const endpoint = currentSessionId
      ? `/messages/?session_id=${currentSessionId}`
      : "/messages/";
    const data = await apiRequest(endpoint);
    showResponse(data);

    // Update messages tab
    const messagesList = document.getElementById("messages-list");
    messagesList.innerHTML = "";

    if (data.length === 0) {
      messagesList.innerHTML = "<p>No messages found.</p>";
    } else {
      data.forEach((message) => {
        const messageDiv = document.createElement("div");
        messageDiv.className = "message-item";
        messageDiv.innerHTML = `
                    <h4>${message.role.toUpperCase()}</h4>
                    <p>${message.content}</p>
                    <div class="meta">
                        Session ID: ${message.session_id} | 
                        Created: ${new Date(
                          message.created_at
                        ).toLocaleString()}
                    </div>
                `;
        messagesList.appendChild(messageDiv);
      });
    }
  } catch (error) {
    showResponse({ error: error.message }, true);
  } finally {
    if (button) setLoading(button, false);
  }
}

// Chat Functions
async function sendChatMessage() {
  const button = event.target;
  const chatInput = document.getElementById("chat-input");
  const message = chatInput.value.trim();

  if (!message) {
    alert("Please enter a message!");
    return;
  }

  if (!currentSessionId) {
    alert("Please create or select a session first!");
    return;
  }

  setLoading(button, true);

  try {
    // Add user message to chat immediately
    addChatMessage("user", message);
    chatInput.value = "";

    // Show typing indicator
    const typingIndicator = addTypingIndicator();

    // Send to AI
    const data = await apiRequest("/ai/chat/", {
      method: "POST",
      body: JSON.stringify({
        session_id: currentSessionId,
        message: message,
      }),
    });

    // Remove typing indicator
    removeTypingIndicator(typingIndicator);

    // Add AI response to chat
    addChatMessage("assistant", data.ai_message.content);

    showResponse(data);
  } catch (error) {
    removeTypingIndicator();
    addChatMessage("system", `Error: ${error.message}`);
    showResponse({ error: error.message }, true);
  } finally {
    setLoading(button, false);
  }
}

function addChatMessage(role, content) {
  const chatMessages = document.getElementById("chat-messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `chat-message ${role}`;

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";

  if (role === "user") {
    contentDiv.innerHTML = `<strong>You:</strong> ${content}`;
  } else if (role === "assistant") {
    contentDiv.innerHTML = `<strong>Legal AI Assistant:</strong> ${content.replace(
      /\n/g,
      "<br>"
    )}`;
  } else {
    contentDiv.innerHTML = content;
  }

  messageDiv.appendChild(contentDiv);
  chatMessages.appendChild(messageDiv);

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return messageDiv;
}

function addTypingIndicator() {
  const chatMessages = document.getElementById("chat-messages");
  const typingDiv = document.createElement("div");
  typingDiv.className = "typing-indicator";
  typingDiv.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;

  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return typingDiv;
}

function removeTypingIndicator(indicator) {
  if (indicator && indicator.parentNode) {
    indicator.parentNode.removeChild(indicator);
  } else {
    // Remove any typing indicators
    const indicators = document.querySelectorAll(".typing-indicator");
    indicators.forEach((ind) => ind.remove());
  }
}

function clearChat() {
  const chatMessages = document.getElementById("chat-messages");
  chatMessages.innerHTML = `
        <div class="chat-message system">
            <div class="message-content">
                <strong>Legal AI Assistant:</strong> Hello! I'm your legal AI assistant. I can help you with legal document drafting, answer legal questions, and provide general legal information. How can I assist you today?
            </div>
        </div>
    `;
}

// AI Functions
async function generateDocument() {
  const button = event.target;
  setLoading(button, true);

  try {
    const data = await apiRequest("/ai/generate/", {
      method: "POST",
      body: JSON.stringify({
        prompt: document.getElementById("ai-prompt").value,
        conversation_history: [],
      }),
    });

    showResponse(data);
  } catch (error) {
    showResponse({ error: error.message }, true);
  } finally {
    setLoading(button, false);
  }
}

async function checkAIHealth() {
  const button = event.target;
  setLoading(button, true);

  try {
    const data = await apiRequest("/ai/health/");
    showResponse(data);
  } catch (error) {
    showResponse({ error: error.message }, true);
  } finally {
    setLoading(button, false);
  }
}

// Document Functions
async function uploadDocument() {
  const button = event.target;
  setLoading(button, true);

  if (!currentSessionId) {
    alert("Please create or select a session first!");
    setLoading(button, false);
    return;
  }

  const fileInput = document.getElementById("document-file");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file to upload!");
    setLoading(button, false);
    return;
  }

  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      `${API_BASE}/documents/upload/?session_id=${currentSessionId}`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
        body: formData,
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP ${response.status}`);
    }

    showResponse(data);
    await listDocuments(); // Refresh documents list
  } catch (error) {
    showResponse({ error: error.message }, true);
  } finally {
    setLoading(button, false);
  }
}

async function listDocuments() {
  const button = event.target;
  if (button) setLoading(button, true);

  try {
    const endpoint = currentSessionId
      ? `/documents/?session_id=${currentSessionId}`
      : "/documents/";
    const data = await apiRequest(endpoint);
    showResponse(data);

    // Update documents tab
    const documentsList = document.getElementById("documents-list");
    documentsList.innerHTML = "";

    if (data.length === 0) {
      documentsList.innerHTML = "<p>No documents found.</p>";
    } else {
      data.forEach((document) => {
        const documentDiv = document.createElement("div");
        documentDiv.className = "document-item";
        documentDiv.innerHTML = `
                    <h4>${document.title}</h4>
                    <p><strong>Filename:</strong> ${document.filename}</p>
                    <p><strong>Status:</strong> ${document.status}</p>
                    <p><strong>Session ID:</strong> ${document.session_id}</p>
                    <div class="meta">
                        Created: ${new Date(
                          document.created_at
                        ).toLocaleString()}<br>
                        Updated: ${new Date(
                          document.updated_at
                        ).toLocaleString()}
                    </div>
                `;
        documentsList.appendChild(documentDiv);
      });
    }
  } catch (error) {
    showResponse({ error: error.message }, true);
  } finally {
    if (button) setLoading(button, false);
  }
}

// Test All Functions
async function runAllTests() {
  const button = event.target;
  const progressDiv = document.getElementById("test-progress");

  setLoading(button, true);
  progressDiv.style.display = "block";
  progressDiv.innerHTML = "<h4>Running All Tests...</h4>";

  const tests = [
    { name: "Register User", func: testRegister },
    { name: "Login User", func: testLogin },
    { name: "Create Session", func: testCreateSession },
    { name: "Send Message", func: testSendMessage },
    { name: "AI Chat", func: testAIChat },
    { name: "Generate Document", func: testGenerateDocument },
    { name: "Upload Document", func: testUploadDocument },
    { name: "List All Data", func: testListAll },
    { name: "Logout User", func: testLogout },
  ];

  for (const test of tests) {
    const stepDiv = document.createElement("div");
    stepDiv.className = "test-step running";
    stepDiv.textContent = `🔄 ${test.name}...`;
    progressDiv.appendChild(stepDiv);

    try {
      await test.func();
      stepDiv.className = "test-step success";
      stepDiv.textContent = `✅ ${test.name} - PASSED`;
    } catch (error) {
      stepDiv.className = "test-step error";
      stepDiv.textContent = `❌ ${test.name} - FAILED: ${error.message}`;
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  setLoading(button, false);
}

// Individual test functions
async function testRegister() {
  return apiRequest("/auth/register/", {
    method: "POST",
    body: JSON.stringify({
      username: "testuser",
      email: "test@example.com",
      password: "testpassword",
    }),
  });
}

async function testLogin() {
  const data = await apiRequest("/auth/login/", {
    method: "POST",
    body: JSON.stringify({
      email: "test@example.com",
      password: "testpassword",
    }),
  });
  authToken = data.access;
  return data;
}

async function testCreateSession() {
  const data = await apiRequest("/sessions/", {
    method: "POST",
    body: JSON.stringify({
      title: "Test Session",
      status: "active",
    }),
  });
  currentSessionId = data.id;
  return data;
}

async function testSendMessage() {
  return apiRequest("/messages/", {
    method: "POST",
    body: JSON.stringify({
      session_id: currentSessionId,
      role: "user",
      content: "Hello, this is a test message.",
    }),
  });
}

async function testAIChat() {
  return apiRequest("/ai/chat/", {
    method: "POST",
    body: JSON.stringify({
      session_id: currentSessionId,
      message: "What is a contract and what are its key elements?",
    }),
  });
}

async function testGenerateDocument() {
  return apiRequest("/ai/generate/", {
    method: "POST",
    body: JSON.stringify({
      prompt: "Draft a simple test document.",
      conversation_history: [],
    }),
  });
}

async function testUploadDocument() {
  // Create a test file
  const testContent = "This is a test document for the API test.";
  const blob = new Blob([testContent], { type: "text/plain" });
  const formData = new FormData();
  formData.append("file", blob, "test.txt");

  const response = await fetch(
    `${API_BASE}/documents/upload/?session_id=${currentSessionId}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

async function testListAll() {
  await apiRequest("/sessions/");
  await apiRequest("/messages/");
  await apiRequest("/documents/");
  return { message: "All lists retrieved successfully" };
}

async function testLogout() {
  const data = await apiRequest("/auth/logout/", {
    method: "POST",
    body: JSON.stringify({}),
  });
  authToken = null;
  currentSessionId = null;
  return data;
}

// Initialize the page
document.addEventListener("DOMContentLoaded", function () {
  console.log("Legal AI API Test Frontend loaded");
  updateAuthStatus("Not logged in", false);
  updateCurrentSession(null);

  // Add Enter key functionality for chat input
  const chatInput = document.getElementById("chat-input");
  if (chatInput) {
    chatInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendChatMessage();
      }
    });
  }
});
