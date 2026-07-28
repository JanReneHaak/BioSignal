import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.visualization.world_map import clinical_trial_map
from src.visualization.publication_trends import publication_volume_chart

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
    'Explore active clinical trials and research publication trends worldwide. '
    'Data sourced live from [ClinicalTrials.gov](https://clinicaltrials.gov) and [EuropePMC](https://europepmc.org). '
    'Learn more on [GitHub](https://github.com/JanReneHaak/BioSignal).'
)

st.divider()

# --- Clinical Trials Radar ---
st.markdown("### 🧭 Clinical Trials Radar")
st.caption("Search a medical condition to visualise where trials are running globally, coloured by phase.")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    term = st.text_input("Medical Condition", value="cancer", label_visibility="collapsed", placeholder="Enter a condition e.g. diabetes, CRISPR, GLP-1")
with col2:
    max_studies = st.slider("Number of studies", min_value=10, max_value=100, value=30, step=10)
with col3:
    fetch_trials = st.button("🔍 Fetch Trials", use_container_width=True)

if fetch_trials:
    with st.spinner(f"Fetching {max_studies} trials for '{term}'..."):
        fig_map = clinical_trial_map(term=term, max_studies=max_studies)

    if fig_map is not None:
        st.success(f"Showing {max_studies} clinical trials for **{term.capitalize()}**")
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption("💡 Hover over a point to see trial details. Colour indicates trial phase.")
    else:
        st.warning("No data found. Try a different search term.")

st.divider()

# --- Publication Trends ---
st.markdown("### 📈 Research Publication Trends")
st.caption("Track how scientific interest in a topic has evolved over the last 10 years.")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    pub_term = st.text_input("Research topic", value="GLP-1", label_visibility="collapsed", placeholder="Enter a topic e.g. GLP-1, CAR-T, mRNA", key="pub_term")
with col2:
    st.empty()  # placeholder to keep layout consistent with the map section
with col3:
    fetch_pubs = st.button("📊 Fetch Trends", use_container_width=True)

if fetch_pubs:
    with st.spinner(f"Fetching publication counts for '{pub_term}'..."):
        fig_pubs = publication_volume_chart(term=pub_term)

    if fig_pubs is not None:
        st.success(f"Showing publication volume for **{pub_term}** over the last 10 years")
        st.plotly_chart(fig_pubs, use_container_width=True)
        st.caption("💡 Data sourced from EuropePMC. Count reflects total indexed publications per year.")
    else:
        st.warning("No data found. Try a different search term.")

st.divider()
st.caption("Built by Jan René Haak · Molecular Biology & Data Science · [LinkedIn](https://linkedin.com/in/jan-rene-haak)")
