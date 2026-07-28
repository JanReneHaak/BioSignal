import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from src.visualization.world_map import clinical_trial_map
from PIL import Image

st.title("Welcome To BioSignal 🔬")
st.markdown("### Early-stage innovation intelligence for Life Sciences")

st.markdown(
    'Welcome To BioSignal. If not already done, check out our '
    '<a href="https://github.com/JanReneHaak/BioSignal" target="_blank">GitHub ReadMe</a>'
    ' about more information.',
    unsafe_allow_html=True
)

st.divider()

# --- Clinical Trials Map ---
st.markdown("### 🧭 Clinical Trials Radar")
st.markdown("This radar allows you to visualize clinical trials that focus on your inputed medical condition.")

col1, col2 = st.columns(2)
with col1:
    term = st.text_input("Medical Condition", value="cancer")
with col2:
    max_studies = st.slider("Number of studies", min_value=10, max_value=100, value=30, step=10)

if st.button("Fetch Trials"):
    with st.spinner("Fetching clinical trials data..."):
        fig = clinical_trial_map(term=term, max_studies=max_studies)
    if fig is not None:
        st.markdown(f"#### The {max_studies} latest clinical trials for the condition: {term.capitalize()}.")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data found for this search term.")
