import plotly.express as px
from src.clinical_trials_api import get_clinical_trials


def clinical_trial_map(term, max_studies, phases=None):

    df = get_clinical_trials(term=term, max_studies=max_studies)

    if df.empty:
        return None

    # Apply phase filter
    if phases:
        df = df[df["Phase"].isin(phases)]

    if df.empty:
        return None

    df["ShortTitle"] = df["BriefTitle"].str[:60] + "..."

    fig = px.scatter_geo(
        df,
        lat="Lat",
        lon="Lon",
        color="Phase",
<<<<<<< HEAD
        hover_name="ShortTitle",
        hover_data={
            "SponsorName": True,
            "NCTId": True,
            "Country": True,
            "BriefTitle": False,
            "Lat": False,
            "Lon": False,
        },
        projection="natural earth",
=======
        hover_name="BriefTitle",
        hover_data={"SponsorName": True, "NCTId": True, "Country": True, "Lat": False, "Lon": False},
        projection="natural earth"
    )

    fig.update_geos(
    visible=True, resolution=50,
    showcountries=True, countrycolor="#000000"
>>>>>>> 7c2749c626d645448e68aa71d784cd83cd617b32
    )

    return fig
