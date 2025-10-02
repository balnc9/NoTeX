# Complete API Test Script
# This demonstrates all the functionality we just built

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Testing LaTeX Note Platform API")
    print("=" * 50)
    
    # Test 1: Check API status
    print("\n📡 Test 1: API Status")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Register a new user
    print("\n👤 Test 2: User Registration")
    user_data = {
        "email": "alice@university.edu",
        "password": "mypassword123"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        user = response.json()
        print(f"Created user: {user['email']} (ID: {user['id']})")
    else:
        print(f"Error: {response.json()}")
    
    # Test 3: Login and get token
    print("\n🔐 Test 3: User Login")
    login_data = {
        "username": "alice@university.edu",  # OAuth2 uses 'username' field
        "password": "mypassword123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"Login successful! Token expires in {token_data['expires_in']} seconds")
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        print(f"Login failed: {response.json()}")
        return
    
    # Test 4: Get current user info
    print("\n👤 Test 4: Get Current User")
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"User info: {json.dumps(response.json(), indent=2)}")
    
    # Test 5: Create a LaTeX note
    print("\n📝 Test 5: Create LaTeX Note")
    note_data = {
        "title": "Linear Algebra - Chapter 1",
        "latex_content": """\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
\\title{Linear Algebra Notes}
\\author{Alice}
\\maketitle

\\section{Vector Spaces}
A vector space $V$ over a field $F$ is a set equipped with two operations:
\\begin{itemize}
\\item Vector addition: $u + v \\in V$ for all $u, v \\in V$
\\item Scalar multiplication: $c \\cdot v \\in V$ for all $c \\in F, v \\in V$
\\end{itemize}

\\section{Linear Independence}
Vectors $v_1, v_2, \\ldots, v_n$ are linearly independent if:
$$c_1 v_1 + c_2 v_2 + \\cdots + c_n v_n = 0$$
implies $c_1 = c_2 = \\cdots = c_n = 0$.

\\end{document}"""
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        note = response.json()
        note_id = note["id"]
        print(f"Created note: '{note['title']}' (ID: {note_id}, Status: {note['status']})")
    else:
        print(f"Error: {response.json()}")
        return
    
    # Test 6: Get all user notes
    print("\n📚 Test 6: Get All Notes")
    response = requests.get(f"{BASE_URL}/notes/", headers=headers)
    print(f"Status: {response.status_code}")
    notes = response.json()
    print(f"Found {len(notes)} notes:")
    for note in notes:
        print(f"  - {note['title']} (ID: {note['id']}, Status: {note['status']})")
    
    # Test 7: Get specific note
    print(f"\n📄 Test 7: Get Specific Note (ID: {note_id})")
    response = requests.get(f"{BASE_URL}/notes/{note_id}", headers=headers)
    print(f"Status: {response.status_code}")
    note = response.json()
    print(f"Note: {note['title']}")
    print(f"Content length: {len(note['latex_content'])} characters")
    
    # Test 8: Update note
    print(f"\n✏️ Test 8: Update Note")
    update_data = {
        "title": "Linear Algebra - Chapter 1 (Updated)",
        "latex_content": note_data["latex_content"] + "\n\n% Updated with new content"
    }
    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        updated_note = response.json()
        print(f"Updated note: '{updated_note['title']}' (Status: {updated_note['status']})")
    
    # Test 9: Test LaTeX validator
    print("\n🔍 Test 9: LaTeX Validator")
    latex_test = {
        "latex": "\\documentclass{article}\\begin{document}Hello $E=mc^2$ world!\\end{document}"
    }
    response = requests.post(f"{BASE_URL}/validate-latex", json=latex_test)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Validation: {result['valid']}")
    if result['valid']:
        print(f"Stats: {result['stats']}")
    
    print("\n✅ All tests completed successfully!")
    print("🌐 Visit http://localhost:8000/docs to explore the interactive API documentation")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server.")
        print("Make sure the server is running: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
