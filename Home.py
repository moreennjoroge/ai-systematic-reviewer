import streamlit as st
from utils import (
    load_metrics_data,
    load_confusion_data,
    create_study_page,
    create_comparison_dashboard
)
st.set_page_config(page_title="Systematic Reviews", page_icon="🏠",layout="wide",
   initial_sidebar_state="expanded",)


# Main Streamlit App
def main():
    # Load metrics data from CSV file
    metrics_data = load_metrics_data("metrics_data.csv")
    
    # Load confusion matrix data from CSV file
    confusion_data = load_confusion_data("confusion_data.csv")
    
    # Get the list of unique study names
    studies = metrics_data["Study"].unique()
    
    # Create a sidebar selectbox for choosing the study or comparison dashboard
    page = st.sidebar.selectbox("Select a Page", studies.tolist() + ["Comparison Dashboard"])
    
    if page == "Comparison Dashboard":
        # Create the comparison dashboard
        create_comparison_dashboard([metrics_data[metrics_data["Study"] == study] for study in studies], [confusion_data[confusion_data["Study"] == study] for study in studies])
    else:
        # Create the study page for the selected study
        create_study_page(page, metrics_data[metrics_data["Study"] == page], confusion_data[confusion_data["Study"] == page])

if __name__ == "__main__":
    main()