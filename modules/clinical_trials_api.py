import requests
import pandas as pd

def get_clinical_trials(term="cancer", max_studies=100, status = "ACTIVE_NOT_RECRUITING|RECRUITING|ENROLLING_BY_INVITATION"):

    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.term": term,
        "filter.overallStatus": status,
        "pageSize": max_studies,
    }

    try:
        response = requests.get(base_url, params=params)
        print(f"Status Code: {response.status_code}") # Help for debugging -> Shows the status code (200 for good response)

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return pd.DataFrame()


    # If everythings fine, the code will continue with the following:
    studies = data.get("studies", [])
    results = []

    for study in studies:
        proto = study.get("protocolSection", {})
        ident = proto.get("identificationModule", {})
        status = proto.get("statusModule", {})
        conditions = proto.get("conditionsModule", {}).get("conditions", [])
        sponsor = proto.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", "")
        locations = proto.get("contactsLocationsModule", {}).get("locations", [])

        if isinstance(locations, list):
            countries = [loc.get("country") for loc in locations if loc and loc.get("country")]
            geopoints = [loc.get("geoPoint") for loc in locations if loc and loc.get("geoPoint")]
        else:
            countries = []
            geopoints = []


        results.append({
            "NCTId": ident.get("nctId"),
            "BriefTitle": ident.get("briefTitle"),
            "StartDate": status.get("startDateStruct", {}).get("startDate"),
            "Condition": ", ".join(conditions),
            "SponsorName": sponsor,
            "LocationCountry": countries,
            "LocationGeoPoints": geopoints
        })

    return pd.DataFrame(results)
