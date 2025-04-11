import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_processor import process_salary_data, get_metrics, get_top_deviations
from utils.visualizations import create_gauge_chart, create_AgencyName_comparison

# Page config
st.set_page_config(
    page_title="Louisville Metro Salary Tracker",
    page_icon="LMG",
    layout="wide"
)

# Load custom CSS
with open('Dashboard/assetts/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown("<h1 style='text-align: left; white-space: nowrap;'>Baltimore Government Salary Tracker</h1>", unsafe_allow_html=True)

# Load and process data
@st.cache_data
def load_data():
    data = pd.read_csv("data/salary_cleaned.csv")
    return process_salary_data(data, datetime.now().strftime("%B %d, %Y"))

try:
    data = load_data()
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox(
            "Select Year",
            options=sorted(data['FiscalYear'].unique()),
            index=len(data['FiscalYear'].unique())-1
        )
    with col2:
        selected_dept = st.selectbox(
            "Select AgencyName",
            options=['All'] + sorted(data['AgencyName'].unique().tolist())
        )

    # Filter data based on selections
    filtered_data = data[data['FiscalYear'] == selected_year]
    if selected_dept != 'All':
        filtered_data = filtered_data[filtered_data['AgencyName'] == selected_dept]

    # Get metrics
    metrics = get_metrics(filtered_data, selected_year)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Salary Spend", f"${metrics['GrossPay']:,.2f}")
    with col2:
        st.metric("Salary Budget", f"${metrics['AnnualSalary']:,.2f}")
    with col3:
        st.metric("Budget Variance", f"{metrics['Pay_Discrepancy_Pct']:+.2f}%")

    # Main visualizations
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(
            create_gauge_chart(
                metrics['GrossPay'],
                metrics['AnnualSalary'],
                selected_year
            ),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            create_AgencyName_comparison(filtered_data, selected_year),
            use_container_width=True
        )

    # Top deviations table
    st.subheader("Top Salary Deviations")
    top_dev = get_top_deviations(filtered_data, selected_year)
    st.dataframe(
        top_dev.style.format({
            'GrossPay': '${:,.2f}',
            'AnnualSalary': '${:,.2f}',
            'Pay_Discrepancy': '${:,.2f}',
            'Pay_Discrepancy_Pct': '{:,.2f}%'
        }),
        use_container_width=True
    )

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.error("Please check your data source and try again.")