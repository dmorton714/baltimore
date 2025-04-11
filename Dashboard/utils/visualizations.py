import plotly.graph_objects as go
import plotly.express as px

def create_gauge_chart(actual, expected, year):
    '''
    Create a gauge chart comparing actual vs expected salary spend
    '''
    steps = [{'range': [0, expected], 'color': '#004080'}]
    if actual > expected:
        steps.append({'range': [expected, actual], 'color': '#ffd700'})

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=actual,
        number={'prefix': "$", 'valueformat': ",.0f"},
        delta={
            'reference': expected,
            'increasing': {'color': "red"},
            'decreasing': {'color': "green"},
            'valueformat': ",.0f",
            'prefix': "$"
        },
        gauge={
            'axis': {'range': [0, max(actual, expected) * 1.1]},
            'bar': {'color': 'rgba(0,0,0,0)'},
            'steps': steps,
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.95,
                'value': actual
            }
        },
        title={'text': f"{year} Budget vs. Actual Salary Spend", 'font': {'size': 20}},
    ))

    fig.update_layout(
        height=400,
        margin=dict(t=100, b=0, l=40, r=40)
    )

    return fig


def create_department_comparison(data, year):
    '''
    Create department comparison bar chart
    '''
    dept_data = data[data['FiscalYear'] == str(year)].groupby('AgencyName').agg({
        'GrossPay': 'sum',
        'AnnualSalary': 'sum'
    }).reset_index()

    dept_data['Variance_Pct'] = ((dept_data['GrossPay'] - dept_data['AnnualSalary']) / dept_data['AnnualSalary']) * 100

    fig = px.bar(dept_data.sort_values('Variance_Pct'),
                 y='AgencyName',
                 x='Variance_Pct',
                 orientation='h',
                 title='Department Budget Variance (%)',
                 color='Variance_Pct',
                 color_continuous_scale=['green', 'yellow', 'red'])

    fig.update_layout(
        height=600,
        margin=dict(t=50, b=0, l=200, r=40),
        xaxis_title="Budget Variance (%)",
        yaxis_title=None,
        coloraxis_showscale=False
    )

    return fig
