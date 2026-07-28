import plotly.express as px
from src.clinical_trials_api import get_clinical_trials


def clinical_trial_map(term, max_studies):

    df = get_clinical_trials(term = term, max_studies = max_studies)


    if df.empty:
        print("No data to plot.")
        return None

    fig = px.scatter_geo(
        df,
        lat="Lat",
        lon="Lon",
        color="Phase",
        hover_name="BriefTitle",
        hover_data={"SponsorName": True, "NCTId": True, "Country": True, "Lat": False, "Lon": False},
        projection="natural earth"
    )

    fig.update_geos(
    visible=True, resolution=50,
    showcountries=True, countrycolor="#000000"
    )

    return fig
