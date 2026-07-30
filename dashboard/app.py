import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.visualization.world_map import clinical_trial_map
from src.visualization.publication_trends import publication_volume_chart
from src.europepmc_api import get_publications

# --- Page Config ---
st.set_page_config(
    page_title="BioSignal",
    page_icon="🔬",
    layout="wide"
)

# --- Header ---
st.title("BioSignal 🔬")
st.markdown("##### Early-stage innovation intelligence for Life Sciences")
st.markdown(
    'Enter a disease or therapeutic area to explore the full research landscape — '
    'active clinical trials, publication trends and the latest science. '
    'Data from [ClinicalTrials.gov](https://clinicaltrials.gov) & [EuropePMC](https://europepmc.org). '
    'Learn more on [GitHub](https://github.com/JanReneHaak/BioSignal).'
)

st.divider()

# --- Single Search Bar ---
col1, col2 = st.columns([3, 1])
with col1:
    disease = st.text_input(
        "Disease or therapeutic area",
        value=None,
        label_visibility="collapsed",
        placeholder="e.g. cancer, GLP-1, CAR-T, Alzheimer's"
    )
with col2:
    search = st.button("🔍 Explore", use_container_width=True)

# --- Phase Filter ---
all_phases = ["PHASE1", "PHASE2", "PHASE3", "PHASE4", "NA", "Unknown"]
place_holder = "Select the phase(s) of the trials you would like to be displayed!"
selected_phases = st.multiselect(
    "Filter by trial phase",
    options=all_phases,
    default=None,
    placeholder=place_holder
)

st.divider()

if search:

    if not disease:
        st.warning("Please enter a disease or therapeutic area first.")
        st.stop()
    if not selected_phases:
        st.warning("Please select at least one trial phase.")
        st.stop()

    # --- Clinical Trials Map ---
    st.markdown("### 🧭 Clinical Trials Radar")
    st.caption(f"Active clinical trials for **{disease}**, filtered by selected phases.")

    with st.spinner("Fetching clinical trials..."):
        fig_map = clinical_trial_map(term=disease, max_studies=100, phases=selected_phases)

    if fig_map is not None:
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption("💡 Hover over a point to see trial details. Colour indicates trial phase.")
    else:
        st.warning("No clinical trial data found.")

    st.divider()

    # --- Trend + Publications side by side ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📈 Publication Trends")
        st.caption(f"Total indexed publications per year for **{disease}**.")

        with st.spinner("Fetching publication trends..."):
            fig_pubs = publication_volume_chart(term=disease)

        if fig_pubs is not None:
            st.plotly_chart(fig_pubs, use_container_width=True)
        else:
            st.warning("No publication data found.")

    with col_right:
        st.markdown("### 📄 Latest Publications")
        st.caption(f"10 most recent papers on **{disease}** indexed in EuropePMC.")

        with st.spinner("Fetching latest publications..."):
            df_pubs = get_publications(term=disease, max_results_per_year=5)
            df_latest = (
                df_pubs
                .dropna(subset=["Year"])
                .sort_values("Year", ascending=False)
                .head(10)
            )

        if not df_latest.empty:
            for _, row in df_latest.iterrows():
                journal = row['Journal'] if row['Journal'] else "Journal not available"
                st.markdown(
                    f"**{row['Title']}**  \n"
                    f"_{journal}_ · {int(row['Year'])}  \n"
                    f"[View on EuropePMC](https://europepmc.org/search?query={row['PMID']})"
                    )
                st.markdown("---")
        else:
            st.warning("No publications found.")

st.divider()
st.caption("Built by Jan René Haak · Molecular Biology & Data Science · [LinkedIn](https://linkedin.com/in/jan-rene-haak)")
