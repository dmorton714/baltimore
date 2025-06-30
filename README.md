# Baltimore

### Future Improvements 
While the dashboard began as a public-facing prototype, it has since transitioned into a contracted project. As a result, further developments and findings are part of a private engagement and are not included in this repository.

## Baltimore Salary Dashboard
An interactive Streamlit dashboard designed to analyze departmental salary spending across Baltimore City. This tool highlights significant deviations in salary data to identify potentially troubled departments. Supporting data-driven decision-making for a political candidates and public stakeholders.

## Project Purpose
This dashboard was built to:
- Visualize department-level salary trends across Baltimore
- Detect outliers and anomalies in salary distributions
- Provide transparency into city payroll spending
- Help a political candidate target departments for further review based on fiscal irregularities

## Features
- Interactive Filtering by department, year, and salary range
- Salary Deviation Detection to highlight unusually high or low spending
- Departmental Summaries with key metrics 
- Visualizations including bar charts, gauge plots, and deviation tables
- Streamlit Interface for ease of use and real-time exploration

## Tech Stack
- Python – Core language
- Streamlit – Web dashboard framework
- Pandas – Data manipulation
- Plotly – Interactive and statistical visualizations
- NumPy – Numerical operations
- Git – Version control

📁 Data
The data used includes:
- Baltimore City departmental salary reports
- Staff-level records including department, role, and pay
- Publicly available sources 

Note: All data is derived from public records.

| data | url |
| --- | --- |
| Baltimore Open Data | https://data.baltimorecity.gov/pages/data-governance |
| Salary Data | https://data.baltimorecity.gov/datasets/0bceed42ed994e65bec410bdf9c383c8_0/explore |
| Crime 14 - 24 600K| https://data.baltimorecity.gov/datasets/e0992dddbbf64231976d5d57763ec4f5_0/explore?location=-6.360272%2C-18.715795%2C1.69&showTable=true |
| NIBRS 22 - Current 200k | https://data.baltimorecity.gov/datasets/204beefe92a645d79fdf0969957bbdf8_0/explore?location=39.287978%2C-76.625846%2C11.12&showTable=true |
| Fiscal Budget 2022 | https://data.baltimorecity.gov/datasets/e8f14ab665424a878dd32ddc150e9d75_0/explore | 
| Homeless | https://data.baltimorecity.gov/datasets/710b935a4e864284ad5da9019fe5fca2_0/explore?location=39.306904%2C-76.627709%2C12.55&showTable=true| 
| tickets 9.5mill | https://data.baltimorecity.gov/datasets/d2a2330d6a374ad39a24a0d7f7b58f19_0/explore | 


## Getting Started
To run this project locally:

###  Virutal Environment Instructions

1. After you have cloned the repo to your machine, navigate to the project 
folder in GitBash/Terminal.
- Create a virtual environment in the project folder. 
- Activate the virtual environment.
- Install the required packages. 
- When you are done working on your repo, deactivate the virtual environment.

### Virtual Environment Commands
| Command | Linux/Mac | GitBash |
| ------- | --------- | ------- |
| Create | `python3 -m venv venv` | `python -m venv venv` |
| Activate | `source venv/bin/activate` | `source venv/Scripts/activate` |
| Install | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Deactivate | `deactivate` | `deactivate` |

2. 
```bash
git clone https://github.com/your-username/baltimore-salary-dashboard.git
cd baltimore-salary-dashboard
pip install -r requirements.txt
streamlit run app.py
```




