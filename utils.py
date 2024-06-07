# utils.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from local_components import card_container

def create_bullet_chart(metric, values, title):
    gpt4 = 100 * values[1]
    gpt3_5 = 100 * values[0]
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta", value=gpt4,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': gpt3_5, 'position': "bottom"},
        title={'text': f"<b>{metric}</b><br><span style='color: gray; font-size:0.8em'>GPT-4o</span>", 'font': {"size": 20}},
        gauge={
            'shape': "bullet",
            'axis': {'range': [0, 100]},
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75, 'value': gpt3_5},
            'bgcolor': "white",
            'borderwidth': 0,
            'bar': {'color': "darkblue"}
        }
    ))
    
    fig.update_layout(
        height=120,
        margin={'t': 0, 'b': 0, 'l': 110, 'r': 50},
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
    )
    
    return fig

def prepare_study_data(metrics_importance, values, improvements):
    data = []
    for metric, details in metrics_importance.items():
        for model, value in zip(["gpt-3.5-turbo", "gpt-4o"], details['Values']):
            data.append({
                "Metric": metric,
                "Model":  model,
                "Value": value,
                "Improvement": details['Improvement']
            })
    return pd.DataFrame(data)

def create_confusion_matrix(df, title):
    fig = go.Figure(data=go.Heatmap(
        z=df.iloc[:, 1:].values,
        x=df.columns[1:],
        y=df['Category'],
        colorscale='Blues'
    ))

    fig.update_layout(
        title=title,
        xaxis_nticks=36
    )

    return fig
def display_metric_card(card_cols, metrics, metrics_importance, values, improvements, i):
    with card_cols[i]:
        index = i
        current_metric = metrics[index]
        current_m_dict = metrics_importance[current_metric]
        m_key = current_metric.replace(" ", "")
        with card_container(key=f"{m_key}_card"):
            st.markdown(f"<b>{current_metric}:</b> <span style='color: gray; font-size:0.8em'>increased from {values[index][0]} to {values[index][1]} ({improvements[index]})</span>", unsafe_allow_html=True)
            st.plotly_chart(create_bullet_chart(current_metric, values[i], f"{metrics[i]} Improvement"), use_container_width=True)
            st.markdown(f"<span style='color: gray; font-size:0.8em'>{current_m_dict['Description']}</span>", unsafe_allow_html=True)