import requests
import pandas as pd

def fetch_publications(term="CRISPR", max_studies=100): # Set CRISPR as the standard study field and 100 studies max

    base_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
    url = f'{base_url}?query={term}%20sort_date:y&format=json&resultType=core'

    response = requests.get(url)
    data = response.json()








    df = pd.DataFrame(studies)
    return df
