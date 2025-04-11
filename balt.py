import pandas as pd
import re
import plotly.graph_objects as go

sal = pd.read_csv('data/salary.csv')


def clean(sal):
    # convert HireDate to datetime
    sal['HireDate'] = pd.to_datetime(sal['HireDate'], unit='ms')
    # sal['HireDate'] = sal['HireDate'].dt.strftime('%m%d%Y')

    # clean FiscalYear
    sal['FiscalYear'] = sal['FiscalYear'].str.replace('^FY', '', regex=True)

    # drop rows with missing values in GrossPay
    sal = sal.dropna(subset=['GrossPay'])

    # removes the trailing number in parentheses from AgencyName
    sal['AgencyName'] = sal['AgencyName'].str.replace(
        r'\s\(\d+\)', '', regex=True)

    # strip spaces
    sal[sal.select_dtypes('object').columns] = sal[sal.select_dtypes(
        'object').columns].apply(lambda x: x.str.strip())

    # List of words to replace
    replace_dict = {
        'Police': 'Police Department',
        'Fire': 'Fire Department',
    }

    # Loop through the dictionary and replace each word with regex
    for old, new in replace_dict.items():
        sal['AgencyName'] = sal['AgencyName'].apply(lambda x: re.sub(
            rf'\b{re.escape(old)}\b(?! Department)', new, str(x)) if isinstance(x, str) else x)

    # Step 1: Fill JobTitle with AgencyName where JobTitle is NaN or empty if no agency name drops
    sal['JobTitle'] = sal['JobTitle'].fillna(sal['AgencyName'])
    sal['JobTitle'] = sal['JobTitle'].apply(lambda x: x if isinstance(
        x, str) and x.strip() != "" else sal['AgencyName'])
    sal = sal[sal['AgencyName'].notna() & (
        sal['AgencyName'].str.strip() != "")]

    # Remove rows where AnnualSalary is NaN or 0
    sal = sal[sal['AnnualSalary'].notna() & (sal['AnnualSalary'] != 0)]

    # Remove rows where GrossPay is NaN or 0
    sal = sal[sal['GrossPay'].notna() & (sal['GrossPay'] != 0)]

    # Discrepancy in amount
    sal['Pay_Discrepancy'] = sal['GrossPay'] - sal['AnnualSalary']

    # Discrepancy in percentage (relative to AnnualSalary)
    sal['Pay_Discrepancy_Pct'] = (
        (sal['GrossPay'] - sal['AnnualSalary']) / sal['AnnualSalary']) * 100

    return sal


# code for 5
def plot_info(year, data) -> None:
    # Ensure 'FiscalYear' is treated as a string
    data['FiscalYear'] = data['FiscalYear'].astype(str)

    # Filter the data for the given year
    year_data = data[data['FiscalYear'] == str(year)]

    # If no data for that year, exit function
    if year_data.empty:
        print(f"No data available for {year}")
        return

    # Group and aggregate data by FiscalYear
    summary = year_data.groupby('FiscalYear')[
        ['GrossPay', 'AnnualSalary']].sum().reset_index()

    # Extract actual and expected values
    actual = summary['GrossPay'].iloc[0]
    expected = summary['AnnualSalary'].iloc[0]

    # Calculate the discrepancy (absolute and percentage)
    discrepancy = actual - expected
    discrepancy_pct = (discrepancy / expected) * 100

    # Create the gauge plot
    steps = [
        # Dark blue for expected salary
        {'range': [0, expected], 'color': '#004080'}
    ]

    # Add yellow step if actual exceeds expected
    if actual > expected:
        # Yellow for actual salary
        steps.append({'range': [expected, actual], 'color': 'yellow'})

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=actual,
        delta={
            'reference': expected,
            'increasing': {'color': "red"},
            'decreasing': {'color': "green"}
        },
        gauge={
            'axis': {'range': [0, expected * 1.1]},
            'bar': {'color': 'rgba(0,0,0,0)'},
            'steps': steps,
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': .95,
                'value': actual  # Place the red line at the actual
            }
        },
        title={'text': f"{year} Budgeted Salary Spend vs. Salary Spend Actual", 'font': {
            'size': 20}},
    ))

    fig.update_layout(
        title_font={'size': 20},  # Set font size for the overall layout title
    )

    # Display the discrepancy
    # print(f"Discrepancy for {year}: ${discrepancy:,.2f} ({discrepancy_pct:.2f}%)")

    # Show the figure
    fig.show()


# code for 7
def calculate_total_spend(year, data) -> str:
    # Filter the data for the specified year
    year_filter = data[data['FiscalYear'] == str(year)]

    # Calculate the sum of 'YTD_Total' for the filtered data
    total_spend = year_filter['GrossPay'].sum().round(2)

    # Formats thousands separators
    total_spend = "{:,.2f}".format(total_spend)

    # Return the total spend as a float
    return str(total_spend)


# code for 9
def calculate_total_budget(year, data) -> str:
    # Filter the data for the specified year
    year_filter = data[data['FiscalYear'] == str(year)]

    # Calculate the sum of 'Salary_Total' for the filtered data
    total_spend = year_filter['AnnualSalary'].sum().round(2)

    # Formats thousands separators
    total_spend = "{:,.2f}".format(total_spend)

    # Return the total spend as a float
    return str(total_spend)


# code for 12
def calculate_budget_difference(year, data) -> str:
    # Filter the data for the specified year
    year_filter = data[data['FiscalYear'] == str(year)]

    if year_filter.empty:
        return "No data for the specified year."

    # Extract actual and expected values
    actual_spend = year_filter['GrossPay'].sum()
    budgeted_salary = year_filter['AnnualSalary'].sum()

    # Calculate the percentage difference
    difference = ((actual_spend - budgeted_salary) / budgeted_salary) * 100

    # Format the difference with a '+' or '-' and thousands separators
    return f"{difference:+,.2f}%"


# code for 10
def top_emp_dev(year, data):
    # we had to avoid division by zero and only calculate Discrepancy_Percent for employees with Salary_Total >= 20k
    # Filter the data for the given year
    top_employee = data[data['FiscalYear'] == str(year)].copy()

    # Round the Discrepancy_Percent to 2 decimal places
    top_employee['Pay_Discrepancy_Pct'] = top_employee['Pay_Discrepancy_Pct'].round(
        2)

    # handle Salary_Total < 20k
    top_employee = top_employee[top_employee['AnnualSalary'] >= 10000]

    # Sort the DataFrame by 'Discrepancy_Percent' in descending order
    top_employee = top_employee.sort_values(
        by='Pay_Discrepancy', ascending=False)

    # Keep only the specified columns
    top_employee = top_employee[['FiscalYear', 'Name', 'AgencyName', 'JobTitle',
                                 'AnnualSalary', 'GrossPay',
                                 'Pay_Discrepancy', 'Pay_Discrepancy_Pct']]

    # Reset index and drop the old index column
    top_employee.reset_index(drop=True, inplace=True)

    return top_employee.head(20)


# code for 11
def department_discrepancy(year, data):
    # Group by 'CalYear' and 'Department', summing 'GrossPay' and 'AnnualSalary'
    department = data.groupby(['FiscalYear', 'AgencyName'])[
        ['GrossPay', 'AnnualSalary']].sum().reset_index()

    # Filter the data by the given year
    department = department[department['FiscalYear'] == str(year)]

    # Calculate the percentage difference: ((GrossPay - AnnualSalary) / AnnualSalary) * 100
    department['Pay_Discrepancy_Pct'] = (
        (department['GrossPay'] - department['AnnualSalary']) / department['AnnualSalary']) * 100

    # Round the Pay_Discrepancy_Pct to 2 decimal places
    department['Pay_Discrepancy_Pct'] = department['Pay_Discrepancy_Pct'].round(
        2)

    # Sort the DataFrame by 'Pay_Discrepancy_Pct' in ascending order
    department = department.sort_values(
        by='Pay_Discrepancy_Pct', ascending=False)

    # Format 'GrossPay' and 'AnnualSalary' with thousands separators
    department['GrossPay'] = department['GrossPay'].apply(
        lambda x: f"{x:,.2f}")
    department['AnnualSalary'] = department['AnnualSalary'].apply(
        lambda x: f"{x:,.2f}")

    # Rename columns for final output
    department = department.rename(columns={
        'GrossPay': 'Total Salary Spend',
        'AnnualSalary': 'Salary Budget',
        'Pay_Discrepancy_Pct': 'Discrepancy Percent'
    })

    # Return the result
    return department


if __name__ == "__main__":
    sal = clean(sal)
    year = 2024
    plot_info(2022, sal)
    total_spend = calculate_total_spend(year, sal)
    total_budget = calculate_total_budget(year, sal)
    budget_difference = calculate_budget_difference(year, sal)
    top_employee = top_emp_dev(year, sal)
    department = department_discrepancy(year, sal)
