import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_processor import process_salary_data, get_metrics, get_top_deviations
from utils.visualizations import create_gauge_chart, create_department_comparison

# Page config
st.set_page_config(
    page_title="Baltimore Salary Tracker",
    page_icon="Baltimore City",
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
    data = pd.read_csv('data/salary_cleaned.csv.zip', compression='zip')
    return process_salary_data(data)


try:
    data = load_data()

    # Filters - Year first
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox(
            "Select Year",
            options=sorted(data['FiscalYear'].unique()),
            index=len(data['FiscalYear'].unique()) - 1
        )

    # Filter data for that year to get relevant departments
    year_filtered_data = data[data['FiscalYear'] == selected_year]
    available_departments = sorted(year_filtered_data['AgencyName'].unique().tolist())

    with col2:
        selected_dept = st.selectbox(
            "Select AgencyName",
            options=['All'] + available_departments
        )

    # Final filtering
    filtered_data = year_filtered_data
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
            create_department_comparison(filtered_data, selected_year),
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
