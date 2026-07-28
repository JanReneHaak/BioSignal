import requests
import pandas as pd

def get_publications(term="cancer", max_results=100):

    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": term,
        "format": "json",
        "pageSize": max_results,
        "resultType": "core",  # includes abstracts
        "sort": "CITED desc",  # most cited first
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error {response.status_code}: {e}")
        return pd.DataFrame()
    except requests.exceptions.ConnectionError:
        print("No internet connection or API unreachable.")
        return pd.DataFrame()
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return pd.DataFrame()

    articles = data.get("resultList", {}).get("result", [])

    if not articles:
        print(f"No publications found for term='{term}'.")
        return pd.DataFrame()

    results = []
    for article in articles:
        results.append({
            "PMID": article.get("pmid"),
            "Title": article.get("title"),
            "Abstract": article.get("abstractText"),
            "Year": article.get("pubYear"),
            "Journal": article.get("journalTitle"),
            "CitedBy": article.get("citedByCount", 0),
        })

    df = pd.DataFrame(results)
    df = df.dropna(subset=["Abstract"])  # drop rows without abstracts
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    return df
