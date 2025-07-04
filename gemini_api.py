import requests

GEMINI_API_KEY = "AIzaSyBkOnH0sV6vhrAZy6XWDmAj802UVDwfQL8"  # Replace with your key
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def query_gemini_with_history(history):
    headers = {"Content-Type": "application/json"}
    data = {"contents": history}

    response = requests.post(GEMINI_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            return "⚠️ Failed to parse response."
    else:
        return f"❌ API error: {response.status_code} - {response.text}"
