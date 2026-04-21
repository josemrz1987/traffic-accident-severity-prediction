import json
import streamlit as st
import pandas as pd
from catboost import CatBoostClassifier

MODEL_PATH = "catboost_model.cbm"
CATS_PATH  = "categories.json"

FEATURES = [
    "Agency Name","Route Type","Road Name","Cross-Street Name","Collision Type",
    "Weather","Surface Condition","Light","Traffic Control",
    "Vehicle Body Type","Vehicle Movement","Vehicle Going Dir",
    "Vehicle Make","multiple_crash","time_of_day","month","weekend",
    "Speed Limit Group","Vehicle Age","geo_cluster"
]

# numéricas (según tu df final)
NUM_INT   = {"month", "weekend", "multiple_crash"}
NUM_FLOAT = {"Vehicle Age"}

st.set_page_config(page_title="112 Triaje", page_icon="🚑", layout="wide")

@st.cache_resource
def load_model(path: str):
    m = CatBoostClassifier()
    m.load_model(path)
    return m

@st.cache_data
def load_categories(path: str):
    with open(path, "r") as f:
        return json.load(f)

model = load_model(MODEL_PATH)
cat_dict = load_categories(CATS_PATH)

st.title("🚑 112: Triaje de severidad (Injury/Fatal)")
st.write("Selecciona los datos del accidente y obtén la probabilidad estimada de lesión/fatalidad (y=1).")

thr = st.sidebar.slider("Umbral de decisión", 0.05, 0.95, 0.54, 0.01)

colA, colB, colC = st.columns(3)
row = {}

# ---------- Inputs ----------
for i, f in enumerate(FEATURES):
    container = [colA, colB, colC][i % 3]

    with container:
        if f in NUM_INT:
            if f == "month":
                row[f] = int(st.number_input("month", min_value=1, max_value=12, value=6))
            elif f == "weekend":
                row[f] = int(st.selectbox("weekend", [0, 1], index=0))
            elif f == "multiple_crash":
                row[f] = int(st.selectbox("multiple_crash (>=3 vehículos)", [0, 1], index=0))

        elif f in NUM_FLOAT:
            row[f] = float(
                st.number_input("Vehicle Age", min_value=0.0, max_value=120.0, value=10.0, step=1.0)
            )

        else:
            options = cat_dict.get(f)
            if not options:
                options = ["UNKNOWN"]

            default_idx = options.index("UNKNOWN") if "UNKNOWN" in options else 0
            row[f] = st.selectbox(f, options=options, index=default_idx)

X_one = pd.DataFrame([row], columns=FEATURES)

st.subheader("📌 Entrada")
st.dataframe(X_one, use_container_width=True)

if st.button("🔮 Predecir"):
    proba = float(model.predict_proba(X_one)[0, 1])
    pred = int(proba >= thr)

    st.subheader("✅ Resultado")
    st.metric("Probabilidad Injury/Fatal (y=1)", f"{proba*100:.1f}%")
    st.write(f"**Decisión (umbral={thr:.2f})**: {'🟥 Injury/Fatal' if pred==1 else '🟩 Property Damage'}")
