# pages/2_Free_Fibula_Flap.py
import streamlit as st
import pandas as pd
from utils import create_bullet_chart, prepare_study_data, create_confusion_matrix,display_metric_card
from local_components import card_container
from streamlit_extras.colored_header import colored_header

# Define the data for the "Free Fibula Flap" study
metrics_importance_fibula_flap = {
    "Recall": {
        "Description": "Essential for ensuring all relevant studies are identified.",
        "Values": [0.8628, 0.9741],
        "Improvement": "+12.91%"
    },
    "Precision": {
        "Description": "Ensures the identified studies are truly relevant.",
        "Values": [0.9728, 0.9871],
        "Improvement": "+1.46%"
    },
    "F1 Score": {
        "Description": "Balances recall and precision.",
        "Values": [0.9061, 0.9785],
        "Improvement": "+7.99%"
    },
    "Specificity": {
        "Description": "Correctly identifies non-relevant studies.",
        "Values": [0.8624, 0.9744],
        "Improvement": "+12.98%"
    },
    "Accuracy": {
        "Description": "Overall correctness of the model's predictions.",
        "Values": [0.8628, 0.9741],
        "Improvement": "+12.91%"
    }
}

confusion_data_include_fibula_flap = pd.DataFrame({
    "Category": ["Include", "Insufficient Information", "Exclude"],
    "First Review": [28, 6, 4],
    "Evaluation Step": [24, 13, 1],
})

confusion_data_exclude_fibula_flap = pd.DataFrame({
    "Category": ["Exclude", "Insufficient Information", "Include"],
    "First Review": [978, 58, 156],
    "Evaluation Step": [1067, 61, 28],
})

values_fibula_flap = [
    [0.8628, 0.9741],  # Recall
    [0.9728, 0.9871],  # Precision
    [0.9061, 0.9785],  # F1 Score
    [0.8624, 0.9744],  # Specificity
    [0.8628, 0.9741]   # Accuracy
]
improvements_fibula_flap = ["+12.91%", "+1.46%", "+7.99%", "+12.98%", "+12.91%"]

st.title("Free Fibula Flap Title and Abstract Screening Results")

st.subheader("Performance Metrics Interpretation")
st.write("#### The evaluation step using GPT-4o significantly improved all performance metrics:")

df_metrics = prepare_study_data(metrics_importance_fibula_flap, values_fibula_flap, improvements_fibula_flap)
metrics = list(metrics_importance_fibula_flap.keys())

card_cols = st.columns(2)
for I in range(len(metrics))[:2]:
    with card_cols[I]:
        display_metric_card( card_cols, metrics, metrics_importance, values, improvements, i)
        index = I
        current_metric = metrics[index]
        current_m_dict = metrics_importance_fibula_flap[current_metric]
        m_key = current_metric.replace(" ", "")
        with card_container(key=f"{m_key}_card"):
            st.markdown(f"<b>{current_metric}:</b> <span style='color: gray; font-size:0.8em'>increased from {values[index][0]} to {values[index][1]} ({improvements[index]})</span>", unsafe_allow_html=True)
            st.plotly_chart(create_bullet_chart(current_metric, values[I], f"{metrics[I]} Improvement"), use_container_width=True)
            st.markdown(f"<span style='color: gray; font-size:0.8em'>{current_m_dict['Description']}</span>", unsafe_allow_html=True)

card_cols3 = st.columns(2)
for d in range(2):
    with card_cols3[d]:
        index = I + d + 1
        current_metric = metrics[index]
        current_m_dict = metrics_importance_fibula_flap[current_metric]
        m_key = current_metric.replace(" ", "")
        with card_container(key=f"{m_key}_card"):
            st.markdown(f"<b>{current_metric}:</b> <span style='color: gray; font-size:0.8em'>increased from {values[index][0]} to {values[index][1]} ({improvements[index]})</span>", unsafe_allow_html=True)
            st.plotly_chart(create_bullet_chart(metrics[index], values[index], f"{metrics[index]} Improvement"), use_container_width=True)
            st.markdown(f"<span style='color: gray; font-size:0.8em'>{current_m_dict['Description']}</span>", unsafe_allow_html=True)

colored_header(
    label="Confusion Matrix Analysis",
    description="Combined Summary of Metrics",
    color_name="violet-70",
)

tabs_confusion = st.tabs(["Included Studies", "Excluded Studies"])

with tabs_confusion[0]:
    st.write("### Included Studies")
    st.write("This heatmap shows the confusion matrix for included studies between the initial review and the evaluation step.")
    st.plotly_chart(create_confusion_matrix(confusion_data_include_fibula_flap, "Confusion Matrix for Included Studies"), use_container_width=True)

with tabs_confusion[1]:
    st.write("### Excluded Studies")
    st.write("This heatmap shows the confusion matrix for excluded studies between the initial review and the evaluation step.")
    st.plotly_chart(create_confusion_matrix(confusion_data_exclude_fibula_flap, "Confusion Matrix for Excluded Studies"), use_container_width=True)
