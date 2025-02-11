import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_expasy_peptide_mass(protein_name: str, min_mass: float = 500, max_mass: float = 3500, enzyme: str = "Trypsin") -> pd.DataFrame:
    """
    Fetch peptide mass data from Expasy PeptideMass service.

    Args:
        protein_name (str): Name of the protein.
        min_mass (float, optional): Minimum mass of peptides. Defaults to 500.
        max_mass (float, optional): Maximum mass of peptides. Defaults to 3500.
        enzyme (str, optional): Enzyme used for digestion. Defaults to "Trypsin".

    Returns:
        pd.DataFrame: DataFrame containing peptide mass, position and sequence.
    """
    # Define the URL for the Expasy PeptideMass service
    url = "https://web.expasy.org/cgi-bin/peptide_mass/peptide-mass.pl"

    # Define the parameters for the PeptideMass service
    params = {
        "protein": protein_name,
        "reagents": "nothing+(in+reduced+form)",
        "mplus": "mh",
        "masses": "monoisotopic",
        "enzyme": enzyme,
        "MC": "0",
        "minmass": str(min_mass),
        "maxmass": str(max_mass),
        "order": "mass"
    }

    # Send a GET request to the Expasy PeptideMass service
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with class "type-1"
        table = soup.find('table', {'class': 'type-1'})

        # Extract the table rows
        rows = table.find_all('tr')

        # Extract the table headers
        headers = [header.text for header in rows[0].find_all('th')]

        # Extract the table data
        data = []
        for row in rows[1:]:
            cells = row.find_all('td')
            data.append([cell.text for cell in cells])

        # Create a DataFrame from the data
        df = pd.DataFrame(data=data, columns=headers)

        return df
    else:
        print(f"Error: {response.status_code}")
        return None