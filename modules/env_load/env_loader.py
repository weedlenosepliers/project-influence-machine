"""
env_loader.py - A module for loading environment variables from a .env file.

This module provides functions to load environment variables from a .env 
file using the `python-dotenv` library. It is intended to be used in conjunction 
with Flask applications or other Python projects that utilize environment variables.
"""
import os
from dotenv import load_dotenv

# Define the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# Load the environment variables from the .env file
load_dotenv(dotenv_path=dotenv_path)

def get_fec_api_key():
    """
    Returns the FEC API Key.
    """
    return os.getenv('FEC_API_KEY')

def get_propublica_congress_api_key():
    """
    Returns the ProPublica Congress API Key.
    """
    return os.getenv('PROPUBLICA_CONGRESS_API_KEY')

def get_propublica_campaign_finance_api_key():
    """
    Returns the ProPublica Campaign Finance API Key.
    """
    return os.getenv('PROPUBLICA_CAMPAIGN_FINANCE_API_KEY')

def get_followthemoney_api_key():
    """
    Returns the FollowTheMoney API Key.
    """
    return os.getenv('FOLLOWTHEMONEY_API_KEY')

def get_github_api_key():
    """
    Returns the GitHub API Key.
    """
    return os.getenv('GITHUB_API_KEY')

def get_openai_api_key():
    """
    Returns the OpenAI API Key.
    """
    return os.getenv('OPENAI_API_KEY')

def get_flask_secret_key():
    """
    Returns the Flask Secret Key.
    """
    return os.getenv('FLASK_SECRET_KEY')
