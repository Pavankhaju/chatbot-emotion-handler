#reate a basic Python Flask project for Dialogflow + OpenRouter webhook

import os

project_path = "/mnt/data/dialogflow-openrouter-python"

os.makedirs(project_path, exist_ok=True)

# main.py file
main_py = """from flask import Flask, request, jsonify
import requests

app = Flask(_name_)

OPENROUTER_API_KEY = "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"  # <-- Replace with your OpenRouter API key

@app.route("/webhook", methods=["POST"])
def webhook():
    req_data = request.get_json()
    user_message = req_data['queryResult']['queryText']

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openchat/openchat-3.5",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        bot_reply = response.json()['choices'][0]['message']['content']

        return jsonify({
            "fulfillmentText": bot_reply
        })
    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "fulfillmentText": "Kuch error ho gaya bhai, thodi der baad try karo."
        })

if _name_ == "_main_":
    app.run(debug=True, port=5000)
"""

# requirements.txt file
requirements_txt = """flask
requests
"""

# Write files
with open(f"{project_path}/main.py", "w") as f:
    f.write(main_py)

with open(f"{project_path}/requirements.txt", "w") as f:
    f.write(requirements_txt)

project_path