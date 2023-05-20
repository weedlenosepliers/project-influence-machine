"""
Administrator interface for interacting with the ChatGPT API and GitHub repositories.
"""

import os
import openai
from flask import Flask, request, render_template
from github import Github
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Set the Flask secret key
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Set the path to the templates directory
templates_path = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'templates')

# Initialize the Flask app with the templates path
app = Flask(__name__, template_folder=templates_path)


@app.route('/')
def index():
    """
    Home page of the administrator interface.
    """
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """
    Send a chat message to the GPT-3 API and display the response.
    """
    if request.method == 'POST':
        # Retrieve the input message from the form
        message = request.form.get('message')

        # Pass the message to the chat_with_gpt function
        response = chat_with_gpt(message)

        # Render a template with the chat history
        return render_template('chat.html', message=message, response=response)
    else:
        return render_template('chat.html')


@app.route('/github', methods=['GET'])
def github():
    """
    Display information about GitHub repositories.
    """
    # Authenticate with the GitHub API
    github_api_key = os.getenv('GITHUB_API_KEY')
    g = Github(github_api_key)

    # Get your user
    user = g.get_user()

    # Get a list of your repositories
    repos = [repo.name for repo in user.get_repos()]

    # Render a template with the list of repositories
    return render_template('github.html', repos=repos)


def chat_with_gpt(message):
    """
    Send a chat message to the GPT-3 API and return the response.
    """
    # Set up the OpenAI API credentials
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key

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

    # Return the response
    return response


if __name__ == '__main__':
    app.run()
