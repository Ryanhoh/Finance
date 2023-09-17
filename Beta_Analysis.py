import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import pandas as pd
from scipy.stats import pearsonr
from scipy.stats import spearmanr


px.defaults.template = "plotly"  
st.set_page_config(layout="wide")

#primaryColor="#FF4B4B"
#backgroundColor="#283650"
#secondaryBackgroundColor="#505B75"
#textColor="#F2F2F3"
#font="sans serif"

company_name = pd.read_csv("company_name.csv")
data_2020_copy = pd.read_csv("data_2020_copy.csv")
data_2021_copy = pd.read_csv("data_2021_copy.csv")
data_2022_copy = pd.read_csv("data_2022_copy.csv")
data_2023_copy = pd.read_csv("data_2023_copy.csv")
final_tri_df = pd.read_csv('final_tri_df.csv')
Beta_years = pd.read_csv('Beta_years.csv')
final_month_df = pd.read_csv('final_month_df.csv')
all_data = pd.read_csv('all_data.csv')

all_data.sort_values(by=['Ticker', 'Year', 'Date'], inplace=True)

annual_performance_2 = all_data.groupby(['Year', 'Ticker']).apply(lambda x: ((x['Close'].iloc[-1] - x['Close'].iloc[0]) / x['Close'].iloc[0]) * 100).reset_index()
annual_performance_2.columns = ['Year', 'Ticker', 'Annual_Performance']
annual_performance_2['Annual_Performance'] = annual_performance_2['Annual_Performance'].round(2)
annual_performance_2.loc[(annual_performance_2['Ticker'] == 'VIV.PA') & (annual_performance_2['Year'] == 2021), 'Annual_Performance'] = -9.68


avg_tri_performance = final_tri_df.groupby('Ticker')['Tri_Performance'].mean().reset_index()
avg_tri_performance = avg_tri_performance.sort_values("Ticker", ascending=True)
avg_tri_performance = avg_tri_performance.round(2)

initial_close = all_data.groupby('Ticker').first()['Close'].reset_index()
final_close = all_data.groupby('Ticker').last()['Close'].reset_index()

merged_data = pd.merge(initial_close, final_close, on='Ticker', suffixes=('_initial', '_final'))
merged_data['Total_Performance'] = ((merged_data['Close_final'] - merged_data['Close_initial']) / merged_data['Close_initial']) * 100
merged_data = merged_data.round(2)

annual_performance = final_tri_df.groupby(['Year', 'Ticker'])['Tri_Performance'].sum().reset_index()
annual_performance['Tri_Performance'] = annual_performance['Tri_Performance'].round(2)

avg_beta_all_years = Beta_years.groupby('Ticker')['Annual_Beta'].mean().reset_index()
avg_beta_all_years = avg_beta_all_years.sort_values("Ticker", ascending=True)
avg_beta_all_years = avg_beta_all_years.round(3)

final_tri_df['Cumulative_Perf'] = final_tri_df.groupby('Ticker')['Tri_Performance'].cumsum()
final_tri_df['Tri_Performance'] = final_tri_df['Tri_Performance'].round(3)

final_tri_df['abs_Beta'] = final_tri_df['Quarterly_Beta'].abs()
final_tri_df['Quarterly_Beta'] = final_tri_df['Quarterly_Beta'].round(2)
final_tri_df['abs_Beta'] = final_tri_df['abs_Beta'].round(2)

Beta_years['Annual_Beta'] = Beta_years['Annual_Beta'].round(3)


tickers = ['ACA.PA', 'AI.PA', 'AIR.PA', 'ALO.PA', 'BN.PA', 'BNP.PA', 'CA.PA', 'CAP.PA', 'CS.PA', 'DG.PA', 'DSY.PA', 'EL.PA', 'EN.PA', 'ENGI.PA', 
           'ERF.PA', 'GLE.PA', 'HO.PA', 'KER.PA', 'LR.PA', 'MC.PA', 'ML.PA', 'MT.AS', 'OR.PA', 'ORA.PA', 'PUB.PA', 'RI.PA', 'RMS.PA', 'RNO.PA', 
           'SAF.PA', 'SAN.PA', 'SGO.PA', 'STMPA.PA', 'SU.PA', 'TEP.PA', 'TTE.PA', 'VIE.PA', 'VIV.PA', 'WLN.PA', 'STLAP.PA']

groups_of_tickers = [tickers[i:i+10] for i in range(0, len(tickers), 10)]

def custom_markdown(text, unsafe_allow_html=True):
    text = text.replace("MC.PA", '<span style="color: #FAE6A0;">MC.PA</span>')
    st.markdown(text, unsafe_allow_html=unsafe_allow_html)

#----------------------------------------------------------------------------------------

min_value = annual_performance_2['Annual_Performance'].min()
max_value = annual_performance_2['Annual_Performance'].max()

years = annual_performance_2['Year'].unique()
figs = {}
for index, year in enumerate(years):
    data_for_year = annual_performance_2[annual_performance_2['Year'] == year]
    data_for_year = data_for_year.sort_values(by='Annual_Performance', ascending=False)
    figs[year] = px.bar(data_for_year, x='Ticker', y='Annual_Performance', color='Annual_Performance',
                        labels={'Annual_Performance': 'P/A (%)'},
                        color_continuous_scale="earth", width=1000)

    figs[year].update_layout(
        title={
            'text': f"Performance {year}",
            'x': 0.15,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=130),
        yaxis=dict(range=[min_value, max_value]),  
        coloraxis_showscale=True if index == 0 else False
    )
    figs[year].update_xaxes(title_text="")
    figs[year].update_yaxes(title_text="", showgrid=True, gridwidth=2, gridcolor='white', zeroline=True, zerolinewidth=3, zerolinecolor='white', dtick=20)


#----------------------------------------------------------------------------------------

min_beta = Beta_years['Annual_Beta'].min()
max_beta = Beta_years['Annual_Beta'].max()

Beta_years['Annual_Beta'] = Beta_years['Annual_Beta'].round(3)
years_beta = Beta_years['Year'].unique()

figs_beta = {}
for year in years_beta:
    data_for_year_beta = Beta_years[Beta_years['Year'] == year]
    
    data_for_year_beta = data_for_year_beta.sort_values(by='Annual_Beta', ascending=False)
    
    figs_beta[year] = px.bar(data_for_year_beta, x='Ticker', y='Annual_Beta', color='Annual_Beta',
                                title=f"Beta {year}",
                                labels={'Annual_Beta': 'Bêta Annuel'},
                                color_continuous_scale="mint", width=1000)
    
    figs_beta[year].update_layout(
        title_x=0.1,
        yaxis=dict(range=[min_beta, max_beta])
    )
    
    if year in [2020, 2021, 2022, 2023]:
        figs_beta[year].update_layout(coloraxis_showscale=False)
        figs_beta[year].update_xaxes(title_text="")
        
        figs_beta[year].update_yaxes(title_text="", showgrid=True, gridwidth=1, gridcolor='white', 
                                     zeroline=True, zerolinewidth=2, zerolinecolor='lightseagreen')  

    figs_beta[year].add_shape(
        type="line",
        x0=0,  
        x1=len(data_for_year_beta) - 1,  
        y0=1,  
        y1=1,  
        line=dict(color="lightseagreen", width=2)
    )



#----------------------------------------------------------------------------------------

sorted_data = merged_data.sort_values(by='Total_Performance', ascending=False)

fig3 = px.bar(sorted_data, x='Ticker', y='Total_Performance', 
             title='Performance Totale des Tickers de 2020 à 2023', 
             color='Total_Performance',
             color_continuous_scale="earth", 
             width=1000)

fig3.update_layout(
    title={
        'text': 'Performance Totale des Tickers de 2020 à 2023',
        'x': 0.18,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    margin=dict(t=110),
    coloraxis_showscale=False
)

fig3.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', showgrid=True, gridwidth=1, gridcolor='white') 


#----------------------------------------------------------------------------------------

sorted_beta_data = avg_beta_all_years.sort_values(by='Annual_Beta', ascending=False)

fig4 = px.bar(sorted_beta_data, x='Ticker', y='Annual_Beta', 
             title='Performance Moyenne des Bêta de 2020 à 2023', 
             color='Annual_Beta',
             color_continuous_scale="earth", 
             width=1000)

fig4.add_shape(
    type="line",
    x0=sorted_beta_data['Ticker'].iloc[0],
    x1=sorted_beta_data['Ticker'].iloc[-1],  
    y0=1,
    y1=1,
    line=dict(color="#4B6858", width=2)
)

fig4.update_layout(
    title={
        'text': 'Performance Moyenne des Bêta de 2020 à 2023',
        'x': 0.18,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    margin=dict(t=110),
    coloraxis_showscale=False
)

fig4.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', showgrid=True, gridwidth=2, gridcolor='white')



#----------------------------------------------------------------------------------------

n_colors = len(final_tri_df['Ticker'].unique())
colors = px.colors.sample_colorscale("Geyser", n_colors)

fig5 = px.bar(final_tri_df, x='Date', y='Tri_Performance', color='Ticker', title='Performance Cumulée des ticker', width=1450, color_discrete_sequence=colors)
fig5.update_layout(
    title={
        'text': 'Performance Cumulée des ticker',
        'x': 0.1,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    bargap=0.4
)
fig5.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='lightgray', showgrid=True, gridwidth=1, gridcolor='white')

fig6 = px.histogram(final_tri_df, x='Quarterly_Beta', color='Ticker', title='Distribution des Beta par trimestre', width=1400, color_discrete_sequence=colors)
fig6.update_layout(
    title={
        'text': 'Distribution des Bêta par trimestre',
        'x': 0.1,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)
fig6.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='lightgray', showgrid=True, gridwidth=1, gridcolor='white')

fig7 = px.histogram(Beta_years, x='Annual_Beta', color='Ticker', title='Distribution des Beta par années', width=1400, color_discrete_sequence=colors)
fig7.update_layout(
    title={
        'text': 'Distribution des Bêta par années',
        'x': 0.1,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)
fig7.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='lightgray', showgrid=True, gridwidth=1, gridcolor='white')



#----------------------------------------------------------------------------------------

n_colors_8 = len(final_tri_df['Ticker'].unique())
palettes_8 = ["Blues", "Bluered", "Oranges", "Jet", "Purples", "Greens", "YlGnBu"]
colors_per_palette_8 = n_colors_8 // len(palettes_8)
geyser_colors_8 = []
for palette in palettes_8:
    geyser_colors_8.extend(px.colors.sample_colorscale(palette, colors_per_palette_8))

custom_color_map_8 = {}
for i, ticker in enumerate(final_tri_df['Ticker'].unique()):
    custom_color_map_8[ticker] = geyser_colors_8[i % len(geyser_colors_8)]

for group in groups_of_tickers:
    sub_data_8 = final_tri_df[final_tri_df['Ticker'].isin(group)]
    fig8 = px.scatter(sub_data_8, x="Date", y="Quarterly_Beta", size="abs_Beta", color="Ticker",
                     title='Evolution des Beta Trimestriel par Ticker',
                     hover_data=['Date'], width=1400, color_discrete_map=custom_color_map_8)
    
    fig8.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='lightgray', showgrid=True, gridwidth=1, gridcolor='white')


    
#----------------------------------------------------------------------------------------

n_colors_9 = len(final_tri_df['Ticker'].unique())
palettes_9 = ["Geyser", "RdYlGn" ,"Tropic", "RdBu"]
colors_per_palette_9 = n_colors_9 // len(palettes_9)
geyser_colors_9 = []
for palette in palettes_9:
    geyser_colors_9.extend(px.colors.sample_colorscale(palette, colors_per_palette_9))

custom_color_map_9 = {}
for i, ticker in enumerate(final_tri_df['Ticker'].unique()):
    custom_color_map_9[ticker] = geyser_colors_9[i % len(geyser_colors_9)]

for group in groups_of_tickers:
    sub_data_9 = final_tri_df[final_tri_df['Ticker'].isin(group)]
    sub_data_9 = sub_data_9.round(3)  

    fig9 = px.scatter(sub_data_9, x='Tri_Performance', y='Quarterly_Beta', color='Ticker', 
                       size=sub_data_9["abs_Beta"].abs(), 
                       hover_data=['Date'], facet_col='Year', width = 1400,
                       color_discrete_map=custom_color_map_9)
    
    fig9.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', showgrid=True, gridwidth=2, gridcolor='white')




#----------------------------------------------------------------------------------------

P_coefficient, P_value = pearsonr(final_tri_df['Tri_Performance'], final_tri_df['Quarterly_Beta'])
S_coefficient, S_value = spearmanr(final_tri_df['Tri_Performance'], final_tri_df['Quarterly_Beta'])

#----------------------------------------------------------------------------------------

option = st.sidebar.radio(
    'Choisissez une page:',
    ('Sujet', 'Action : Performance Annuelle', 'Bêta : Valeur Annuelle', 'Performance Moyenne', 'Performance Cumulée et Distribution', 'Évolution des Bêta', 'Analyse de Corrélation', 'Test Statistique', 'Conclusion', 'Code')
)

st.markdown(
    """
<style>
    .container {
        display: flex;
        justify-content: center;
    }
    .reportview-container .main {
        max-width: 150%;
        padding: 2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

if option == 'Sujet':
    st.markdown("<h2 style='text-decoration: underline;'>Analyse des Bêta et des performances des actions du CAC 40</h2>", unsafe_allow_html=True)
    st.write("")
    st.markdown("""
    Dans un monde financier en constante évolution, la compréhension des performances des actions et de leur Bêta est devenue cruciale 
    pour les investisseurs, les gestionnaires de portefeuille et les analystes. 
    <a href="https://www.investopedia.com/terms/b/beta.asp" style="color: #FFD700 ;" target="_blank">Le Bêta</a>, un indicateur de la volatilité 
    d'une action par rapport à un indice de marché, est souvent utilisé pour évaluer le risque associé à un 
    investissement particulier. Parallèlement, la performance d'une action est un reflet direct de sa rentabilité. 
    Cependant, existe-t-il une corrélation entre ces deux indicateurs clés ? C'est la question centrale que cette analyse cherche à résoudre.
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("<h3 style='text-decoration: underline;'>Objectif</h3>", unsafe_allow_html=True) 
    
    st.markdown("""
            L'objectif principal de cette analyse est d'examiner en profondeur les performances et les Bêta des actions du CAC 40 de **janvier 2020 à août 2023**. 
            Nous cherchons à :
                <li><strong>Évaluer les performances individuelles</strong> des tickers en termes de <strong>rentabilité</strong>.</li>
                <li><strong>Analyser le Bêta de chaque ticker</strong> pour comprendre leur <strong>volatilité</strong> par rapport au marché.</li>
                <li>Examiner s'il existe une <strong>corrélation</strong> entre la <strong>performance et le Bêta des actions</strong>.</li>

            En utilisant des données fiables et des méthodes d'analyse, cette étude vise à fournir des insights qui pourraient être utiles pour les décisions d'investissement et la gestion du risque.
            """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-decoration: underline;'>Problématiques</h3>", unsafe_allow_html=True) 
             
    st.markdown("""
            Nous aborderons les questions suivantes :
                <ol style="padding-left:26px;">
                    <li>Comment le rendement des actions et leurs bêtas ont-ils évolué au fil du temps ?</li>
                    <li>Quelle est la distribution des performances et des Bêta des actions du CAC 40 ?</li>
                    <li>Existe-t-il une corrélation observable entre la performance et le Bêta d'une action ?</li>
                </ol>
        """, unsafe_allow_html=True)

    
    st.markdown("<h4 style='text-decoration: underline;'>Remarques</h4>", unsafe_allow_html=True) 

    st.markdown("""
        Le Bêta est généralement calculé sur une période de 5 ans. J'ai fais le choix de le calculer sur différentes périodes inférieures à 5 ans.
        <ul style="padding-left:26px;">
            <li>Une période de <strong>3 mois</strong>.</li>
            <li>Une période de <strong>1 an</strong>.</li>
            <li>Une période de <strong>3.5 ans</strong>.</li>
        </ul>
        Les Bêta calculés sur une courte période ont <strong>tendance à être plus volatile</strong> et peuvent avoir des valeurs qui semblent <strong>"illogiques"</strong>.<br>
        Ceux-ci peuvent être <strong>influencés</strong> par des événements <strong>temporaires/ponctuels</strong> qui ne reflètent <strong>pas nécessairement</strong> la sensibilité de l'action au long terme.<br>
        Plus un Bêta est calculé sur une <strong>courte temporalité</strong>, plus il sera <strong>sensible aux variations du marché</strong>. Sa valeur peut donc être considérablement affectée.<br>
    """, unsafe_allow_html=True)
    

elif option == 'Action : Performance Annuelle':
    st.markdown("<h1 style='text-decoration: underline;'>Performance Annuelle par Action</h1>", unsafe_allow_html=True)

    st.markdown("""
    Nous avons fait le choix de centrer notre étude sur une seule action : 
    <a href="https://www.lvmh.com/investors/investors-and-analysts/publications/?publications=29" style="color:#FAE6A0;">**MC.PA (Moët Hennessy Louis Vuitton)**</a>.
    Nous nous concentrerons donc sur ses performances, ses Bêta, et tenterons de répondre à nos problématiques.
    La temporalité sélectionnée pour cette étude spécifique sera de 3.5 ans.<br>
                Si vous souhaitez suivre cette analyse, rendez-vous à la section **Performance Moyenne.**""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.plotly_chart(figs[2020], use_container_width=True)
    col2.plotly_chart(figs[2021], use_container_width=True)

    col3, col4 = st.columns(2)
    col3.plotly_chart(figs[2022], use_container_width=True)
    col4.plotly_chart(figs[2023], use_container_width=True)

    st.write(" ")
    st.write(" ")

#--------------------------------------------------------------------------------------------------------------


    st.markdown("<h3 style='text-decoration: underline;'>Entreprises du CAC40</h3>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    num_cols = 4  
    cols = st.columns(num_cols)
    split_length = len(company_name) // num_cols

    for i in range(num_cols):
        start_index = i * split_length
        end_index = (i + 1) * split_length if i != num_cols - 1 else len(company_name)
        sub_df = company_name[start_index:end_index]
        with cols[i]:
            for _, row in sub_df.iterrows():
                st.markdown(f"- **{row['Ticker']}**: {row['Entreprise']}")

#----------------------------------------------------------------------------------------

elif option == 'Bêta : Valeur Annuelle':
    st.markdown("<h1 style='text-decoration: underline;'>Bêta Annuelle par Action</h1>", unsafe_allow_html=True)

    sort_by_alpha_beta = st.checkbox("Ordre alphabétique", key="sort_by_alpha_beta")

    col1, col2 = st.columns(2)
    if sort_by_alpha_beta:
        col1.plotly_chart(figs_beta[2020].update_xaxes(categoryorder="category ascending"), use_container_width=True)
        col2.plotly_chart(figs_beta[2021].update_xaxes(categoryorder="category ascending"), use_container_width=True)
    else:
        col1.plotly_chart(figs_beta[2020], use_container_width=True)
        col2.plotly_chart(figs_beta[2021], use_container_width=True)

    col3, col4 = st.columns(2)
    if sort_by_alpha_beta:
        col3.plotly_chart(figs_beta[2022].update_xaxes(categoryorder="category ascending"), use_container_width=True)
        col4.plotly_chart(figs_beta[2023].update_xaxes(categoryorder="category ascending"), use_container_width=True)
    else:
        col3.plotly_chart(figs_beta[2022], use_container_width=True)
        col4.plotly_chart(figs_beta[2023], use_container_width=True)


#----------------------------------------------------------------------------------------

elif option == 'Performance Moyenne':
    st.markdown("<h1 style='text-decoration: underline;'>Performance Moyenne : Ticker / Bêta 2020-2023</h1>", unsafe_allow_html=True)

    st.write("")

    text1 = """
    <u>**Performances**</u>:
    - Action MC.PA : **+ 90.5%**
    - Marché : **+ 17.17%**
    - Bêta : **1.278**

    <u>**Interprétation**</u>:<br>
                <br>
    Avec un Bêta de 1.278, l'action MC.PA est légèrement plus volatile que le marché. 
                Cela signifie qu'en périodes de hausse ou de baisse du marché, on peut s'attendre à ce que l'action MC.PA augmente ou diminue de façon légèrement plus prononcée que le marché lui-même.
    """
    text1 = text1.replace("MC.PA", '<span style="color: #FAE6A0;">MC.PA</span>')
    st.markdown(text1, unsafe_allow_html=True)

    st.markdown("""Vous l'avez peut-être remarqué, mais le Bêta **"semble incohérent"** ici. Effectivement, dans un monde parfait, le Bêta aurait dû être égal à **5.27**. 
                Sa performance aurait été proportionnellement en ligne avec celle du marché. 
                Cependant, le Bêta mesure la volatilité relative, pas nécessairement la performance relative.<br>""", unsafe_allow_html=True)
                
    custom_markdown("""L'action MC.PA, bien qu'ayant fortement surperformé le marché, n'a pas montré une volatilité cinq fois supérieure à celle du marché. 
                Cela suggère que **d'autres facteurs modulent sa volatilité, indépendamment de sa performance**.""", unsafe_allow_html=True)
    

    st.write(" ")

    sort_by_perf_3 = st.checkbox("Ordre alphabétique", key="sort_by_perf_3")

    if sort_by_perf_3:
        sorted_data = sorted_data.sort_values(by='Ticker', ascending=True)
        fig3 = px.bar(sorted_data, x='Ticker', y='Total_Performance', 
                     title='Performance Totale des Tickers de 2020 à 2023', 
                     color='Total_Performance',
                     color_continuous_scale="earth", 
                     width=1400)
    else:
        sorted_data = sorted_data.sort_values(by='Total_Performance', ascending=False)
        fig3 = px.bar(sorted_data, x='Ticker', y='Total_Performance', 
                     title='Performance Totale des Tickers de 2020 à 2023', 
                     color='Total_Performance',
                     color_continuous_scale="earth", 
                     width=1400)

    fig3.update_layout(coloraxis_showscale=False) 
    fig3.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', showgrid=True, gridwidth=1, gridcolor='white') 


    st.plotly_chart(fig3)

    sort_by_perf_4 = st.checkbox("Ordre alphabétique", key="sort_by_perf_4")

    if sort_by_perf_4:
        sorted_beta_data = sorted_beta_data.sort_values(by='Ticker', ascending=True)
        fig4 = px.bar(sorted_beta_data, x='Ticker', y='Annual_Beta', 
                     title='Performance Moyenne des Bêta de 2020 à 2023', 
                     color='Annual_Beta',
                     color_continuous_scale="earth", 
                     width=1400)
    else:
        sorted_beta_data = sorted_beta_data.sort_values(by='Annual_Beta', ascending=False)
        fig4 = px.bar(sorted_beta_data, x='Ticker', y='Annual_Beta', 
                     title='Performance Moyenne des Bêta de 2020 à 2023', 
                     color='Annual_Beta',
                     color_continuous_scale="earth", 
                     width=1400)

    fig4.update_layout(coloraxis_showscale=False) 
    fig4.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', showgrid=True, gridwidth=1, gridcolor='white')


    st.plotly_chart(fig4)



#----------------------------------------------------------------------------------------

elif option == 'Performance Cumulée et Distribution':
    st.markdown("<h1 style='text-decoration: underline;'>Performance cumulée et distribution des Bêta : 2020-2023</h1>", unsafe_allow_html=True)

    custom_markdown("""Dans cette section, vous trouverez divers graphiques. Pour mettre en évidence un ticker spécifique, double-cliquez sur son nom dans la légende. 
                Ensuite, vous pouvez sélectionner manuellement d'autres tickers si vous souhaitez les comparer. Dans le cadre de notre analyse, double-clique sur **MC.PA**.
        """, unsafe_allow_html=True)
    
    st.write()

    custom_markdown(""" 
    <u>**Interprétation :**</u><br>
                <br>
    Nous allons nous concentrer sur les deux derniers graphiques.<br>
                <li>Le premier (**distribution des Bêta par trimestres**) nous indique que sur les Bêta des 15 trimestres étudiées,  **11 sont supérieurs à 1.1**. <br>
                <li>Le deuxième (**distribution des Bêta par années**) nous indique que sur les 3.5 années étudiées, **3 sont supérieurs à 1.3**.<br>
                <br>
                Ces observations nous indiquent que l'action **MC.PA** est fréquemment plus volatile que le marché et rejoignent nos observations précédentes.<br>
                Rendez-vous à la section **Analyse de corrélation**.""", unsafe_allow_html=True)
    
    st.write()

    st.markdown(""" 

        """)

    st.plotly_chart(fig5)
    st.plotly_chart(fig6)
    st.plotly_chart(fig7)

#----------------------------------------------------------------------------------------

elif option == 'Évolution des Bêta':
    st.markdown("<h1 style='text-decoration: underline;'>Évolution des Bêta par Ticker sur Trois Ans</h1>", unsafe_allow_html=True)
    for group in groups_of_tickers:
        sub_data = final_tri_df[final_tri_df['Ticker'].isin(group)]
        fig8 = px.scatter(sub_data, x="Date", y="Quarterly_Beta", size="abs_Beta", color="Ticker",
                          hover_data=['Date'], width=1400, color_discrete_map=custom_color_map_8)
        
        fig8.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', showgrid=True, gridwidth=1, gridcolor='white')
    
        st.plotly_chart(fig8)
    
#----------------------------------------------------------------------------------------

elif option == 'Analyse de Corrélation':
    st.markdown("<h1 style='text-decoration: underline;'>Analyse de corrélation entre les Bêta et les performances trimestrielle par Ticker</h1>", unsafe_allow_html=True)
    st.write()
    custom_markdown("""Double-clique sur **MC.PA** (deuxième graphique)""", unsafe_allow_html=True)

    st.write()

    custom_markdown("""
        <h4><u>Interprétation</u>:</h4>
        <div style="text-align: center; margin-top: 20px; margin-bottom: 30px;">
            <table style="margin-left: auto; margin-right: auto;">
                <thead>
                    <tr>
                        <th>Caractéristique</th>
                        <th>2020-T2</th>
                        <th>2021-T1</th>
                        <th>2021-T3</th>
                        <th>2022-T1</th>
                        <th>2022-T4</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Bêta</strong></td>
                        <td>0.95</td>
                        <td>1.38</td>
                        <td>1.65</td>
                        <td>1.35</td>
                        <td>1.43</td>
                    </tr>
                    <tr>
                        <td><strong>Performance</strong></td>
                        <td>+20.283%</td>
                        <td>+10.935%</td>
                        <td>-6.597%</td>
                        <td>-11.163%</td>
                        <td>+11.826%</td> 
                    </tr>
                </tbody>
            </table>
        </div>
                <br>
        <p>Bien que la performance de MC.PA ait montré des variations significatives, il est clair que la valeur du Bêta n'est pas systématiquement en phase avec la performance de l'action. 
                Par exemple, malgré un Bêta élevé au 3ème trimestre 2021, l'action a connu une perte, tandis qu'au 1er trimestre 2020, un Bêta inférieur à 1 coïncidait avec une performance positive de +20%. 
        """, unsafe_allow_html=True)



    for group in groups_of_tickers:
        sub_data = final_tri_df[final_tri_df['Ticker'].isin(group)]
        sub_data = sub_data.round(3)
        
        fig9 = px.scatter(sub_data, x='Tri_Performance', y='Quarterly_Beta', color='Ticker',
                        size=sub_data["abs_Beta"].abs(),
                        custom_data=['Date', 'Ticker'], facet_col='Year', width=1400,
                        color_discrete_map=custom_color_map_9)
        
        fig9.update_traces(
            hovertemplate="<br>".join([
                "Performance: %{x}",
                "Bêta: %{y}",
                "Date: %{customdata[0]}",
                "Ticker: %{customdata[1]}"
            ])
        )
        
        fig9.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', showgrid=True, gridwidth=1, gridcolor='white')
        
        st.plotly_chart(fig9)





#----------------------------------------------------------------------------------------


#                                                          TEST STATISTIQUES

elif option == 'Test Statistique':
    st.markdown("<h1 style='text-decoration: underline;'>Tests statistiques : Pearson et Spearman</h1>", unsafe_allow_html=True)

    st.markdown("""
    
    Visuellement, aucune corrélation existe entre les performances des actions et leur Bêta. 
    Afin de valider cette hypothèse, nous allons procéder à des tests statistiques. Leurs résultats - couplés aux observations graphiques réalisées précédemment - nous permettront de conclure.
                
    Les 2 tests stastistique que nous allons utiliser sont les tests de Pearson et de Spearman.          
    **Pearson** mesure la relation **Linéaire** entre deux variables tandis que **Spearman** mesure la relation **Monotone**. 
                 
    Une valeur proche de 1 indique une forte corrélation positive, une valeur proche de -1 indique une forte corrélation négative, et une valeur proche de 0 indique une absence de corrélation linéaire.""", unsafe_allow_html=True)
                
    st.markdown("""
        Les analyses effectuées visent à éclaircir les points suivants :<br> 
        <li> Déterminer l'existence d'une corrélation entre les performances des actions et leur Bêta.
        <li> Identifier la nature de cette relation : est-elle **linéaire** ou **monotone** ?
        <li> Évaluer si les actions présentant des performances supérieures sont associées à un Bêta élevé (ou inversement).
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("<u><b>Test de Pearson</b></u>", unsafe_allow_html=True)

    st.markdown(""" 
                ```python 
                P = pearsonr(data['Perf_Tri_ticker'], data['Bêta'])

                Coefficient de corrélation de Pearson : 0.0065
                Valeur p (Pearson) : 0.8775""")
    
    
    st.markdown(""" 
                Remarque : 
                Il n'y a **pas de corrélation significative** entre les performances des actions et leur Bêta (valeur p = 0.8775 est bien supérieure à 0.05).
                La relation **n'est pas fortement linéaire** (coefficient de Pearson très proche de 0).
                Les données **ne montrent pas une tendance claire** des actions à haute performance ayant un Bêta élevé ou faible.""")

    st.write("")
    st.write("")

    st.markdown("<u><b>Test de Spearman</b></u>", unsafe_allow_html=True)

    st.markdown(""" 
                ```python 
                S = spearmanr(data['Perf_Tri_ticker'], data['Bêta'])

                Coefficient de corrélation de Spearman: -0.0142
                Valeur p : 0.7354""")

    st.write("")

    st.markdown(""" Remarque : 
                **Pas de corrélation significative** détectée.
                La relation est **faiblement** **monotone**.
                **Pas de tendance claire établie** entre les performances élevées et un Bêta élevé ou faible.
                """)

#----------------------------------------------------------------------------------------


elif option == 'Conclusion':
    st.markdown("<h1 style='text-decoration: underline;'>Conclusion</h1>", unsafe_allow_html=True)

    custom_markdown("""Après une analyse approfondie des performances et des Bêta des actions du CAC 40 de **janvier 2020 à août 2023**, avec une attention particulière portée à l'action MC.PA, plusieurs constatations majeures ont émergé.""", unsafe_allow_html=True)

    custom_markdown("""Premièrement, bien que le Bêta soit couramment utilisé comme un indicateur de la volatilité relative d'une action vis-à-vis du marché, nos observations suggèrent qu'il ne constitue **pas un prédicteur fiable** de sa **performance à venir**.
                Ceci est particulièrement flagrant pour l'action MC.PA : malgré des valeurs de Bêta élevées observées lors de certains trimestres, la performance effective de cette action n'était pas systématiquement en adéquation avec la volatilité attendue.
                Il convient de souligner que le Bêta est une mesure de la volatilité relative, et non une indication directe de la performance relative. Par exemple, bien que MC.PA ait nettement surpassé le marché, sa volatilité n'a pas systématiquement suivi cette tendance.""", unsafe_allow_html=True)

    st.markdown("""Deuxièmement, nos analyses statistiques, en utilisant à la fois les corrélations de **Pearson** et de **Spearman**, n'ont révélé **aucune corrélation notable**. 
                Cela conforte la notion selon laquelle le Bêta, bien qu'utile pour **évaluer la volatilité**, ne sert pas de prédicteur direct de la performance des actions.
                Il est crucial de garder à l'esprit que d'autres variables peuvent influencer la volatilité d'une action, sans nécessairement être liées à sa performance intrinsèque.""", unsafe_allow_html=True)

    st.markdown("""Pour conclure, il est indéniable que **la performance d'une action et son Bêta ne sont pas systématiquement corrélés**. 
                Dans le domaine de l'analyse financière, la prudence est de mise. Se reposer exclusivement sur le Bêta comme prédicteur de performance serait une démarche réductrice et pourrait conduire à des interprétations erronées.""", unsafe_allow_html=True)
    
    st.markdown("""***Cette analyse a été réalisée à des fins personnelles sans intention de conseil financier. Une action du CAC 40 a été délibérément exclue, par conséquent, bien que les résultats reflètent une tendance générale, ils ne doivent pas être considérés comme exacts.***""", unsafe_allow_html=True)



elif option == 'Code':

    st.markdown("<h1 style='text-decoration: underline;'>Aperçu du Code de l'Analyse</h1>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.write("""<u>**Collecte et Préparation des Données**</u> :""", unsafe_allow_html=True)

    code1 = """
    import yfinance as yf
    import pandas as pd
    import time

    tickers = ['AI.PA', 'AIR.PA', 'ALO.PA', 'MT.AS', 'CS.PA', 'BNP.PA', 'EN.PA', 'CAP.PA', 'CA.PA', 'ACA.PA', 'BN.PA', 'DSY.PA', 'ENGI.PA', 'EL.PA', 'ERF.PA', 'RMS.PA',
            'KER.PA', 'OR.PA', 'LR.PA', 'MC.PA', 'ML.PA', 'ORA.PA', 'RI.PA','PUB.PA', 'RNO.PA', 'SAF.PA', 'SGO.PA', 'SAN.PA', 'SU.PA', 'GLE.PA', 'STLAP.PA',
            'STMPA.PA', 'TEP.PA', 'HO.PA', 'TTE.PA', 'URW.PA', 'VIE.PA', 'DG.PA', 'VIV.PA', 'WLN.PA']

    all_data = pd.DataFrame()
    row_counter = 0

    for ticker in tickers:
            data = yf.download(ticker, start='2020-01-01', end='2023-08-29')
            data = data.reset_index()
            data.insert(0, 'Ticker', ticker)

            all_data = pd.concat([all_data, data], ignore_index=True)
            
            row_counter += 1

            if row_counter % 7 == 0:                   
                print(f"Processed {row_counter} rows.")
                clear_output(wait=True)
            time.sleep(0.0000001) 
    

    data_2020_copy = pd.read_csv("data_2020_copy.csv")
    data_2021_copy = pd.read_csv("data_2021_copy.csv")
    data_2022_copy = pd.read_csv("data_2022_copy.csv")
    data_2023_copy = pd.read_csv("data_2023_copy.csv")
    final_tri_df = pd.read_csv('final_tri_df.csv')
    Beta_years = pd.read_csv('Beta_years.csv')
    final_month_df = pd.read_csv('final_month_df.csv')
    all_data = pd.read_csv('all_data.csv')"""

    st.code(code1, language='python')

    st.write("")
    st.write("")

    st.write("""<u>**Analyse du Rendement Annuel par Action et Première Visualisation**</u> :""", unsafe_allow_html=True)

    code5 = """
    annual_performance_2 = all_data.groupby(['Year', 'Ticker']).apply(lambda x: ((x['Close'].iloc[-1] - x['Close'].iloc[0]) / x['Close'].iloc[0]) * 100).reset_index()
    annual_performance_2.columns = ['Year', 'Ticker', 'Annual_Performance']
    annual_performance_2['Annual_Performance'] = annual_performance_2['Annual_Performance'].round(2)
    
    years = annual_performance_2['Year'].unique()
    figs = {}
    for index, year in enumerate(years):
        data_for_year = annual_performance_2[annual_performance_2['Year'] == year]
        figs[year] = px.bar(data_for_year, x='Ticker', y='Annual_Performance', color='Annual_Performance',
                            labels={'Annual_Performance': 'Performance Annuelle (%)'},
                            color_continuous_scale="sunset", width = 1000) 

        figs[year].update_layout(
            title={
                'text': f"Performance {year}",
                'x': 0.2,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            margin=dict(t=130), 
            coloraxis_showscale=True if index == 0 else False 
        )
        figs[year].update_xaxes(title_text="")
        figs[year].update_yaxes(title_text="", showgrid=True, gridwidth=2, gridcolor='white', zeroline=True, zerolinewidth=3, zerolinecolor='white')

    col1, col2 = st.columns(2)
    col1.plotly_chart(figs[2020], use_container_width=True)
    col2.plotly_chart(figs[2021], use_container_width=True)

    col3, col4 = st.columns(2)
    col3.plotly_chart(figs[2022], use_container_width=True)
    col4.plotly_chart(figs[2023], use_container_width=True)"""

    st.code(code5, language='python')

    st.write("")
    st.write("")

    st.write("""<u>**Évaluation de la Performance du CAC40**</u> :""", unsafe_allow_html=True)

    code6 ="""
def calculate_cac40_annual_performance(df):
    start_price = df['Close_CAC40'].iloc[0]
    end_price = df['Close_CAC40'].iloc[-1]
    return ((end_price - start_price) / start_price) * 100

    perf_cac40_2020 = calculate_cac40_annual_performance(data_2020_copy)
    perf_cac40_2021 = calculate_cac40_annual_performance(data_2021_copy)
    perf_cac40_2022 = calculate_cac40_annual_performance(data_2022_copy)
    perf_cac40_2023 = calculate_cac40_annual_performance(data_2023_copy)

Resultat :

    Année 2020 : - 8.11%
    Année 2021 : + 27.98%
    Année 2022 : - 10.30%
    Année 2023 : + 11.07%
    """
    st.code(code6, language='python')

    st.write("")
    st.write("")

    st.write("""<u>**Rendement Composé du CAC40 sur 3.5 Ans**</u> :""", unsafe_allow_html=True)

    code7 ="""def compound_return(*returns):
    total_return = 1
    for r in returns:
        total_return *= (1 + r)
    return total_return - 1

returns = [-0.0811, 0.2798, -0.1030, 0.1107]
compound_performance = compound_return(*returns)
compound_performance

Résultat : Le rendement composé du CAC40 sur 3.5 ans est d'environ 17.17 %."""
    st.code(code7, language='python')



