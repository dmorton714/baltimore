import pandas as pd


def process_salary_data(sal):
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


def get_metrics(data, year):
    '''
    Calculate key metrics for the dashboard
    '''
    year_data = data[data['FiscalYear'] == str(year)]
    total_spend = year_data['GrossPay'].sum()
    total_budget = year_data['AnnualSalary'].sum()
    variance_pct = ((total_spend - total_budget) / total_budget) * 100 if total_budget != 0 else 0

    return {
        'total_spend': round(total_spend, 2),
        'total_budget': round(total_budget, 2),
        'variance_pct': round(variance_pct, 2)
    }


def get_top_deviations(data, year, limit=10):
    '''
    Get top salary deviations
    '''
    year_data = data[data['FiscalYear'] == str(year)].copy()
    budget = year_data['AnnualSalary']
    year_data['Deviation'] = year_data['GrossPay'] - budget
    year_data['Deviation_Pct'] = (year_data['Deviation'] / budget * 100).round(2)
    year_data['AnnualSalary'] = year_data['AnnualSalary'].round(2)

    return year_data.nlargest(limit, 'Deviation_Pct')[
        ['EmployeeName', 'Department', 'GrossPay', 'AnnualSalary', 'Deviation', 'Deviation_Pct']
    ]
