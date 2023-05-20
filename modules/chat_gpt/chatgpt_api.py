"""
This module defines the API for chatting with GPT.
"""

import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

@app.route('/')
def index():
    """
    Welcome page for the Influence Machine.
    """
    return 'Welcome to the Influence Machine'

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    API endpoint to chat with GPT.
    """
    # Retrieve the input message from the API request
    message = request.json.get('message', '')

    # Set up the OpenAI API credentials
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    # Define the parameters for the chat completion
    completion_parameters = {
        'engine': 'davinci',
        'prompt': message,
        'max_tokens': 50,  # Adjust the response length as needed
        'temperature': 0.6,
        'n': 1,
        'stop': None,
    }

    # Send the completion request to ChatGPT
    completion_response = openai.Completion.create(**completion_parameters)

    # Extract the generated response from the completion
    response = completion_response.choices[0].text.strip()

    # Return the response as a JSON object
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()
