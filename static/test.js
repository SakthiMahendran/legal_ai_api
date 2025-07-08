let token = null;
// Registration handler

document.getElementById('registerForm').onsubmit = async function(e) {
    e.preventDefault();
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const res = await fetch('/api/v1/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });
    const data = await res.json();
    if(res.ok) {
        document.getElementById('registerResult').innerText = 'Registration successful! You can now login.';
    } else {
        document.getElementById('registerResult').innerText = data.detail || 'Registration failed';
    }
};
document.getElementById('loginForm').onsubmit = async function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const res = await fetch('/api/v1/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if(res.ok) {
        token = data.access_token;
        document.getElementById('loginResult').innerText = 'Login successful!';
    } else {
        document.getElementById('loginResult').innerText = data.detail || 'Login failed';
    }
};
document.getElementById('generateForm').onsubmit = async function(e) {
    e.preventDefault();
    if(!token) {
        document.getElementById('generateResult').innerText = 'You must login first.';
        return;
    }
    const prompt = document.getElementById('prompt').value;
    const res = await fetch('/api/v1/ai/generate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ prompt, conversation_history: [] })
    });
    const data = await res.json();
    document.getElementById('generateResult').innerText = res.ok ? data.result : (data.detail || 'Generation failed');
};
