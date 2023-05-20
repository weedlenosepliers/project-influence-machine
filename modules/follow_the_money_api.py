"""
This module provides functions to combine and retrieve financial contributions of members of Congress.
"""
import os
import requests

from .env_loader import get_followthemoney_api_key

# Define the API endpoints
FTM_API_BASE_URL = 'https://api.followthemoney.org/'

# Set the API key for FollowTheMoney API
FTM_API_KEY = get_followthemoney_api_key()

DATA_DIRECTORY = "/workspaces/project-influence-machine/data/"

def get_candidate_contributions(candidate_name, office):
    endpoint = f"{FTM_API_BASE_URL}/candidate.search.list"
    params = {
        'apikey': FTM_API_KEY,
        'search': candidate_name,
        'format': 'json',
        'office': office
    }

    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        data = response.json()

        # Filter the records to find a more precise match
        filtered_records = []
        for record in data:
            record_name = f"{record.get('first_name', '')} {record.get('last_name', '')}"
            if candidate_name.lower() in record_name.lower():
                filtered_records.append(record)

        return filtered_records

    except requests.exceptions.RequestException as ex:
        print('Error:', ex)

    return []

def process_members(filename):
    combined_data = []
    with open(os.path.join(DATA_DIRECTORY, filename), 'r') as file:
        for line in file:
            # Extract only the name line from the file
            if 'Name:' in line:
                name = line.split('Name:')[1].strip()
                contributions = get_candidate_contributions(name, 'S' if 'senate' in filename else 'H')
                member_data = {
                    'name': name,
                    'financial_contributions': sum([contribution['amount'] for contribution in contributions])
                }
                combined_data.append(member_data)
    return combined_data

def main():
    # Process House members
    house_members = process_members('house_member_contributions.txt')
    with open(os.path.join(DATA_DIRECTORY, 'house_member_contributions_with_finance.txt'), 'w', encoding='utf-8') as file:
        for member in house_members:
            file.write(f"Name: {member['name']}\n")
            file.write(f"Financial Contributions: ${member['financial_contributions']}\n")
            file.write("\n")

    # Process Senate members
    senate_members = process_members('senate_member_contributions.txt')
    with open(os.path.join(DATA_DIRECTORY, 'senate_member_contributions_with_finance.txt'), 'w', encoding='utf-8') as file:
        for member in senate_members:
            file.write(f"Name: {member['name']}\n")
            file.write(f"Financial Contributions: ${member['financial_contributions']}\n")
            file.write("\n")

if __name__ == '__main__':
    main()
