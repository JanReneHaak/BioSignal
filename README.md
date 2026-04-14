# BioSignal 🔬

> **Early-stage innovation intelligence for Life Sciences — powered by open data & NLP.**

BioSignal aggregates signals from clinical trials, scientific publications, startup funding and patent activity to help pharma, biotech and VC decision-makers spot emerging trends before they become obvious.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Development-f59e0b?style=flat-square)

---

## What is BioSignal?

Imagine a biotech company asking: *"Which therapeutic areas should we invest in over the next 5 years?"*

BioSignal answers that question by combining four open data sources into one interactive dashboard:

| Signal | Source | What it reveals |
|--------|--------|-----------------|
| Clinical trial activity | ClinicalTrials.gov API v2 | Where R&D investment is flowing |
| Publication trends | PubMed / EuropePMC | Emerging scientific consensus |
| Startup & funding data | Crunchbase / Dealroom | Where venture capital is betting |
| Patent activity | Lens.org API | Early IP moves by major players |

**Example insight:** Combining rising Phase I trial counts in cell therapy + increasing publication volume + VC funding spikes → early signal to prioritise cell therapy partnerships.

---

## Features

- **Module 1 — ClinicalTrials Radar**: Interactive world map of active studies by indication, sponsor and phase. Filter by disease area, timeframe and country.
- **Module 2 — Research Trend Detection**: NLP-based topic modelling (BERTopic) on PubMed abstracts. Visualises topic emergence over time and co-occurrence networks.
- **Module 3 — Startup & Funding Monitor**: Heatmaps of VC investment by geography and therapeutic focus. Tracks funding waves.
- **Module 4 — Patent Snapshot** *(in progress)*: First-mention timelines for emerging targets; patent activity by company and technology.

---

## Tech Stack

```
biosignal/
├── src/
│   ├── clinical_trials_api.py   # ClinicalTrials.gov v2 API client
│   ├── pubmed_api.py            # PubMed / EuropePMC fetcher
│   ├── nlp/
│   │   ├── topic_model.py       # BERTopic pipeline
│   │   └── preprocessing.py    # spaCy text cleaning
│   └── utils.py
├── dashboard/
│   └── app.py                   # Streamlit multi-page app
├── notebooks/
│   ├── clinical_trials_exploration.ipynb
│   └── topic_modelling_pubmed.ipynb
├── data/                        # Cached API responses (gitignored)
├── reports/                     # Export-ready charts & summaries
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
cartopy
```

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/JanReneHaak/BioSignal
cd biosignal

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the dashboard
streamlit run dashboard/app.py
```

### Fetch clinical trials data

```python
from src.clinical_trials_api import fetch_clinical_trials

# Get 50 active CRISPR trials with full location data
df = fetch_clinical_trials(term="CRISPR", max_studies=50)
```

---

## Example Output

### Clinical Trials World Map
Active studies plotted by geographic location, coloured by trial phase. Hover for sponsor name, indication and NCT ID.

### Topic Emergence Over Time
Line chart showing paper volume per topic cluster (e.g. mRNA vaccines, CAR-T, GLP-1 agonists) from 2015 to present.

### Funding Heatmap
VC investment in Life Science startups by country and therapeutic focus — updated from Crunchbase CSV exports.

---

## Use Case: Strategic Investment Decision

**Client:** Mid-sized biotech company
**Question:** *"Where should we focus our pipeline over the next 5 years?"*

BioSignal's answer — combining three independent signals:

```
Rising Phase I trial counts in cell therapy
+ Accelerating publication volume (BERTopic cluster growth)
+ Increased Series A funding in cell therapy startups
─────────────────────────────────────────────────────────
→ Recommendation: Prioritise cell therapy partnerships or in-licensing
```

---

## Roadmap

- [x] ClinicalTrials.gov v2 API integration
- [x] Interactive Plotly world map
- [ ] Streamlit multi-page dashboard
- [ ] BERTopic NLP pipeline on PubMed abstracts
- [ ] Startup & funding module (Crunchbase CSV)
- [ ] Patent snapshot (Lens.org API)
- [ ] Streamlit Cloud deployment
- [ ] PDF export / consulting-style report

---

## Background & Motivation

Built as a portfolio project at the intersection of my background in molecular biology (M.Sc. Molecular Biosystems, Uni Magdeburg), nephrology research (Uniklinikum Erlangen / MDIBL Maine, USA) and data science (Le Wagon Bootcamp). The goal: demonstrate that life science domain knowledge + data engineering skills can generate real strategic value — the kind of analysis that usually requires expensive intelligence platforms.

---

## Contributing

Contributions welcome. Open an issue to discuss new data sources, visualisation ideas or methodology questions.

---

## License

MIT — free to use, adapt and build upon.

---

*Built by Jan René Haak(https://linkedin.com/in/jan-rene-haak)*
*Business Relation Development*
*Molecular Biology & Data Science*
