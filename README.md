# UNSW-NB15 Network-Traffic Clustering

**[Open the live Streamlit app](https://karim797-unsw-clustering.streamlit.app/)**

Unsupervised clustering of network-flow behaviour using preprocessing, PCA, K-Means, DBSCAN, Agglomerative Clustering, internal validation metrics, cluster profiling, and an external label check.

The attack labels are used only after clustering for interpretation; they are not model inputs.

## Deployment note

The clean run selected Agglomerative Clustering. Unlike K-Means, it has no native `predict()` method for assigning new rows. The interactive dashboard therefore uses K-Means and starts with a deterministic representative network-flow demo. Users can optionally replace it with UNSW-NB15-compatible CSV or Parquet data. This does not alter the notebook's Agglomerative result.

## Run

Place the Parquet dataset in `data/UNSW_NB15_training-set.parquet` and run `clustering_project.ipynb` from top to bottom.

Run the interactive dashboard locally with `streamlit run app.py`.
