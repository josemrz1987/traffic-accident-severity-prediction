# Traffic Accident Severity Prediction
### Early-stage triage support tool using Machine Learning

Master's Thesis — MSc Data Science, Big Data & Business Analytics  
Universidad Complutense de Madrid · 2025–2026  
Author: Jose Manuel Ríos Zorrilla

---

## Overview

Binary classification model to predict whether a traffic accident will result in **physical injuries or fatalities** (vs. material damage only), using only information available at the time of the initial report — before any post-accident assessment.

Designed as a decision-support tool for emergency triage: helping dispatchers prioritize ambulance vs. roadside assistance when information is still limited.

---

## Dataset

- **Source:** Maryland ACRS (Automated Crash Reporting System) — [data.gov](https://catalog.data.gov/dataset/crash-reporting-drivers-data)
- **Snapshot:** October 2025
- **Task:** Binary classification — `y=1` (Injury/Fatal) vs. `y=0` (Property Damage)
- **Class distribution:** ~64% material damage / ~36% physical injury

---

## Methodology highlights

- Explicit exclusion of **data leakage variables** (post-accident assessments) to ensure realistic inference at notification time
- Structured variable typology (quality issues, leakage risk, administrative, high cardinality)
- Feature engineering: `geo_cluster`, `time_of_day`, `multiple_crash`, `vehicle_age`, `speed_limit_group`, `weekend`, `month`
- Model comparison: LightGBM, XGBoost, **CatBoost** (selected)
- **Decision threshold optimization** (recommended threshold: 0.54) to balance recall on the positive class vs. operational false alarm rate
- **SHAP interpretability**: global feature importance, beeswarm, waterfall, and dependence plots

---

## Results

| Model | Threshold | Precision (pos) | Recall (pos) | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|
| CatBoost | 0.50 | 0.481 | 0.735 | 0.697 | 0.543 |
| XGBoost | 0.50 | 0.488 | 0.675 | 0.690 | 0.535 |
| LightGBM | 0.50 | 0.491 | 0.664 | 0.690 | 0.536 |

> The ROC-AUC of ~0.69 is a deliberate result of excluding leakage variables. Retaining post-accident fields would inflate performance but make the model unusable in a real early-notification scenario.

---

## Stack

![Python](https://img.shields.io/badge/Python-3.10-blue)
![CatBoost](https://img.shields.io/badge/CatBoost-gradient%20boosting-yellow)
![SHAP](https://img.shields.io/badge/SHAP-interpretability-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-app-red)

- **Modeling:** CatBoost, XGBoost, LightGBM, Scikit-learn
- **Interpretability:** SHAP
- **App:** Streamlit
- **Environment:** Google Colab

---

## Repository structure

```
├── notebook/          # Main analysis notebook (EDA, modeling, SHAP)
├── app/               # Streamlit application
├── model/             # Persisted CatBoost model (.cbm) + preprocessing artifacts
├── data/              # Data snapshot (October 2025) —  https://catalog.data.gov/dataset/crash-reporting-drivers-data
└── memoria/           # Full thesis document (PDF, Spanish)
```

---

## How to run the app

```bash
pip install -r requirements.txt
streamlit run app/app.py

---

## Notes

This project was developed in Spanish as an academic Master's thesis. Code comments, variable names, and the full thesis document (PDF) are in Spanish.

---

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — Free to use for non-commercial purposes with attribution.
