const fs = require('fs');
const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config(); // Load environment variables from .env file

const FTM_API_BASE_URL = 'https://api.followthemoney.org/';

// Get the API key for FollowTheMoney API from the environment variables
const FTM_API_KEY = process.env.FOLLOWTHEMONEY_API_KEY;

const DATA_DIRECTORY = '/workspaces/project-influence-machine/data/';

// The rest of the code remains the same...


async function get_candidate_contributions(candidateName, office) {
  const endpoint = `${FTM_API_BASE_URL}/candidate.search.list`;
  const params = {
    apikey: FTM_API_KEY,
    search: candidateName,
    format: 'json',
    office: office,
  };

  try {
    const response = await axios.get(endpoint, { params, timeout: 10000 });
    const data = response.data;

    // Filter the records to find a more precise match
    const filteredRecords = data.filter((record) => {
      const recordName = `${record.first_name || ''} ${record.last_name || ''}`;
      return candidateName.toLowerCase() === recordName.toLowerCase();
    });

    return filteredRecords;
  } catch (error) {
    console.error('Error:', error.message);
    return [];
  }
}

function process_members(filename) {
  const combinedData = [];
  const fileContent = fs.readFileSync(`${DATA_DIRECTORY}/${filename}`, 'utf-8');

  const lines = fileContent.split('\n');
  for (const line of lines) {
    if (line.includes('Name:')) {
      const name = line.split('Name:')[1].trim();
      const contributions = get_candidate_contributions(name, filename.includes('senate') ? 'S' : 'H');

      if (Array.isArray(contributions)) {
        const financialContributions = contributions.reduce((sum, contribution) => sum + contribution.amount, 0);
        const memberData = {
          name: name,
          financial_contributions: financialContributions,
        };
        combinedData.push(memberData);
      }
    }
  }

  return combinedData;
}

function main() {
  // Process House members
  const houseMembers = process_members('house_member_contributions.txt');
  const houseFileContent = houseMembers
    .map((member) => `Name: ${member.name}\nFinancial Contributions: $${member.financial_contributions}\n`)
    .join('\n');

  fs.writeFileSync(`${DATA_DIRECTORY}/house_member_contributions_with_finance.txt`, houseFileContent, 'utf-8');

  // Process Senate members
  const senateMembers = process_members('senate_member_contributions.txt');
  const senateFileContent = senateMembers
    .map((member) => `Name: ${member.name}\nFinancial Contributions: $${member.financial_contributions}\n`)
    .join('\n');

  fs.writeFileSync(`${DATA_DIRECTORY}/senate_member_contributions_with_finance.txt`, senateFileContent, 'utf-8');
}

main();
