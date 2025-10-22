import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# ✅ Create the client safely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return "DFC Assistant is live! Send POST JSON to /chat with {'message':'Hi'}."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # modern, fast model
            messages=[
                {"role": "system", "content": "You are DFC Assistant, a friendly fashion expert for Divine Favour Collections in Jos. You help customers choose stylish male and female outfits politely."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
  
