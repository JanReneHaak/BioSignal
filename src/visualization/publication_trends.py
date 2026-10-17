import plotly.express as px
import pandas as pd
from datetime import datetime
from src.europepmc_api import get_publication_counts

def publication_volume_chart(term="cancer", year_lower=datetime.now().year-10, year_upper=datetime.now().year):

    df = get_publication_counts(term=term, year_lower=year_lower, year_upper=year_upper)

    if df.empty:
        return None

    fig = px.bar(
        df,
        x="Year",
        y="PaperCount",
        labels={"PaperCount": "Number of Publications", "Year": "Year"},
        color="PaperCount",
        color_continuous_scale="balance",
    )

    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(tickmode="linear", dtick=1),
    )

    return fig
