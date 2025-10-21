import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder=".")

# Load your OpenAI API key safely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are DFC Assistant, a helpful and professional AI support for DFC (Divine Favour Clothing)."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
