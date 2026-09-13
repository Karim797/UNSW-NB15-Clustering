# UNSW-NB15 Network-Traffic Clustering

Unsupervised clustering of network-flow behaviour using preprocessing, PCA, K-Means, DBSCAN, Agglomerative Clustering, internal validation metrics, cluster profiling, and an external label check.

The attack labels are used only after clustering for interpretation; they are not model inputs.

## Deployment note

The clean run selected Agglomerative Clustering. Unlike K-Means, it has no native `predict()` method for assigning new rows. The saved bundle reproduces the analysis, but a live inference app should either use the best K-Means candidate or implement a documented cluster-assignment approximation.

## Run

Place the Parquet dataset in `data/UNSW_NB15_training-set.parquet` and run `clustering_project.ipynb` from top to bottom.

Run the interactive batch-clustering dashboard with `streamlit run app.py`. The dashboard uses K-Means because it supports a practical interactive workflow; this does not alter the notebook's Agglomerative result.
