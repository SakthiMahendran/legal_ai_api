import requests
import json
import os

BASE_URL = "http://localhost:8000"
EMAIL = "demo@example.com"
PASSWORD = "demopassword"

TICK = "\u2705"
CROSS = "\u274C"

def print_status(name, ok, resp=None):
    emoji = TICK if ok else CROSS
    print(f"{emoji} {name} - {'PASS' if ok else 'FAIL'}")
    if resp is not None:
        try:
            print(json.dumps(resp, indent=2))
        except Exception:
            print(resp)

def test_register():
    url = f"{BASE_URL}/api/v1/auth/register/"
    payload = {"username": "demo", "email": EMAIL, "password": PASSWORD}
    r = requests.post(url, json=payload)
    print_status("Register", r.status_code in [200, 201, 400], r.json())
    return r

def test_login():
    url = f"{BASE_URL}/api/v1/auth/login/"
    payload = {"email": EMAIL, "password": PASSWORD}
    r = requests.post(url, json=payload)
    ok = r.ok and ("access" in r.json())
    print_status("Login", ok, r.json())
    return r.json()["access"] if ok else None

def test_create_session(token):
    url = f"{BASE_URL}/api/v1/sessions/"
    payload = {"title": "Test Session", "status": "active"}
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(url, json=payload, headers=headers)
    ok = r.ok and "id" in r.json()
    print_status("Create Session", ok, r.json())
    return r.json()["id"] if ok else None

def test_send_message(token, session_id):
    url = f"{BASE_URL}/api/v1/messages/"
    payload = {"session": session_id, "role": "user", "content": "Hello, what is a contract?"}
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(url, json=payload, headers=headers)
    ok = r.ok and "id" in r.json()
    print_status("Send Message", ok, r.json())
    return r.json()["id"] if ok else None

def test_generate_document(token):
    url = f"{BASE_URL}/api/v1/ai/generate/"
    payload = {"prompt": "Draft a simple NDA agreement.", "conversation_history": []}
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(url, json=payload, headers=headers)
    ok = r.ok and "result" in r.json()
    print_status("AI Document Generation", ok, r.json())
    return r.json()["result"] if ok else None

def test_list_documents(token):
    url = f"{BASE_URL}/api/v1/documents/"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    ok = r.ok
    print_status("List Documents", ok, r.json())
    return r.json() if ok else None

def test_upload_document(token, session_id):
    url = f"{BASE_URL}/api/v1/documents/upload/"
    headers = {"Authorization": f"Bearer {token}"}
    # Create a dummy file
    filename = "dummy.txt"
    with open(filename, "w") as f:
        f.write("This is a test document.")
    files = {"file": open(filename, "rb")}
    data = {"session_id": session_id}
    r = requests.post(url, files=files, data=data, headers=headers)
    files["file"].close()
    os.remove(filename)
    ok = r.ok and "id" in r.json()
    print_status("Upload Document", ok, r.json())
    return r.json()["id"] if ok else None

def test_logout(token):
    url = f"{BASE_URL}/api/v1/auth/logout/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"token": token}
    r = requests.post(url, json=payload, headers=headers)
    ok = r.ok
    print_status("Logout", ok, r.json())

def main():
    test_register()
    token = test_login()
    if not token:
        print("Cannot continue without login token.")
        return
    session_id = test_create_session(token)
    if not session_id:
        print("Cannot continue without session.")
        return
    test_send_message(token, session_id)
    test_generate_document(token)
    test_upload_document(token, session_id)
    test_list_documents(token)
    test_logout(token)

if __name__ == "__main__":
    main()

def test_list_documents(token):
    url = f"{BASE_URL}/api/v1/documents/"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    print("List Documents:", r.status_code, r.json())
    return r

if __name__ == "__main__":
    # Register (will fail if already registered)
    test_register()
    # Login
    token = test_login()
    if token:
        test_list_documents(token)
    else:
        print("Login failed. Check credentials or registration.")
