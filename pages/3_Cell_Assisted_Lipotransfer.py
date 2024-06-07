# pages/1_Cell_Assisted_Lipotransfer.py
import streamlit as st
import pandas as pd
from utils import create_bullet_chart, prepare_study_data, create_confusion_matrix
from local_components import card_container
from streamlit_extras.colored_header import colored_header

# Sample data for "Cell Assisted Lipotransfer" study
metrics_importance_lipotransfer = {
    "Recall": {
        "Description": "Essential for ensuring all relevant studies are identified.",
        "Values": [0.9881, 0.9981],
        "Improvement": "+1.01%"
    },
    "Precision": {
        "Description": "Ensures the identified studies are truly relevant.",
        "Values": [0.9960, 0.9984],
        "Improvement": "+0.24%"
    },
    "F1 Score": {
        "Description": "Balances recall and precision.",
        "Values": [0.9913, 0.9982],
        "Improvement": "+0.69%"
    },
    "Specificity": {
        "Description": "Correctly identifies non-relevant studies.",
        "Values": [0.9888, 0.9981],
        "Improvement": "+0.93%"
    },
    "Accuracy": {
        "Description": "Overall correctness of the model's predictions.",
        "Values": [0.9881, 0.9981],
        "Improvement": "+1.00%"
    }
}

confusion_data_include_lipotransfer = pd.DataFrame({
    "Category": ["Include", "Insufficient Information", "Exclude"],
    "First Review": [8, 1, 2],
    "Evaluation Step": [27, 254, 2390],
})

confusion_data_exclude_lipotransfer = pd.DataFrame({
    "Category": ["Exclude", "Insufficient Information", "Include"],
    "First Review": [2647, 255, 35],
    "Evaluation Step": [2390, 254, 27],
})

values_lipotransfer = [
    [0.9881, 0.9981],  # Recall
    [0.9960, 0.9984],  # Precision
    [0.9913, 0.9982],  # F1 Score
    [0.9888, 0.9981],  # Specificity
    [0.9881, 0.9981]   # Accuracy
]
improvements_lipotransfer = ["+1.01%", "+0.24%", "+0.69%", "+0.93%", "+1.00%"]

st.title("Cell Assisted Lipotransfer Title and Abstract Screening Results")

st.subheader("Performance Metrics Interpretation")
st.write("#### The evaluation step using GPT-4o significantly improved all performance metrics:")

df_metrics = prepare_study_data(metrics_importance_lipotransfer, values_lipotransfer, improvements_lipotransfer)
metrics = list(metrics_importance_lipotransfer.keys())

card_cols = st.columns(2)
for I in range(len(metrics))[:2]:
    with card_cols[I]:
        index = I
        current_metric = metrics[index]
        current_m_dict = metrics_importance_lipotransfer[current_metric]
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
        current_m_dict = metrics_importance_lipotransfer[current_metric]
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
    st.plotly_chart(create_confusion_matrix(confusion_data_include_lipotransfer, "Confusion Matrix for Included Studies"), use_container_width=True)

with tabs_confusion[1]:
    st.write("### Excluded Studies")
    st.write("This heatmap shows the confusion matrix for excluded studies between the initial review and the evaluation step.")
    st.plotly_chart(create_confusion_matrix(confusion_data_exclude_lipotransfer, "Confusion Matrix for Excluded Studies"), use_container_width=True)
