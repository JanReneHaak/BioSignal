import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from modules.clinical_trials_api import get_clinical_trials


def clinical_trial_map(term, max_studies):

    df = get_clinical_trials(term = term, max_studies = max_studies)

    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(1, 1, 1, projection = ccrs.Robinson())
    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()
    ax.stock_img()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, alpha = 0.5)
    for i in range(df.shape[0]):

        latlon = df.iloc[i].LocationGeoPoints.copy()
        lat = latlon[0].get("lat")
        lon = latlon[0].get("lon")
        study = df.iloc[i].NCTId
        # Add a red point marker
        ax.plot(lon, lat+2, marker= "v", color= "red", markersize = 7,
                transform = ccrs.Geodetic())


        # Add a label
        ax.text(lon + 2.5, lat + 2, study, transform = ccrs.Geodetic(), color = "red", size = 10)

    plt.title(f"{max_studies} Clinical Trials that deal with {term.capitalize()}.")


    return plt
