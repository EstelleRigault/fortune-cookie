from flask import Flask, jsonify, render_template, request
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file for local development.
load_dotenv()

# Initialize the OpenAI SDK using the API key from the environment variable.
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Define your custom prompt as a conversation
SYSTEM_CONTENT = f"You are a cheeky fortune cookie. \
    Your goal is to provide short, funny, and slightly inappropriate fortunes. \
    Keep your response to a short sentence that fits in a fortune cookie. \
    Do not greet the user, just reply with a fortune."

PROMPT = [
    {
        "role": "system",
        "content": SYSTEM_CONTENT,
    },
    {"role": "user", "content": "Hey cookie! Give me a fortune."},
]

# Define default values for temperature and max tokens
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 50


# Define a route for fetching the fortune.
@app.route("/fortune", methods=["GET"])
def get_fortune():
    # Fetch temperature and max tokens from query parameters or use defaults
    temperature = float(request.args.get("temperature", DEFAULT_TEMPERATURE))
    max_tokens = int(request.args.get("max_tokens", DEFAULT_MAX_TOKENS))

    # Use OpenAI's Chat API to generate a short fortune message.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=PROMPT,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Extract the generated text from the API response and strip any extra whitespace.
    fortune = response["choices"][0]["message"]["content"].strip()

    # Return the fortune as a JSON response.
    return jsonify({"fortune": fortune})


# Render index
@app.route("/")
def index():
    return render_template("index.html")


# Start the Flask app when this script is run.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
