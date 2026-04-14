from src.visualization.world_map import clinical_trial_map

fig = clinical_trial_map(term="cancer", max_studies=50)
fig.show()  # opens in your browser automatically
