import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


st.set_page_config(page_title="Network Traffic Clustering", page_icon="🌐")
st.title("UNSW-NB15 Network-Traffic Clustering")
st.caption("Explore the built-in demo immediately, or upload UNSW-NB15-compatible data.")


@st.cache_data
def make_demo_data(rows=2_000):
    rng = np.random.default_rng(42)
    traffic_type = rng.choice(3, rows, p=[0.45, 0.35, 0.20])
    scale = np.choose(traffic_type, [1.0, 3.0, 0.35])
    spkts = np.maximum(2, rng.poisson(8 * scale)).astype(int)
    dpkts = np.maximum(1, rng.poisson(6 * scale)).astype(int)
    duration = rng.lognormal(-1.2 + traffic_type * 0.7, 0.9)
    sbytes = np.maximum(spkts * rng.lognormal(4.2 + traffic_type * 0.35, 0.7), 40).astype(int)
    dbytes = np.maximum(dpkts * rng.lognormal(4.0 + traffic_type * 0.45, 0.8), 40).astype(int)
    return pd.DataFrame({
        "dur": duration,
        "proto": np.choose(traffic_type, ["tcp", "udp", "icmp"]),
        "service": rng.choice(["-", "http", "dns", "ftp", "smtp"], rows),
        "state": np.choose(traffic_type, ["FIN", "CON", "INT"]),
        "spkts": spkts,
        "dpkts": dpkts,
        "sbytes": sbytes,
        "dbytes": dbytes,
        "rate": (spkts + dpkts) / np.maximum(duration, 1e-3),
        "sload": sbytes * 8 / np.maximum(duration, 1e-3),
        "dload": dbytes * 8 / np.maximum(duration, 1e-3),
        "sinpkt": duration * 1_000 / spkts,
        "dinpkt": duration * 1_000 / dpkts,
        "smean": sbytes / spkts,
        "dmean": dbytes / dpkts,
    })


uploaded = st.file_uploader("Optional network-flow dataset", type=["csv", "parquet"])

if uploaded is None:
    data = make_demo_data()
    st.success("Using 2,000 built-in representative network-flow rows. Upload a file to replace them.")
else:
    data = pd.read_parquet(uploaded) if uploaded.name.lower().endswith(".parquet") else pd.read_csv(uploaded)
    st.success(f"Using your uploaded dataset ({len(data):,} rows).")
if len(data) > 10_000:
    data = data.sample(10_000, random_state=42).reset_index(drop=True)
    st.info("A reproducible 10,000-row sample is used to keep the interactive app responsive.")
drop_columns = [c for c in ["id", "label", "attack_cat", "attack_label", "attack_category"] if c in data]
X = data.drop(columns=drop_columns).replace([np.inf, -np.inf], np.nan).dropna(axis=1)
categorical = X.select_dtypes(include=["object", "category"]).columns.tolist()
numerical = X.select_dtypes(include=np.number).columns.tolist()

preprocess = ColumnTransformer([
    ("num", StandardScaler(), numerical),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])
k = st.slider("Number of clusters", 2, 10, 4)
processed = preprocess.fit_transform(X)
pca_components = min(10, processed.shape[0] - 1, processed.shape[1])
pca = PCA(n_components=pca_components, random_state=42)
reduced = pca.fit_transform(processed.toarray() if hasattr(processed, "toarray") else processed)
labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(reduced)

result = data.copy()
result["cluster"] = labels
st.subheader("Cluster sizes")
st.bar_chart(result["cluster"].value_counts().sort_index())
if reduced.shape[1] >= 2:
    chart = pd.DataFrame({"PC1": reduced[:, 0], "PC2": reduced[:, 1], "cluster": labels.astype(str)})
    st.scatter_chart(chart, x="PC1", y="PC2", color="cluster")
st.dataframe(result.head(500))
st.download_button("Download clustered data", result.to_csv(index=False), "clustered_network_traffic.csv", "text/csv")
