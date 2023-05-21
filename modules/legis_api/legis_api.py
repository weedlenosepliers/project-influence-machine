"""
Module for fetching and retrieving information about members of 
the U.S. Congress using the ProPublica Congress API.

This module contains functions to:
1. Fetch members of Congress from the ProPublica Congress API.
2. Print and save the fetched data into text files.
"""
import os
import requests
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Set the API key
API_KEY = os.getenv('PROPUBLICA_CONGRESS_API_KEY')

# Define the API endpoints for House and Senate members
HOUSE_ENDPOINT = 'https://api.propublica.org/congress/v1/{congress}/house/members.json'
SENATE_ENDPOINT = 'https://api.propublica.org/congress/v1/{congress}/senate/members.json'

# Set the request headers with the API key
headers = {
    'X-API-Key': API_KEY
}

def get_members(congress, chamber):
    """
    Fetch members from the ProPublica Congress API.

    Args:
        congress (int): The number of the congress.
        chamber (str): The chamber ('house' or 'senate').

    Returns:
        list: A list of member objects.
    """
    endpoint = HOUSE_ENDPOINT if chamber.lower() == 'house' else SENATE_ENDPOINT
    endpoint = endpoint.format(congress=congress)

    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data['results'][0]['members']
        else:
            print(f'Failed to fetch {chamber} members.')
            return []
    except requests.exceptions.RequestException as ex:
        print('Error:', ex)
        return []


def print_and_save_current_congress_members(congress_number):
    """
    Fetches and prints the members of the current Congress from the ProPublica Congress API.
    Replaces the existing data files with the fetched data.

    Args:
        congress_number (int): The number of the current Congress.
    """
    house_members = get_members(congress_number, 'house')
    senate_members = get_members(congress_number, 'senate')

    # Directory and file paths
    dir_path = '/workspaces/project-influence-machine/data/'
    house_file = os.path.join(dir_path, 'house_member_contributions.txt')
    senate_file = os.path.join(dir_path, 'senate_member_contributions.txt')

    print('House Members:')
    with open(house_file, 'w', encoding='utf-8') as house_file_writer:
        for member in house_members:
            print(f"Name: {member['first_name']} {member['last_name']}")
            print(f"Party: {member['party']}")
            house_file_writer.write(f"Name: {member['first_name']} {member['last_name']}\n")
            house_file_writer.write(f"Party: {member['party']}\n")

    print('Senate Members:')
    with open(senate_file, 'w', encoding='utf-8') as senate_file_writer:
        for member in senate_members:
            print(f"Name: {member['first_name']} {member['last_name']}")
            print(f"Party: {member['party']}")
            senate_file_writer.write(f"Name: {member['first_name']} {member['last_name']}\n")
            senate_file_writer.write(f"Party: {member['party']}\n")

if __name__ == '__main__':
    # Fetch, print, and save the members of the 118th Congress
    print_and_save_current_congress_members(118)
