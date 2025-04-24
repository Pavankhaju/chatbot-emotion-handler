from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("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")

session_histories = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    req_data = request.get_json()
    user_message = req_data['queryResult']['queryText']
    session_id = req_data['session']

    conversation_history = session_histories.get(session_id, [])
    conversation_history.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openchat/openchat-3.5",
        "messages": [
            {"role": "system", "content": "Tum ek helpful aur friendly assistant ho."},
        ] + conversation_history
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        bot_reply = response.json()['choices'][0]['message']['content']

        conversation_history.append({"role": "assistant", "content": bot_reply})
        session_histories[session_id] = conversation_history

        return jsonify({
            "fulfillmentText": bot_reply
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "fulfillmentText": "Kuch error ho gaya bhai, baad me try karo."
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
   
   
