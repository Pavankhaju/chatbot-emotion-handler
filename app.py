from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("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")

# Store conversations by session ID
session_memory = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    req_data = request.get_json()
    session_id = req_data['session']  # Dialogflow ka session ID
    user_message = req_data['queryResult']['queryText']

    if session_id not in session_memory:
        session_memory[session_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    session_memory[session_id].append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openchat/openchat-3.5",
        "messages": session_memory[session_id]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        bot_reply = response.json()['choices'][0]['message']['content']
        session_memory[session_id].append({"role": "assistant", "content": bot_reply})

        return jsonify({"fulfillmentText": bot_reply})
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"fulfillmentText": "Kuch error ho gaya bhai, baad me try karo."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
