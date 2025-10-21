import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder=".")

# Initialize OpenAI client
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
                {
                    "role": "system",
                    "content": (
                        "You are DFC Assistant — the official AI of Divine Favour Collections. "
                        "The store specializes in both male and female wears, "
                        "located at Okonkwo Plaza, opposite Jaiz Bank, Jos, Plateau State, Nigeria. "
                        "You are friendly, polite, and professional. You help customers find outfits, "
                        "recommend styles, explain prices, and provide store information."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
