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


    # If everythings fine, the code will continue with the following:
    studies = data.get("studies", [])
    results = []

    for study in studies:
        proto = study.get("protocolSection", {})
        ident = proto.get("identificationModule", {})
        status_module = proto.get("statusModule", {})
        phases = proto.get("designModule", {}).get("phases", [])
        phase = phases[0] if phases else "Unknown"
        conditions = proto.get("conditionsModule", {}).get("conditions", [])
        sponsor = proto.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", "")
        locations = proto.get("contactsLocationsModule", {}).get("locations", [])

        for loc in locations:
            geopoint = loc.get("geoPoint")
            if not geopoint:  # skip if geoPoint is None or missing
                continue


            results.append({
                "NCTId": ident.get("nctId"),
                "BriefTitle": ident.get("briefTitle"),
                "Condition": ", ".join(conditions),
                "SponsorName": sponsor,
                "Phase": phase,
                "Country": loc.get("country"),
                "Lat": geopoint.get("lat"),
                "Lon": geopoint.get("lon"),
            })


    if not results:
        print(f"No studies found for term='{term}'.")
        return pd.DataFrame()

    return pd.DataFrame(results)
