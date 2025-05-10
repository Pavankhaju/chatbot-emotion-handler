from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Webhook route
@app.route("/", methods=["POST"])  # <-- Yaha path sahi hona chahiye
def webhook():
    try:
        body = request.get_json()
        user_message = body["queryResult"]["queryText"]

        # OpenRouter API call (for emotional chatbot response)
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a warm, caring, emotionally supportive chatbot."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 200
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        bot_reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "fulfillmentText": bot_reply
        })

    except Exception as e:
        return jsonify({
            "fulfillmentText": f"Error occurred: {str(e)}"
        })

if__name__ == "__main+__":
    app.run(debug=True)
