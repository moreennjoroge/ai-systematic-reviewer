# pages/3_Comparison_Dashboard.py
import streamlit as st
import pandas as pd
from utils import create_bullet_chart, prepare_study_data, create_confusion_matrix
from local_components import card_container
from streamlit_extras.colored_header import colored_header

# Define the data for both studies
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

values_lipotransfer = [
    [0.9881, 0.9981],  # Recall
    [0.9960, 0.9984],  # Precision
    [0.9913, 0.9982],  # F1 Score
    [0.9888, 0.9981],  # Specificity
    [0.9881, 0.9981]   # Accuracy
]
improvements_lipotransfer = ["+1.01%", "+0.24%", "+0.69%", "+0.93%", "+1.00%"]

values_fibula_flap = [
    [0.8628, 0.9741],  # Recall
    [0.9728, 0.9871],  # Precision
    [0.9061, 0.9785],  # F1 Score
    [0.8624, 0.9744],  # Specificity
    [0.8628, 0.9741]   # Accuracy
]
improvements_fibula_flap = ["+12.91%", "+1.46%", "+7.99%", "+12.98%", "+12.91%"]

st.title("Comparison of LLM Title and Abstract Screening Results")

st.subheader("Performance Metrics Comparison")

# Prepare combined DataFrame
df_metrics_lipotransfer = prepare_study_data(metrics_importance_lipotransfer, values_lipotransfer, improvements_lipotransfer)
df_metrics_fibula_flap = prepare_study_data(metrics_importance_fibula_flap, values_fibula_flap, improvements_fibula_flap)
df_combined = pd.concat([df_metrics_lipotransfer, df_metrics_fibula_flap], keys=["Cell Assisted Lipotransfer", "Free Fibula Flap"], names=["Study"])

df_combined.reset_index(level=0, inplace=True)

st.write("### Detailed Performance Metrics")

st.write("The following charts show the performance metrics for both studies.")

studies = df_combined["Study"].unique()
for study in studies:
    st.write(f"#### {study}")
    df_study = df_combined[df_combined["Study"] == study]
    st.vega_lite_chart(
        df_study,
        {
            "encoding": {
                "x": {
                    "field": 'Value',
                    "type": "quantitative",
                    "title": "Metric Value",
                    "scale": {"domain": [min(df_study["Value"])-0.003,1]}
                },
                "y": {
                    "field": 'Metric',
                    "type": "nominal",
                    "title": 'Metric',
                    "axis": {
                        "offset": 0.05,
                        "ticks": False,
                        "minExtent": 0.8,
                        "domain": False
                    }
                }
            },
            "layer": [
                {
                    "mark": "line",
                    "encoding": {
                        "detail": {
                            "field": 'Metric',
                            "type": "nominal"
                        },
                        "color": {"value": "#db646f"}
                    }
                },
                {
                    "mark": {
                        "type": "point",
                        "filled": True
                    },
                    "encoding": {
                        "color": {
                            "field": 'Model',
                            "type": "ordinal",
                            "scale": {
                                "domain": ["gpt-3.5-turbo", "gpt-4o"],
                                "range": ["#e6959c", "#911a24"]
                            },
                            "title": 'Model'
                        },
                        "size": {"value": 100},
                        "opacity": {"value": 1}
                    }
                }
            ]
        },
        use_container_width=True,
    )

st.write("### Confusion Matrix Analysis")

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

tabs_confusion = st.tabs(["Cell Assisted Lipotransfer", "Free Fibula Flap"])

with tabs_confusion[0]:
    st.write("#### Included Studies")
    st.plotly_chart(create_confusion_matrix(confusion_data_include_lipotransfer, "Confusion Matrix for Included Studies (Cell Assisted Lipotransfer)"), use_container_width=True)
    st.write("#### Excluded Studies")
    st.plotly_chart(create_confusion_matrix(confusion_data_exclude_lipotransfer, "Confusion Matrix for Excluded Studies (Cell Assisted Lipotransfer)"), use_container_width=True)

with tabs_confusion[1]:
    st.write("#### Included Studies")
    st.plotly_chart(create_confusion_matrix(confusion_data_include_fibula_flap, "Confusion Matrix for Included Studies (Free Fibula Flap)"), use_container_width=True)
    st.write("#### Excluded Studies")
    st.plotly_chart(create_confusion_matrix(confusion_data_exclude_fibula_flap, "Confusion Matrix for Excluded Studies (Free Fibula Flap)"), use_container_width=True)
