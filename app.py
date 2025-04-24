from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(_name_)

# API key environment se uthao
OPENROUTER_API_KEY = os.getenv("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")

# Har session ka alag history store hoga
session_histories = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    req_data = request.get_json()

    # User ka message aur session ID
    user_message = req_data['queryResult']['queryText']
    session_id = req_data['session']

    # Purani history lo ya blank list lo
    conversation_history = session_histories.get(session_id, [])

    # User ka current message add karo
    conversation_history.append({"role": "user", "content": user_message})

    # API headers
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # API payload
    payload = {
        "model": "openchat/openchat-3.5",
        "messages": [
            {"role": "system", "content": "Tum ek helpful aur friendly assistant ho."}
        ] + conversation_history
    }

    try:
        # API call
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        # Bot ka response lo
        bot_reply = response.json()['choices'][0]['message']['content']

        # Bot ka reply bhi history me save karo
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

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
   
   
