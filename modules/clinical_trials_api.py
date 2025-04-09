import requests
import pandas as pd

def fetch_clinical_trials(term="CRISPR", max_studies=100): # Set CRISPR as the standard study field and 100 studies max

    base_url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": term,
        "fields": "NCTId,Condition,BriefTitle,Phase,StudyType,StartDate,LocationCountry,SponsorName",
        "min_rnk": 1,
        "max_rnk": max_studies,
        "fmt": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    studies = data["StudyFieldsResponse"]["StudyFields"]

    df = pd.DataFrame(studies)
    return df
