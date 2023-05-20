"""
Fetches members from the ProPublica Congress API and combines them with financial data.

Prints the combined data for House and Senate members and outputs the list of members
along with their respective financial contributions.
"""
import os
import requests
import legis_api


# Function to retrieve secret value from environment variables
def get_secret_value(secret_name):
    """
    Retrieve the value of a secret from environment variables.

    Args:
        secret_name (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable.
    """
    return os.getenv(secret_name, '')

# Get the API key for the ProPublica Campaign Finance API from environment variables
FINANCE_API_KEY = get_secret_value('PROPUBLICA_CAMPAIGN_FINANCE_API')

# Define the API endpoint for financial data from the ProPublica Campaign Finance API
FIN_API_BASE_URL = 'https://api.propublica.org/campaign-finance/v1/'
FIN_ENDPOINT = 'candidates/{fec_candidate_id}/totals.json'

# Set the request headers for the ProPublica Campaign Finance API
finance_headers = {
    'X-API-Key': FINANCE_API_KEY
}

def fetch_financial_data(member):
    """
    Fetch financial data for a member from the ProPublica Campaign Finance API.

    Args:
        member (dict): The member object.

    Returns:
        float: The total financial donations for the member.
    """
    congress_number = member.get('congress', member.get('congress_number'))
    member_id = member.get('id')
    fec_candidate_id = member.get('fec_candidate_id')

    if not congress_number or not member_id or not fec_candidate_id:
        print(f"Incomplete member information: {member}")
        return 0

    endpoint = f"{FIN_API_BASE_URL}{FIN_ENDPOINT.format(fec_candidate_id=fec_candidate_id)}"
    try:
        response = requests.get(endpoint, headers=finance_headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            if len(results) > 0:
                total_donations = results[0]['total_contributions']
                return total_donations
            else:
                print(f"No financial data found for member: {member_id}")
                return 0
        else:
            print(f"Failed to fetch financial data for member: {member_id}")
            return 0
    except requests.exceptions.RequestException as ex:
        print('Error:', ex)
        return 0

def combine_member_data(members):
    """
    Combines member data with financial data.

    Args:
        members (list): The list of member objects.

    Returns:
        list: The list of member objects with financial data.
    """
    combined_data = []
    for member in members:
        financial_donations = fetch_financial_data(member)
        member['financial_donations'] = financial_donations
        combined_data.append(member)
    return combined_data

def main():
    """
    Fetches members from the ProPublica Congress API and combines them with financial data.

    Prints the combined data for House and Senate members and outputs the list of members
    along with their respective financial contributions.
    """
    congress_number = 117  # Example: Fetch data for Congress number 117

    house_members = legis_api.get_members(congress_number, chamber='house')  # Specify 'house' chamber
    combined_house_data = combine_member_data(house_members)

    print("House Members:")
    for member in combined_house_data[:10]:  # Displaying the first 10 members
        print(f"First Name: {member['first_name']}")
        print(f"Last Name: {member['last_name']}")
        print(f"Party: {member.get('party', 'N/A')}")
        print(f"State: {member['state']}")
        print(f"Financial Donations: ${member['financial_donations']}")
        print("")

    # Output the list of House members and their contributions
    with open("house_member_contributions.txt", 'w', encoding='utf-8') as file:
        for member in combined_house_data:
            file.write(f"First Name: {member['first_name']}\n")
            file.write(f"Last Name: {member['last_name']}\n")
            file.write(f"Party: {member.get('party', 'N/A')}\n")
            file.write(f"State: {member['state']}\n")
            file.write(f"Financial Donations: ${member['financial_donations']}\n")
            file.write("\n")

    senate_members = legis_api.get_members(congress_number, chamber='senate')  # Specify 'senate' chamber
    combined_senate_data = combine_member_data(senate_members)

    print("Senate Members:")
    for member in combined_senate_data[:10]:  # Displaying the first 10 members
        print(f"First Name: {member['first_name']}")
        print(f"Last Name: {member['last_name']}")
        print(f"Party: {member.get('party', 'N/A')}")
        print(f"State: {member['state']}")
        print(f"Financial Donations: ${member['financial_donations']}")
        print("")

    # Output the list of Senate members and their contributions
    with open("senate_member_contributions.txt", 'w', encoding='utf-8') as file:
        for member in combined_senate_data:
            file.write(f"First Name: {member['first_name']}\n")
            file.write(f"Last Name: {member['last_name']}\n")
            file.write(f"Party: {member.get('party', 'N/A')}\n")
            file.write(f"State: {member['state']}\n")
            file.write(f"Financial Donations: ${member['financial_donations']}\n")
            file.write("\n")

if __name__ == '__main__':
    main()
