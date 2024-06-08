import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from local_components import card_container
from streamlit_extras.colored_header import colored_header

# Function to create a grouped bar chart
def create_grouped_bar_chart(df):
    df_melted = df.melt(id_vars=['Metric', 'Model'], value_vars=['Value'], var_name='Variable', value_name='MetricValue')
    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X('MetricValue:Q', title='Value'),
        y=alt.Y('Model:N', sort=None),
        color=alt.Color('Model:N'),
        row=alt.Row('Metric:N', title=None)
    ).configure_axisY(title=None).configure_facet(spacing=0).configure_header(labelAngle=0).properties(width='container', height=200)
    
    st.altair_chart(chart, use_container_width=True)

# Function to create a Plotly bullet chart
def create_bullet_chart(metric, values, title):
    gpt4 = 100 * values[1]
    gpt3_5 = 100 * values[0]
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta", value=gpt4,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': gpt3_5, 'position': "bottom"},
        title={'text': f"<b>{metric}</b><br><span style='color: gray; font-size:0.8em'>GPT-4o</span>", 'font': {"size": 20}},
        gauge={'shape': "bullet", 'axis': {'range': [0, 100]}, 'threshold': {'line': {'color': "red", 'width': 2}, 'thickness': 0.75, 'value': gpt3_5}, 'bgcolor': "white", 'borderwidth': 0, 'bar': {'color': "darkblue"}}
    ))
    
    fig.update_layout(height=120, margin={'t': 0, 'b': 0, 'l': 110, 'r': 50}, xaxis=dict(showticklabels=False, showgrid=False, zeroline=False), yaxis=dict(showticklabels=False, showgrid=False, zeroline=False))
    
    return fig

# Function to create a Vega-Lite metric chart
def vega_lite_metric_chart(df):
    domain = [min(df[["GPT-3.5 Average", "GPT-4 Average"]].min()) - 0.003, 1]
    df_melted = df.melt(id_vars=["Study", "Metric"], value_vars=["GPT-3.5 Average", "GPT-4 Average"], var_name="Model", value_name="Value")
    st.vega_lite_chart(
        df_melted,
        {
            "encoding": {
                "x": {"field": "Value", "type": "quantitative", "title": "Metric Value", "scale": {"domain": domain}},
                "y": {"field": "Metric", "type": "nominal", "title": "Metric", "axis": {"offset": 0.05, "ticks": False, "minExtent": 0.8, "domain": False}},
                "color": {"field": "Model", "type": "nominal", "scale": {"domain": ["GPT-3.5 Average", "GPT-4 Average"], "range": ["#e6959c", "#911a24"]}, "title": "Model"}
            },
            "layer": [
                {"mark": "line", "encoding": {"detail": {"field": "Metric", "type": "nominal"}, "color": {"value": "#db646f"}}},
                {"mark": {"type": "point", "filled": True}, "encoding": {"size": {"value": 100}, "opacity": {"value": 1}}}
            ]
        },
        use_container_width=True,
    )

# Function to create a confusion matrix heatmap
def create_confusion_matrix(df, title):
    fig = go.Figure(data=go.Heatmap(z=df.iloc[:, 1:].values, x=df.columns[1:], y=df['Category'], colorscale='Blues'))
    fig.update_layout(title=title, xaxis_nticks=36)
    return fig

# Function to load metrics data from a CSV file
def load_metrics_data(csv_file):
    return pd.read_csv(csv_file)

# Function to load confusion matrix data from a CSV file
def load_confusion_data(csv_file):
    return pd.read_csv(csv_file)

# Function to display metric cards
def display_metric_cards(metrics, metrics_data, font_size=1.2):
    num_metrics = len(metrics)
    num_cols = 2
    card_cols = [st.columns(num_cols) for _ in range((num_metrics - 1) // num_cols + 1)]

    for i in range(num_metrics):
        metric = metrics[i]
        values = [metrics_data[metrics_data["Metric"] == metric][f"GPT-3.5 Average"].values[0], metrics_data[metrics_data["Metric"] == metric][f"GPT-4 Average"].values[0]]
        description = metrics_data[metrics_data["Metric"] == metric]["Description"].values[0]

        col_index = i // num_cols
        card_index = i % num_cols

        with card_cols[col_index][card_index]:
            m_key = metric.replace(" ", "")
            with card_container(key=f"{m_key}_card"):
                st.plotly_chart(create_bullet_chart(metric, values, f"{metric} Improvement"), use_container_width=True)
                st.markdown(f"<span style='color: gray; font-size:{font_size}em'>{description}</span>", unsafe_allow_html=True)

# Function to create a study page
def create_study_page(study_name, metrics_data, confusion_data):
    st.title(f"{study_name} Title and Abstract Screening Results")
    
    st.subheader("Performance Metrics Interpretation")
    st.write("#### The evaluation step using GPT-4o significantly improved all performance metrics:")
    
    metrics = metrics_data["Metric"].unique()
    display_metric_cards(metrics, metrics_data)
    
    colored_header(label="Confusion Matrix Analysis", description="Combined Summary of Metrics", color_name="violet-70")
    
    vega_lite_metric_chart(metrics_data)
    
    tabs_confusion = st.tabs(["Included Studies", "Excluded Studies"])
    
    with tabs_confusion[0]:
        st.write("### Included Studies")
        st.write("This heatmap shows the confusion matrix for included studies between the initial review and the evaluation step.")
        st.plotly_chart(create_confusion_matrix(confusion_data[confusion_data["Category"] == "Include"], "Confusion Matrix for Included Studies"), use_container_width=True)
    
    with tabs_confusion[1]:
        st.write("### Excluded Studies")
        st.write("This heatmap shows the confusion matrix for excluded studies between the initial review and the evaluation step.")
        st.plotly_chart(create_confusion_matrix(confusion_data[confusion_data["Category"] == "Exclude"], "Confusion Matrix for Excluded Studies"), use_container_width=True)

# Function to create a comparison dashboard
def create_comparison_dashboard(metrics_data, confusion_data):
    st.title("Comparison of LLM Title and Abstract Screening Results")

    st.subheader("Performance Metrics Comparison")
    
    metrics_data_combined = pd.concat(metrics_data)
    confusion_data_combined = pd.concat(confusion_data)
    
    with card_container(key="chart1"):
        st.vega_lite_chart(metrics_data_combined, {
            'mark': {'type': 'bar', 'tooltip': True, 'cornerRadiusEnd': 4},
            'encoding': {
                'x': {'field': 'Metric', 'type': 'ordinal'},
                'y': {'field': 'Value', 'type': 'quantitative', 'axis': {'grid': False}},
                'xOffset': {'field': 'Model'},
                'color': {'field': 'Model'}
            },
        }, use_container_width=True)
    
    st.write("### Detailed Performance Metrics")
    
    st.write("The following charts show the performance metrics for all studies.")
    
    studies = metrics_data_combined["Study"].unique()
    for study in studies:
        st.write(f"#### {study}")
        df_study = metrics_data_combined[metrics_data_combined["Study"] == study]
        vega_lite_metric_chart(df_study)
    
    st.write("### Confusion Matrix Analysis")
    
    tabs_confusion = st.tabs(studies)
    
    for i, study in enumerate(studies):
        with tabs_confusion[i]:
            st.write(f"#### Included Studies - {study}")
            st.plotly_chart(create_confusion_matrix(confusion_data_combined[(confusion_data_combined["Study"] == study) & (confusion_data_combined["Category"] == "Include")], f"Confusion Matrix for Included Studies ({study})"), use_container_width=True)
            st.write(f"#### Excluded Studies - {study}")
            st.plotly_chart(create_confusion_matrix(confusion_data_combined[(confusion_data_combined["Study"] == study) & (confusion_data_combined["Category"] == "Exclude")], f"Confusion Matrix for Excluded Studies ({study})"), use_container_width=True)
