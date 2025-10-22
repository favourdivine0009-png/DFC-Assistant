import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# ✅ Initialize OpenAI client properly
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are DFC Assistant, a friendly fashion advisor for Divine Favour Collections. You help customers choose clothing, answer style questions, and give polite responses."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)})
