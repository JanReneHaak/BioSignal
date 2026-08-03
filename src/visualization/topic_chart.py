import plotly.express as px
from src.europepmc_api import get_publications
from src.nlp.topic_model import get_topics


def topic_chart(term="cancer"):

    df = get_publications(term=term, max_results_per_year=50)

    if df.empty:
        return None

    abstracts = df["Abstract"].dropna().tolist()

    if len(abstracts) < 20:
        print(f"Too few abstracts ({len(abstracts)}) for topic modelling.")
        return None

    topic_df = get_topics(abstracts, term=term)

    if topic_df.empty:
        return None

    topic_df = topic_df.sort_values("Count", ascending=True)

    fig = px.bar(
        topic_df,
        x="Count",
        y="Label",
        orientation="h",
        color="Count",
        color_continuous_scale="balance",
        labels={"Count": "Number of Abstracts", "Label": "Research Topic"},
    )

    fig.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(tickfont=dict(size=12)),
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return fig
