# BioSignal 🔬

> **Early-stage innovation intelligence for Life Sciences — powered by open data & NLP.**

BioSignal aggregates signals from clinical trials, scientific publications and NLP-based topic modelling to help pharma, biotech and VC decision-makers spot emerging trends before they become obvious.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Development-f59e0b?style=flat-square)

---

## What is BioSignal?

Imagine a biotech company asking: *"Which therapeutic areas should we invest in over the next 5 years?"*

BioSignal answers that question by combining open data sources into one interactive dashboard. Enter a disease or therapeutic area and get three independent intelligence signals instantly:

| Signal | Source | What it reveals |
|--------|--------|-----------------|
| Clinical trial activity | ClinicalTrials.gov API v2 | Where R&D investment is flowing, by phase and geography |
| Publication volume trends | EuropePMC API | How scientific interest has evolved over the last 10 years |
| Research topic clusters | EuropePMC + BERTopic NLP | Which sub-fields within a disease area are emerging |

**Example insight:** Search "CAR-T" → see Phase I trials surging in Asia, publication volume accelerating since 2021, and BERTopic revealing that solid tumour applications and manufacturing scalability are the fastest-growing research clusters — early signal to prioritise CAR-T solid tumour partnerships.

---

## Features

### ✅ Module 1 — Clinical Trials Radar
Interactive world map of active clinical trials sourced live from ClinicalTrials.gov. Filter by trial phase (Phase 1–4) using a multiselect. Hover tooltips show trial title, sponsor, NCT ID and country.

### ✅ Module 2 — Publication Trends
Bar chart showing total indexed publications per year for the last 10 years, sourced from EuropePMC. Shows whether scientific interest in a topic is growing, plateauing or declining. Includes a list of the 10 most recent papers with direct links to EuropePMC.

### ✅ Module 3 — Research Topic Clusters
NLP pipeline using spaCy preprocessing and BERTopic topic modelling on recent abstracts. Identifies distinct research sub-fields within a disease area and ranks them by publication volume. Results are cached per search term for fast repeat queries.

### 🔜 Module 4 — Startup & Funding Monitor *(planned)*
Heatmaps of VC investment by geography and therapeutic focus using Crunchbase/Dealroom data.

### 🔜 Module 5 — Patent Snapshot *(planned)*
First-mention timelines for emerging targets via Lens.org API.

---

## Tech Stack

```
BioSignal/
├── src/
│   ├── clinical_trials_api.py      # ClinicalTrials.gov v2 API client
│   ├── europepmc_api.py            # EuropePMC abstract & count fetcher
│   ├── nlp/
│   │   ├── topic_model.py          # BERTopic pipeline with UMAP + HDBSCAN
│   │   └── preprocessing.py       # spaCy lemmatization & text cleaning
│   └── visualization/
│       ├── world_map.py            # Plotly scatter_geo map
│       ├── publication_trends.py   # Plotly bar chart
│       └── topic_chart.py         # BERTopic horizontal bar chart
├── dashboard/
│   └── app.py                      # Streamlit dashboard
├── data/                           # Cached API responses (gitignored)
├── reports/                        # Export-ready charts & summaries
├── requirements.txt
└── README.md
```

**Core dependencies:**

```txt
requests
pandas
plotly
streamlit
bertopic
spacy
sentence-transformers
umap-learn
hdbscan
scikit-learn
```

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/JanReneHaak/BioSignal
cd BioSignal

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the dashboard
streamlit run dashboard/app.py
```

### Fetch clinical trials data

```python
from src.clinical_trials_api import get_clinical_trials

# Get 50 active CRISPR trials with full location data
df = get_clinical_trials(term="CRISPR", max_studies=50)
```

### Fetch publication counts

```python
from src.europepmc_api import get_publication_counts

# Get total paper count per year for the last 10 years
df = get_publication_counts(term="GLP-1")
```

### Run topic modelling

```python
from src.europepmc_api import get_publications
from src.nlp.topic_model import get_topics
from src.nlp.preprocessing import preprocess

df = get_publications(term="CAR-T", max_results_per_year=50)
abstracts = df["Abstract"].dropna().tolist()
topic_df = get_topics(abstracts, term="CAR-T")
```

---

## Use Case: Strategic Investment Decision

**Question:** *"Where should we focus our pipeline over the next 5 years?"*

BioSignal's answer — combining three independent signals for "CAR-T":

```
Rising Phase I trial counts in solid tumour indications
+ Accelerating publication volume since 2021
+ BERTopic clusters: manufacturing scalability & solid tumour antigens growing fastest
──────────────────────────────────────────────────────────────────────────────────────
→ Signal: CAR-T is moving beyond haematology — solid tumour applications are emerging
→ Recommendation: Prioritise CAR-T solid tumour partnerships or in-licensing
```

---

## Roadmap

- [x] ClinicalTrials.gov v2 API integration
- [x] Interactive Plotly world map with phase filter
- [x] Streamlit dashboard
- [x] EuropePMC publication volume trends (10-year view)
- [x] Latest publications with direct links
- [x] BERTopic NLP pipeline on EuropePMC abstracts
- [x] spaCy preprocessing pipeline
- [x] Result caching with st.cache_data
- [ ] Startup & funding module (Crunchbase/Dealroom)
- [ ] Patent snapshot (Lens.org API)
- [ ] Streamlit Cloud deployment
- [ ] Signal synthesis — combined insight summary across all modules
- [ ] PDF export / consulting-style report

---

## Background & Motivation

Built as a portfolio project at the intersection of my background in molecular biology (M.Sc. Molecular Biosystems, Uni Magdeburg), nephrology research (Uniklinikum Erlangen / MDIBL Maine, USA) and data science (Le Wagon Bootcamp). The goal: demonstrate that life science domain knowledge + data engineering skills can generate real strategic value, the kind of analysis that usually requires expensive intelligence platforms.

---

## Contributing

Contributions welcome. Open an issue to discuss new data sources, visualisation ideas or methodology questions.

---

## License

MIT — free to use, adapt and build upon.

---

*Built by [Jan René Haak](https://linkedin.com/in/jan-rene-haak)*
*Business Development Specialist · Molecular Biology & Data Science*
