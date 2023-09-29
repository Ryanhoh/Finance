import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import plotly.subplots as sp
import pandas as pd
import numpy as np
import json

from scipy.stats import pearsonr
from scipy.stats import spearmanr
import numpy as np
from scipy.stats import linregress


ticker_to_name = {
    'ACA.PA': 'Crédit Agricole',
    'AI.PA': 'Air Liquide',
    'AIR.PA': 'Airbus',
    'ALO.PA': 'Alstom',
    'BN.PA': 'Danone',
    'BNP.PA': 'BNP Paribas',
    'CA.PA': 'Carrefour',
    'CAP.PA': 'Capgemini',
    'CS.PA': 'AXA',
    'DG.PA': 'Vinci',
    'DSY.PA': 'Dassault Systèmes',
    'EL.PA': 'EssilorLuxottica',
    'EN.PA': 'Bouygues',
    'ENGI.PA': 'Engie',
    'ERF.PA': 'Eurofins Scientific',
    'GLE.PA': 'Société Générale',
    'HO.PA': 'Thales',
    'KER.PA': 'Kering',
    'LR.PA': 'Legrand',
    'MC.PA': 'LVMH',
    'ML.PA': 'Michelin',
    'MT.AS': 'ArcelorMittal',
    'OR.PA': "L'Oréal",
    'ORA.PA': 'Orange',
    'PUB.PA': 'Publicis',
    'RI.PA': 'Pernod Ricard',
    'RMS.PA': 'Hermès',
    'RNO.PA': 'Renault',
    'SAF.PA': 'Safran',
    'SAN.PA': 'Sanofi',
    'SGO.PA': 'Saint-Gobain',
    'STMPA.PA': 'STMicroelectronics',
    'SU.PA': 'Schneider Electric',
    'TEP.PA': 'Teleperformance',
    'TTE.PA': 'TotalEnergies',
    'VIE.PA': 'Veolia',
    'VIV.PA': 'Vivendi',
    'WLN.PA': 'Worldline',
    'STLAP.PA': 'Stellantis'
}


def split_data_by_year(df):
    df['Date'] = pd.to_datetime(df.index) 
    dataframes = {}
    years = df['Date'].dt.year.unique() 

    for year in years:
        dataframes[f"df_all_{year}"] = df[df['Date'].dt.year == year].drop(columns=['Date']).copy()

    return dataframes

#  -------------------------------------------------    FONCTION   ---------------------------------------------------------


def calculate_annual_beta(df):
    df = df.select_dtypes(include=[np.number])
    df = df.pct_change().dropna()
    
    np_array = df.values
    m = np_array[:, 0]  
    beta = []
    for ind, col in enumerate(df):
        if ind > 0:
            s = np_array[:, ind]
            covariance = np.cov(s, m)
            beta.append(covariance[0, 1] / covariance[1, 1])
    return pd.Series(beta, df.columns[1:], name='beta')

def calculate_beta_over_period(dataframes, start_year, end_year):
    df_period = pd.concat([dataframes[f"df_all_{year}"] for year in range(start_year, end_year + 1)])
    df_period = df_period.select_dtypes(include=[np.number])
    beta = calculate_annual_beta(df_period)
    return beta



#  -------------------------------------------------    FONCTION   ---------------------------------------------------------


def calculate_market_performance(dataframes, start_year, end_year):
    df_period = pd.concat([dataframes[f"df_all_{year}"] for year in range(start_year, end_year + 1)])
    df_period = df_period['^FCHI']
    initial_price = df_period.iloc[0]
    final_price = df_period.iloc[-1]
    performance = (final_price - initial_price) / initial_price
    return performance

def calculate_performance(dataframes, start_year, end_year):
    df_period = pd.concat([dataframes[f"df_all_{year}"] for year in range(start_year, end_year + 1)])
    df_period = df_period.drop(columns=['^FCHI', 'Date.1'], errors='ignore')
    initial_prices = df_period.iloc[0]
    final_prices = df_period.iloc[-1]
    performance = (final_prices - initial_prices) / initial_prices
    return performance

#  -------------------------------------------------    FONCTION   ---------------------------------------------------------

def generate_dual_plot(beta_values, performance_values, period, color_scale, width=1400):
    tickers = performance_values.index
    scaled_colors = [color_scale[int(i*(len(color_scale)-1)/(len(beta_values)-1))] for i in range(len(beta_values))]
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=(f'Performance {period}', f'Beta {period}'))
    

    for idx, ticker in enumerate(tickers):
        company_name = ticker_to_name.get(ticker, ticker)  
        hovertext_performance = f"{ticker}<br>Performance = {'+' if performance_values[idx] > 0 else ''}{performance_values[idx]:.2f}%"
        hovertext_beta = f"{ticker}<br>Beta = {beta_values[idx]:.2f}"
        
        fig.add_trace(go.Bar(x=[ticker], y=[performance_values[idx]], name=company_name, hoverinfo="text", hovertext=hovertext_performance, marker_color=scaled_colors[idx], legendgroup=ticker), row=1, col=1)
        fig.add_trace(go.Bar(x=[ticker], y=[beta_values[idx]], name=company_name, hoverinfo="text", hovertext=hovertext_beta, marker_color=scaled_colors[idx], legendgroup=ticker, showlegend=False), row=1, col=2)

        source_annotation = dict(x=1.1, y=-0.3, xref='paper', yref='paper', text='Source : Yahoo Finance', showarrow=False, font=dict(size=10, color="grey"), xanchor='right', yanchor='auto')
    if 'annotations' in fig.layout:
        fig.layout.annotations += (source_annotation,)
    else:
        fig.layout.annotations = [source_annotation]

    fig.update_yaxes(title_text="Performance (%)", row=1, col=1, gridcolor='white', zerolinecolor='white', tickcolor='white')
    fig.update_yaxes( row=1, col=2, gridcolor='grey', zerolinecolor='white', tickcolor='white')
    fig.update_xaxes(tickcolor='white', zerolinecolor='white', linecolor='white', row=1, col=1)
    fig.update_xaxes(tickcolor='white', zerolinecolor='white', linecolor='white', row=1, col=2)
    fig.add_shape(type="line", x0=-0.5, x1=len(tickers)-0.5, y0=1, y1=1, line=dict(color="lightseagreen", width=2), xref='x2', yref='y2')
    fig.update_layout(barmode='overlay', width=width)

    return fig

#  -------------------------------------------------    FONCTION   ---------------------------------------------------------

def render_table():
    st.markdown("""
    <style>
        table {
            width: 30%;  
            margin-left: 0%;
            margin-right: auto;
        }
        th {
            font-weight: bold;
            color: white;
            text-decoration: underline;
            padding: 10px;
        }
        td {
            padding: 10px;
        }
    </style>

    <table>
        <tr>
            <th>Actions défensives</th>
            <th>Actions offensives</th>
        </tr>
        <tr>
            <td>LVMH  (MC.PA)</td>
            <td>Airbus  (AIR.PA)</td>
        </tr>
        <tr>
            <td>Hermes  (RMS.PA)</td>
            <td>Capgemini  (CAP.PA)</td>
        </tr>
        <tr>
            <td>Danone  (BN.PA)</td>
            <td>Dassault Systèmes  (DSY.PA)</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)


def add_annotations_to_bars(fig):
    new_annotations = []

    if hasattr(fig.layout, "annotations"):
        new_annotations.extend(fig.layout.annotations)

    for j, trace in enumerate(fig.data):
        if trace.visible == "legendonly":
            continue

        if (j % 2) == 0:  
            trace_type = "Performance"
            xref = 'x1'
            yref = 'y1'
        else: 
            trace_type = "Beta"
            xref = 'x2'
            yref = 'y2'

        for x_val, y_val in zip(trace.x, trace.y):
            if y_val != 0:  
                annotation_text = str(round(y_val, 2))
                y_position = y_val / 2 if y_val > 0 else y_val / 2
                if trace_type == "Performance":
                    annotation_text += "%"
                new_annotations.append(
                    dict(
                        x=x_val,
                        y=y_position,
                        text=annotation_text,
                        showarrow=False,
                        font=dict(size=12, color='black'),
                        xref=xref,
                        yref=yref
                    )
                )
    
    fig.layout.annotations = new_annotations


class _SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

def get_session_state(**kwargs):
    session_state = getattr(st, '_session_state', None)
    if session_state is None:
        st._session_state = _SessionState(**kwargs)
        session_state = st._session_state
    return session_state

#  -------------------------------------------------    FONCTION   ---------------------------------------------------------
def beta_histogram_annually(betas_annual, tickers_to_filter=None, color_scale="Geyser", show_counts=False, custom_title='Beta : Distribution des 40 actions par année', width=1400):
    df_list = []

    for year, beta_df in betas_annual.items():
        temp_df = beta_df.reset_index()
        temp_df.columns = ['Ticker', 'Beta']
        temp_df['Year'] = year
        df_list.append(temp_df)

    full_df = pd.concat(df_list, axis=0)

    if tickers_to_filter:
        full_df = full_df[full_df['Ticker'].isin(tickers_to_filter)]

    full_df['Company Name'] = full_df['Ticker'].apply(lambda x: ticker_to_name.get(x, x))

    n_colors = len(full_df['Company Name'].unique())
    colors = px.colors.sample_colorscale(color_scale, n_colors)

    fig = px.histogram(full_df, x='Beta', color='Company Name', title=custom_title, color_discrete_sequence=colors)
    
    if show_counts or (tickers_to_filter and len(tickers_to_filter) == 1):
        fig.update_traces(texttemplate='%{y}', textposition='inside', selector=dict(type='histogram'))

    fig.update_layout(
        title={
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        barmode='overlay',
        xaxis_title_text='Bêta',
        yaxis_title_text='Nombre d’occurrences',
        width=width,
        bargap=0.1,
        showlegend=True,
        xaxis=dict(tickcolor='white', zerolinecolor='white', linecolor='white', gridcolor='white'),
        yaxis=dict(tickcolor='white', zerolinecolor='white', linecolor='white', gridcolor='white')   
    )

    source_annotation = dict(
        x=1.12, y=-0.2,
        xref='paper',
        yref='paper',
        text='Source : Yahoo Finance',
        showarrow=False,
        font=dict(size=10, color="grey"),
        xanchor='right',
        yanchor='auto'
    )

    fig.update_layout(annotations=[source_annotation])

    return fig



#  -------------------------------------------------    FONCTION   ---------------------------------------------------------


def beta_histogram_periods(betas_periods, periods):
    fig = go.Figure()
    for beta_df, (start, end) in zip(betas_periods, periods):
        fig.add_trace(go.Histogram(x=beta_df, name=f'{start}-{end}', opacity=0.75))

    fig.update_layout(
        title_text='Distribution des Bêta par Tranche d’Années',
        barmode='overlay',
        xaxis_title_text='Bêta',
        yaxis_title_text='Nombre d’actions',
        bargap=0.1
    )

    return fig

#  -------------------------------------------------    FONCTION   ---------------------------------------------------------

def plot_beta_vs_performance(betas, performances, period, color_scale, width=1400, regression_line_width=1.7, marker_size=18):
    
    df = pd.DataFrame({'Beta': betas, 'Performance': performances})
    
    df['Company Name'] = df.index.map(lambda x: ticker_to_name.get(x, x))
    
    title = f'Corrélation {period}'
    
    fig = px.scatter(df, x='Beta', y='Performance', hover_name='Company Name', color='Company Name',
                     color_discrete_sequence=color_scale,
                     labels={'Beta': 'Bêta', 'Performance': 'Performance (%)'},
                     hover_data={'Beta': True, 'Performance': True},
                     title=title
                     )

    slope, intercept, _, _, _ = linregress(df['Beta'], df['Performance'])
    x_vals = np.array(df['Beta'])
    y_vals = intercept + slope * x_vals
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Régression', line=dict(color='white', width=regression_line_width)))

    source_annotation = dict(
        x=1.12, y=-0.2,
        xref='paper',
        yref='paper',
        text='Source : Yahoo Finance',
        showarrow=False,
        font=dict(size=10, color="grey"),
        xanchor='right',
        yanchor='auto'
    )

    fig.update_layout(
        width=width,
        title_x=0.42,
        xaxis=dict(tickcolor='white', zeroline=False, linecolor='white', gridcolor='rgba(255, 255, 255, 0.03)', showgrid=True),
        yaxis=dict(tickcolor='white', zeroline=False, linecolor='white', gridcolor='rgba(255, 255, 255, 0.03)', tickformat='.0%', showgrid=True),
        annotations=[source_annotation]
    )
    
    fig.update_traces(marker=dict(size=marker_size), selector=dict(mode='markers'), hoverinfo='name+x+y')

    return fig


def load_lottie_file(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)











