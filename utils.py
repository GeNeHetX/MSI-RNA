import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

def get_url(url, **kwargs):
    """
    Send a GET request to a given URL and return the response.
    
    Args:
        url (str): URL to send the GET request to.
        **kwargs: Additional keyword arguments to pass to requests.get.
        
    Returns:
        requests.models.Response: Response object.
    """
    response = requests.get(url, **kwargs);

    if not response.ok:
        print(response.text)
        response.raise_for_status()
        sys.exit()

    return response


def get_uniprotkbid(gene_name: str, taxonomy_id: int = 9606, reviewed: bool = True) -> list[str]:
    """
    Get a list of UniProtKB IDs for a given gene name.

    Args:
        gene_name (str): Gene name.
        taxonomy_id (int, optional): Taxonomy ID. Defaults to 9606 Homo sapiens (Human).
        reviewed (bool, optional): Consider only reviewed entries. Defaults to True.

    Returns:
        list[str]: List of UniProtKB IDs.
    """
    # Query parameters
    website = "https://rest.uniprot.org/uniprotkb"
    reviewed = " AND (reviewed:true)" if reviewed else ""

    # Run a search query for a protein
    response = get_url(f"{website}/search?query=(gene:{gene_name}) AND (taxonomy_id:{taxonomy_id}){reviewed}&fields=id&size=100")

    # # Store the protein names
    protein_names = [entry["uniProtkbId"] for entry in response.json()["results"]]

    return protein_names


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
    response = get_url(url, params=params)

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