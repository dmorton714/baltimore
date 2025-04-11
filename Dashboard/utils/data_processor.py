import pandas as pd
import re


def process_salary_data(sal):
    # Convert HireDate to datetime
    sal['HireDate'] = pd.to_datetime(sal['HireDate'], errors='coerce')

    # Clean FiscalYear (ensure it is treated as a string)
    sal['FiscalYear'] = sal['FiscalYear'].astype(str).str.replace('^FY', '', regex=True)

    # Drop rows with missing values in GrossPay
    sal = sal.dropna(subset=['GrossPay'])

    # Ensure AgencyName is a string and remove trailing numbers in parentheses
    sal['AgencyName'] = sal['AgencyName'].fillna('').astype(str)
    sal['AgencyName'] = sal['AgencyName'].str.replace(r'\s\(\d+\)', '', regex=True)

    # Strip spaces for object columns (make sure they are string type)
    sal[sal.select_dtypes('object').columns] = sal[sal.select_dtypes('object').columns].apply(
        lambda x: x.fillna('').astype(str).str.strip()  # Ensure NaN values are filled and then strip spaces
    )

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

    # >>> Filter out GrossPay < 30000
    sal = sal[sal['GrossPay'] >= 30000]

    # >>> Filter out GrossPay < 30000
    sal = sal[sal['AnnualSalary'] >= 30000]

    # Discrepancy in amount
    sal['Pay_Discrepancy'] = sal['GrossPay'] - sal['AnnualSalary']

    # Discrepancy in percentage (relative to AnnualSalary)
    sal['Pay_Discrepancy_Pct'] = (
        (sal['GrossPay'] - sal['AnnualSalary']) / sal['AnnualSalary']) * 100

    return sal


def get_metrics(data, year):
    '''
    Calculate key metrics for the dashboard
    '''
    year_data = data[data['FiscalYear'] == str(year)]
    total_spend = year_data['GrossPay'].sum()
    total_budget = year_data['AnnualSalary'].sum()
    variance_pct = ((total_spend - total_budget) / total_budget) * 100 if total_budget != 0 else 0

    # Calculate the individual values you want to display
    gross_pay = total_spend
    annual_salary = total_budget
    pay_discrepancy_pct = variance_pct  # Use your existing logic or calculation if needed

    return {
        'GrossPay': gross_pay,
        'AnnualSalary': annual_salary,
        'Pay_Discrepancy_Pct': pay_discrepancy_pct,
        'total_spend': round(total_spend, 2),
        'total_budget': round(total_budget, 2),
        'variance_pct': round(variance_pct, 2)
    }


def get_top_deviations(data, year, limit=20):
    '''
    Get top salary deviations
    '''
    year_data = data[data['FiscalYear'] == str(year)].copy()

    # Round for cleaner display
    year_data['GrossPay'] = year_data['GrossPay'].round(2)
    year_data['AnnualSalary'] = year_data['AnnualSalary'].round(2)
    year_data['Pay_Discrepancy'] = year_data['Pay_Discrepancy'].round(2)
    year_data['Pay_Discrepancy_Pct'] = year_data['Pay_Discrepancy_Pct'].round(2)

    return year_data.nlargest(limit, 'Pay_Discrepancy_Pct')[
        ['Name', 'AgencyName', 'GrossPay', 'AnnualSalary', 'Pay_Discrepancy', 'Pay_Discrepancy_Pct']
    ]
