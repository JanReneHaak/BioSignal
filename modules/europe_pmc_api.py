import requests
import pandas as pd

def fetch_publications(term="CRISPR", max_studies=100): # Set CRISPR as the standard study field and 100 studies max

    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    url = f'{base_url}?db=pubmed&term={search_term}&retmode=json&retstart={((page - 1) * 10)}&retmax=10'

    response = requests.get(url)
    data = response.json()







    df = pd.DataFrame(studies)
    return df
