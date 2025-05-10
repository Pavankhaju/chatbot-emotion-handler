from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(_name_)
api_key = os.getenv("OPENROUTER_API_KEY")

@app.route("/", methods=["POST"])
def webhook():
    try:
        body = request.get_json()
        user_message = body["queryResult"]["queryText"]

        # OpenRouter API Call
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
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

if __name__ == "__main__":
    app.run()
