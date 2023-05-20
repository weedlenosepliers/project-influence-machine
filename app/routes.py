"""
This module defines the routes for the Flask application.
"""
from flask import request, jsonify
from your_module import chat_with_gpt

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    API endpoint to chat with GPT.
    """
    # Retrieve the input message from the API request
    message = request.json.get('message', '')

    # Call the function to chat with GPT and get the response
    response = chat_with_gpt(message)

    # Return the response as a JSON object
    return jsonify({'response': response})
