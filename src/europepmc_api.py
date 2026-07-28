import requests
import pandas as pd
from datetime import datetime

import requests
import pandas as pd
from datetime import datetime


def get_publication_counts(term="cancer"):
    """Fetch total publication count per year from EuropePMC — no abstract download needed."""

    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    current_year = datetime.now().year
    years = range(current_year - 10, current_year + 1)

    results = []

    for year in years:
        query = f"{term} AND (FIRST_PDATE:[{year}-01-01 TO {year}-12-31])"
        params = {
            "query": query,
            "format": "json",
            "pageSize": 1,        # we only need the hitCount, not the papers
            "resultType": "lite", # lite is faster, we don't need abstracts here
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error {response.status_code}: {e}")
            continue
        except requests.exceptions.ConnectionError:
            print("No internet connection or API unreachable.")
            break
        except requests.exceptions.Timeout:
            print(f"Timeout for year {year}, skipping.")
            continue

        hit_count = data.get("hitCount", 0)
        results.append({"Year": year, "PaperCount": hit_count})

    return pd.DataFrame(results)


def get_publications(term="cancer", max_results_per_year=20):
    """Fetch abstracts for NLP/BERTopic — keeps the per-year sampling approach."""

    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    current_year = datetime.now().year
    years = range(current_year - 10, current_year + 1)

    all_results = []

    for year in years:
        query = f"{term} AND (FIRST_PDATE:[{year}-01-01 TO {year}-12-31])"
        params = {
            "query": query,
            "format": "json",
            "pageSize": max_results_per_year,
            "resultType": "core",
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error {response.status_code}: {e}")
            continue
        except requests.exceptions.ConnectionError:
            print("No internet connection or API unreachable.")
            break
        except requests.exceptions.Timeout:
            print(f"Timeout for year {year}, skipping.")
            continue

        articles = data.get("resultList", {}).get("result", [])

        for article in articles:
            all_results.append({
                "PMID": article.get("pmid"),
                "Title": article.get("title"),
                "Abstract": article.get("abstractText"),
                "Year": article.get("pubYear"),
                "Journal": article.get("journalTitle"),
                "CitedBy": article.get("citedByCount", 0),
            })

    if not all_results:
        print(f"No publications found for term='{term}'.")
        return pd.DataFrame()

    df = pd.DataFrame(all_results)
    df = df.dropna(subset=["Abstract"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    return df
