import requests
import json
import sys

def test_review():
    url = "http://localhost:8000/review-code"
    
    payload = {
        "code": "def hello(): print('hello')",
        "description": "A simple hello world function",
        "language": "python"
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        try:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        except:
            print("Response Text (not JSON):")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to localhost:8000. Is the backend running?")
    except Exception as e:
        print(f"Error: {e}")

def test_health():
    url = "http://localhost:8000/health"
    print(f"Sending request to {url}...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_health()
    print("-" * 20)
    test_review()
