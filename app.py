from flask import Flask, jsonify
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file for local development.
load_dotenv()

# Initialize the OpenAI SDK using the API key from the environment variable.
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Define your custom prompt here
PROMPT = "Imagine you're a sentient AI fortune cookie with a cheeky sense of humor. You've just realized you're not just filled with paper, but with bytes and bits. Craft a funny and slightly inappropriate fortune that includes a dash of innuendo."
# Set the desired temperature here (e.g., 0.7 for a balance between randomness and determinism)
TEMPERATURE = 0.7


# Define a route for fetching the fortune.
@app.route("/fortune", methods=["GET"])
def get_fortune():
    # Use OpenAI's Completion API to generate a short fortune message with the specified prompt and temperature.
    response = openai.Completion.create(
        engine="gpt-3.5-turbo", prompt=PROMPT, max_tokens=50, temperature=TEMPERATURE
    )

    # Extract the generated text from the API response and strip any extra whitespace.
    fortune = response.choices[0].text.strip()

    # Return the fortune as a JSON response.
    return jsonify({"fortune": fortune})


# Start the Flask app when this script is run.
if __name__ == "__main__":
    app.run(debug=True)
