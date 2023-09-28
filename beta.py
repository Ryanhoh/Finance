import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import plotly.subplots as sp
import pandas as pd
import numpy as np
import datetime 
from fonctions import render_table
from streamlit_lottie import st_lottie
import json

from fonctions import split_data_by_year,calculate_performance, calculate_annual_beta, generate_dual_plot, calculate_beta_over_period, add_annotations_to_bars
from fonctions import _SessionState, get_session_state, beta_histogram_annually, beta_histogram_annually, plot_beta_vs_performance, ticker_to_name


px.defaults.template = "plotly"  
st.set_page_config(layout="wide")

#primaryColor="#FF4B4B"
#backgroundColor="#233350"
#secondaryBackgroundColor="#505B75"
#textColor="#F2F2F3"
#font="sans serif"


company_name = pd.read_csv("company_name.csv")

pivot_data = pd.read_csv(
    "pivot_data.csv",
    parse_dates=['Date'],
    date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d'),
    index_col='Date'
)

annual_dataframes = split_data_by_year(pivot_data)
pivot_data = pivot_data.drop(columns=["Date.1"])

performance_2008_to_2012 = calculate_performance(annual_dataframes, 2008, 2012)
performance_2013_to_2017 = calculate_performance(annual_dataframes, 2013, 2017)
performance_2018_to_2023 = calculate_performance(annual_dataframes, 2018, 2023)
performance_2008_to_2023 = calculate_performance(annual_dataframes, 2008, 2023)

beta_2008_to_2012 = calculate_beta_over_period(annual_dataframes, 2008, 2012)
beta_2013_to_2017 = calculate_beta_over_period(annual_dataframes, 2013, 2017)
beta_2018_to_2023 = calculate_beta_over_period(annual_dataframes, 2018, 2023)
beta_2008_to_2023 = calculate_beta_over_period(annual_dataframes, 2008, 2023)

beta_2008 = calculate_annual_beta(annual_dataframes["df_all_2008"])
beta_2009 = calculate_annual_beta(annual_dataframes["df_all_2009"])
beta_2010 = calculate_annual_beta(annual_dataframes["df_all_2010"])
beta_2011 = calculate_annual_beta(annual_dataframes["df_all_2011"])
beta_2012 = calculate_annual_beta(annual_dataframes["df_all_2012"])
beta_2013 = calculate_annual_beta(annual_dataframes["df_all_2013"])
beta_2014 = calculate_annual_beta(annual_dataframes["df_all_2014"])
beta_2015 = calculate_annual_beta(annual_dataframes["df_all_2015"])
beta_2016 = calculate_annual_beta(annual_dataframes["df_all_2016"])
beta_2017 = calculate_annual_beta(annual_dataframes["df_all_2017"])
beta_2018 = calculate_annual_beta(annual_dataframes["df_all_2018"])
beta_2019 = calculate_annual_beta(annual_dataframes["df_all_2019"])
beta_2020 = calculate_annual_beta(annual_dataframes["df_all_2020"])
beta_2021 = calculate_annual_beta(annual_dataframes["df_all_2021"])
beta_2022 = calculate_annual_beta(annual_dataframes["df_all_2022"])
beta_2023 = calculate_annual_beta(annual_dataframes["df_all_2023"])

session_state = get_session_state(filtered=False)
selected_tickers = ["MC.PA", "AIR.PA", "RMS.PA", "CAP.PA", "BN.PA", "DSY.PA"]

combined_scale1 = px.colors.sequential.Sunset 
combined_scale2 = px.colors.sequential.Redor 
combined_scale3 = px.colors.sequential.Mint
combined_scale4 = px.colors.sequential.Tealgrn 

combined_scale5 = px.colors.sequential.Teal
combined_scale6 = px.colors.sequential.Mint 
combined_scale7 = px.colors.sequential.Darkmint
combined_scale8 = px.colors.sequential.Tealgrn 

color_scales = [combined_scale1, combined_scale2, combined_scale3, combined_scale4]
betas = [beta_2008_to_2012, beta_2013_to_2017, beta_2018_to_2023, beta_2008_to_2023]
performances = [performance_2008_to_2012, performance_2013_to_2017, performance_2018_to_2023, performance_2008_to_2023]

color_scale = [combined_scale5, combined_scale6, combined_scale7, combined_scale8]
period = ["2008-2012", "2013-2017", "2018-2023", "2008-2023"]


period_betas = [beta_2008_to_2012, beta_2013_to_2017, beta_2018_to_2023, beta_2008_to_2023]
periods = [
    (2008, 2012),
    (2013, 2017),
    (2018, 2023),
    (2008, 2023)
]

annual_betas = {}
for year in range(2008, 2024):
    beta_values = calculate_annual_beta(annual_dataframes[f"df_all_{year}"])
    annual_betas[year] = beta_values


action_et = {
    "Actions défensives": ["LVMH", "Hermes", "Danone"],
    "Actions offensives": ["Airbus", "Capgemini", "Dassault Systèmes"]
}

option = st.sidebar.radio(
    'Choisissez une page:',
    ('Sujet', 'Analyse des performances', 'Analyses des tendances', 'Analyse des relations' ,'Conclusion')
)

if option == "Sujet":
    st.markdown("<h2 style='text-decoration: underline;'>Analyse des Bêta et des performances des actions du CAC 40</h2>", unsafe_allow_html=True)
    st.write("")
    st.markdown("""

    L'étude s'étend du 1er janvier 2008 au 14 septembre 2023. Cette période englobe des moments charnières tels que la crise financière de 2008-2009, suivie de réglementations bancaires renforcées et de politiques monétaires assouplies. 
    Par ailleurs, une série de percées technologiques majeures, notamment dans les domaines de l'intelligence artificielle, de la blockchain, et de l'énergie renouvelable, ont remodelé les secteurs industriels et financiers entre 2010 et 2023. 
    Les tensions commerciales des années 2010, spécifiquement entre les États-Unis et la Chine, ont ajouté une dynamique d'incertitude. 
    La pandémie de COVID-19 en 2020 a perturbé l'économie mondiale, entraînant des récessions et une montée notable du MRO depuis 2022. Ces événements ont influencé les tendances du marché, justifiant une analyse approfondie des performances et de la volatilité des actifs durant cette temporalité.
    """, unsafe_allow_html=True)

    st.markdown(""" 
    Les données que nous avons étudiées proviennent de la bibliothèque **Yahoo Finance**, sélectionnée pour son vaste éventail d'informations financières, ses mises à jour régulières et sa fiabilité.               
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("<h4 style='text-decoration: underline;'>Problématiques</h4>", unsafe_allow_html=True) 
    st.write("")

    st.markdown("<h5>Comment le rendement des actions et leurs bêtas ont-ils évolué de 2008 à aujourd'hui ? Existe-t-il une relation observable entre ces deux indicateurs ?</h5>", unsafe_allow_html=True) 

    st.write("")
    
    st.markdown("""
            <li><strong>Évaluer les performances individuelles</strong> des entreprises en termes de <strong>rentabilité</strong>.</li>
            <li><strong>Analyser le Bêta de chaque entreprise et examiner sa distribution</strong> au fil de la période analysée.</li>
            <li><strong>Etudier la relation entre beta et performance</strong></li><br>
        """, unsafe_allow_html=True)
             

    st.markdown("<h4 style='text-decoration: underline;'>Remarques</h4>", unsafe_allow_html=True) 


    st.markdown("""
        Le Bêta est généralement calculé sur une période de 5 ans. Nous l'étudierons sur les tranches suivantes : 

        <table style="margin-left: 26px; border: 1px solid black;">
            <tr>
                <th>Temporalité</th>
            </tr>
            <tr>
                <td><strong>2008 - 2012</strong></td>
            </tr>
            <tr>
                <td><strong>2013 - 2017</strong></td>
            </tr>
            <tr>
                <td><strong>2018 - 2023</strong></td>
            </tr>
            <tr>
                <td><strong>2008 - 2023</strong></td>
            </tr>
        </table>
    """, unsafe_allow_html=True)



elif option == 'Analyse des performances':
    st.markdown("<h2 style='text-decoration: underline;'>Performances des actions et des Beta du 01-2008 au 09-2023</h2>", unsafe_allow_html=True)

    st.markdown("""
    Pour clarifier notre analyse, nous distinguerons deux types d'entreprises du CAC 40. 
    D'une part, nous avons les entreprises **défensives**. Celles-ci proposent généralement des biens et services de première nécessité, avec une demande stable face aux aléas économiques. 
    D'autre part, nous examinerons les entreprises **offensives**. Ces dernières opèrent souvent dans le secteur technologique et sont plus sensibles aux variations économiques.

    Les actions que nous analyserons sont les suivantes :""", unsafe_allow_html=True)

    st.markdown("")

    render_table()

    st.markdown("")
    st.markdown("")

    st.markdown(""" 
    Les graphiques ci-après illustrent à la fois les performances et les valeurs beta des actions du CAC40 sur des tranches d'années définies.<br>
    Ils offrent une analyse intégrée de ces deux indicateurs clés, éclairant leur interrelation au fil du temps.
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    periods = [
        (2008, 2012),
        (2013, 2017),
        (2018, 2023),
        (2008, 2023)
    ]

    if st.button('Filtrer les graphiques'):
        session_state.filtered = not session_state.filtered
    
    st.markdown("")

    if session_state.filtered:
        betas = [beta[beta.index.isin(selected_tickers)] for beta in betas]
        performances = [perf[perf.index.isin(selected_tickers)] for perf in performances]

    for i, (start, end) in enumerate(periods):

        if i == 0:
            st.markdown("""<h4 style='text-decoration: underline;'>Analyse 2008-2012</h2>""", unsafe_allow_html=True)
            st.markdown("""LVMH et Hermès, bien que défensives, ont allié forte performance à un bêta proche ou inférieur à 1, démontrant une croissance robuste avec une volatilité relative au marché. 
                     En revanche, Danone, malgré son faible bêta, n'a pas su capitaliser positivement.<br>
                        <br>
                        Airbus et Dassault Systèmes, malgré leur nature plus cyclique, ont démontré une croissance solide avec un bêta proche ou inférieur à 1. 
                     Capgemini, quant à elle, avec un bêta légèrement supérieur à 1, a connu une période plus difficile avec une performance en négatif.""", unsafe_allow_html=True)
        elif i == 1:
            st.markdown("""<h4 style='text-decoration: underline;'>Analyse 2013-2017</h2>""", unsafe_allow_html=True)
            st.markdown("""LVMH, avec un bêta de 1.02, et Hermès, doté d'un bêta de 0.59, ont affiché une solide performance pendant cette période, soulignant leur résilience et leur capacité à générer des rendements en dépit des fluctuations du marché. 
                     Danone, même avec un bêta modéré, a connu une croissance plus limitée. <br>
                     <br>
                     Du côté des entreprises à tendance cyclique, Airbus et Dassault Systèmes ont montré une forte croissance avec des bêtas inférieurs à 1, attestant de leur robustesse. 
                     Capgemini, malgré un bêta proche de 1, a surpassé avec une impressionnante augmentation de sa performance.""", unsafe_allow_html=True)

        elif i == 2:
            st.markdown("""<h4 style='text-decoration: underline;'>Analyse 2018-2023</h2>""", unsafe_allow_html=True)
            st.markdown("""LVMH et Hermès ont enregistré des croissances exceptionnelles, témoignant de la vigueur du secteur du luxe, même durant la crise. 
                    Danone, pour sa part, a rencontré des difficultés, bien que son bêta suggère une volatilité modérée par rapport au marché.<br>
                     <br>
                        Airbus, avec un bêta élevé de 1.51, illustre les conséquences tumultueuses de la crise du COVID-19 sur l'industrie aéronautique : les restrictions de mobilité ont entraîné d'importantes fluctuations dans ses performances.
                        Dassault Systèmes et Capgemini ont, en dépit des perturbations, montré une solidité remarquable.<br>
                     <br>
                     La pandémie a indéniablement façonné le paysage économique de ces entreprises, générant des défis et des opportunités inédits.
                    """, unsafe_allow_html=True)
            
        elif i == 3:
            st.markdown("""<h4 style='text-decoration: underline;'>Analyse 2008-2023</h2>""", unsafe_allow_html=True)
            st.markdown(""" LVMH et Hermès ont connu des croissances phénoménales au cours de ces 16 années, témoignant de la montée en puissance continue du secteur du luxe à l'échelle mondiale. 
                        Ces performances stellaires, conjuguées à des bêtas légèrement supérieurs à 0.6, indiquent une robustesse notable face aux turbulences du marché. 
                        Danone, malgré une performance plus modeste, présente également un bêta inférieur à 1, traduisant une relative stabilité dans son secteur.<br>
                        <br>
                        Dans le segment plus cyclique, Airbus a navigué avec succès à travers de multiples défis, y compris la crise financière de 2008 et la pandémie de COVID-19, ce qui est reflété par son bêta de 1.1 et sa performance. 
                        Capgemini et Dassault Systèmes ont tous deux démontré une capacité remarquable à capitaliser sur la révolution technologique et numérique, affichant des croissances solides avec des bêtas proches de 1.<br>
                        <br>
                        Sur cette période de 2008 à 2023, le marché a été témoin d'événements majeurs tels que la crise financière mondiale, l'émergence rapide des technologies numériques, et bien sûr, la pandémie de COVID-19. 
                        Ces événements ont influencé le comportement du bêta des entreprises. La crise financière a mis en évidence la résilience des marques de luxe, tandis que la transformation digitale a favorisé les acteurs technologiques. 
                        La pandémie, quant à elle, a accentué la bifurcation avec certains secteurs comme l'aéronautique subissant des chocs importants, tandis que d'autres, notamment le luxe, ont rebondi avec vigueur post-crise.<br>
                        (x 21.29 pour Hermes...)
                        """, unsafe_allow_html=True)

        fig = generate_dual_plot(betas[i], performances[i]*100, f"{start}-{end}", color_scales[i])
        if session_state.filtered:
            add_annotations_to_bars(fig)
        st.plotly_chart(fig)

if option == "Analyses des tendances":

    annual_hist_all = beta_histogram_annually(annual_betas, color_scale='Bluyl', show_counts=True)
    annual_hist_sel = beta_histogram_annually(annual_betas, selected_tickers, color_scale='Tealgrn', show_counts=True, custom_title='Beta : Distributions des 6 actions par année')


    st.markdown("""<h2 style='text-decoration: underline;'>Analyse de la Volatilité Annuelle</h2>""", unsafe_allow_html=True)

    st.markdown(" ")
    st.markdown("""Ce graphique détaille la distribution des bêtas sur les 16 années étudiées.<br>
                Les barres représentent différents intervalles de bêta, et le nombre (count) affiché sur chaque barre représente le nombre d'années où l'entreprise a enregistré un bêta moyen dans cet intervalle.<br>
                Il permet d'évaluer rapidement la tendance de volatilité d'une action par rapport au marché sur l'ensemble de la temporalité étudiée.""", unsafe_allow_html=True)

    st.plotly_chart(annual_hist_all)

    st.markdown("""<h4 style='text-decoration: underline;'>Analyse ciblée</h4>""", unsafe_allow_html=True)
    st.markdown(" ")

    st.markdown("""
        <ul>
        <li><b><u>Dassault Systèmes</u></b> montre une volatilité qui varie sur différents intervalles. Cette variabilité peut refléter les innovations et les cycles de produits dans le secteur du logiciel et des services technologiques.</li><br>
        <li><b><u>LVMH</u></b> affiche une volatilité parfois supérieure à celle du marché, ce qui n'est pas surprenant pour une marque de luxe. Les produits de luxe peuvent connaître des périodes de forte demande, mais aussi des périodes de ralentissement en fonction des tendances et de l'économie mondiale.</li><br>
        <li><b><u>Hermes</u></b> présente une volatilité souvent inférieure à celle du marché. Cela pourrait indiquer une clientèle fidèle et une demande stable.</li>
        </ul>
    """, unsafe_allow_html=True)


    st.plotly_chart(annual_hist_sel)

    st.markdown("""
        <ul>
        <li><b><u>Airbus</u></b> présente une volatilité souvent proche de celle du marché, indiquant que son comportement en termes de prix suit généralement les tendances du marché global. 
                Cela peut signifier que les investissements dans Airbus reflètent les tendances générales de l'industrie aéronautique.</li><br>
        <li><b><u>Danone</u></b> se distingue par sa stabilité relative, avec une volatilité généralement inférieure à celle du marché. 
                Cela peut s'expliquer par la nature de ses produits de base qui sont moins sujets aux fluctuations rapides du marché.</li><br>
        <li><b><u>Capgemini</u></b>  tend à suivre de près les mouvements du marché. 
                Son profil de volatilité suggère qu'elle est susceptible de connaître des périodes d'augmentation rapide de la valeur, mais aussi des périodes de baisse.</li>
        </ul>
    """, unsafe_allow_html=True)


if option == "Analyse des relations":
    periods = ["2008-2012", "2013-2017", "2018-2023", "2008-2023"]

    st.markdown("<h2 style='text-decoration: underline;'>Étude de corrélation entre les performances et les bêta</h2><br>", unsafe_allow_html=True)

    st.markdown("""Ces graphiques dépeignent la relation entre le risque relatif d'une entreprise, représenté par le Bêta, et sa performance au fil du temps.<br>
                Ils permettent d'identifier rapidement des **"anomalies"** et de comparer les comportements d'entreprises sur différentes périodes.<br>
                La **droite de régression** offre en outre un repère visuel de la tendance générale de cette relation.""", unsafe_allow_html=True)

    for i, (beta, performance, period, scale) in enumerate(zip(betas, performances, periods, color_scale)):
        if i == 0:
            st.markdown("""<h4 style='text-decoration: underline;'>Analyse 2008-2012</h4>""", unsafe_allow_html=True)
            st.markdown("""<br>Au cours de la période 2008-2012, une tendance générale a émergé pour les actions du CAC40 : à mesure que le bêta augmentait, la performance tendait à diminuer. 
                        Cela est particulièrement notable par la pente descendante de la droite de régression. 
                        Les actions avec un faible bêta, généralement considérées comme moins risquées, ont montré une grande variabilité dans leurs rendements, s'écartant parfois considérablement de cette droite.
                        Cette variabilité a probablement été influencée par la crise financière mondiale de 2008 et les tensions commerciales entre les États-Unis et la Chine autour de 2010, mettant en lumière l'impact de facteurs externes sur leur performance durant cette période. """, unsafe_allow_html=True)
        elif i == 1:
            st.markdown("""<h4 style='text-decoration: underline;'>Analyse 2013-2017</h4>""", unsafe_allow_html=True)
            st.markdown("""<br>Durant la période 2013-2017, la majorité des actions du CAC40 a affiché des performances positives. 
                        Toutefois, l'observation des points par rapport à la droite de régression révèle une dynamique fluctuante. Alors que certaines plages de bêta montrent des actions se rapprochant de cette droite, indiquant 
                        une relation typique entre risque et rendement, d'autres tranches montrent des écarts plus prononcés. 
                        Ces variations pourraient être influencées par divers événements économiques et politiques. Par exemple, les incertitudes liées au vote du Brexit en 2016 ont pu introduire des volatilités sur certains segments du marché. 
                        De même, la reprise économique post-crise financière a pu bénéficier à certains secteurs plus que d'autres, influençant ainsi leur performance relative au bêta.""", unsafe_allow_html=True)
        elif i == 2:
            st.markdown("""<h4 style='text-decoration: underline;'>Analyse 2018-2023</h4>""", unsafe_allow_html=True)
            st.markdown("""<br>Durant la période 2018-2023, marquée par les répercussions de la pandémie de la COVID-19, la relation entre le bêta et la performance des actions du CAC40 s'est avérée subtile, avec une droite de régression presque horizontale. 
                        Cette tendance suggère qu'il y avait une corrélation très faible, voire inexistante, entre le risque systématique (bêta) et la performance des actions durant ces années perturbées. 
                        Au cours de la période marquée par la pandémie, bien que de nombreuses entités aient navigué à travers des turbulences économiques, des entreprises telles que LVMH et Hermès ont brillé par leur résilience. 
                        Leur progression remarquable est principalement attribuable à une demande soutenue en provenance du marché asiatique. 
                        Enfin, la concentration des points autour de la droite de régression témoigne d'une stabilité relative, probablement favorisée par les interventions stratégiques des banques centrales et des dispositifs gouvernementaux.""", unsafe_allow_html=True)

        elif i == 3:
            st.markdown("""<h4 style='text-decoration: underline;'>Analyse 2008-2023</h4>""", unsafe_allow_html=True)
            st.markdown("""Au cours de la période étendue de 2008 à 2023, une corrélation négative se dégage entre le bêta et la performance des actions du CAC40. 
                        Bien que la majorité des actions se positionnent entre un bêta de 0,6 et 1,2, leur rapprochement de la droite de régression en montre une relation risque-rendement manifeste. 
                        Hermès, avec un bêta de 0.65, a enregistré une performance astronomique de 2130%, faisant preuve de sa singularité dans cet ensemble. 
                        Cette tendance générale suggère qu'en dépit des chocs économiques de cette période, la relation entre risque systématique et rendement est toujours centrale, mais elle est nuancée par des outliers comme Hermès. 
                        En somme, à mesure que le risque systématique augmente, la performance a tendance à diminuer, mais des exceptions notables et d'autres facteurs sous-jacents influencent également le paysage des rendements.""", unsafe_allow_html=True)
            
        fig = plot_beta_vs_performance(beta, performance, period, scale)
        st.plotly_chart(fig)

if option == "Conclusion":

    st.markdown("""<h2 style='text-decoration: underline;'>Problématiques : </h2>""", unsafe_allow_html=True)

    st.markdown("""<h4>Comment le rendement des actions et leurs bêtas ont-ils évolué de 2008 à aujourd'hui ? 
            Existe-t-il une relation observable entre ces deux indicateurs ?</h4>""", unsafe_allow_html=True)
    
    st.markdown("""<h4 style='text-decoration: underline;'>Analyse globle</h4>""", unsafe_allow_html=True)

    st.markdown("""
    Depuis 2008 jusqu'à 2023, d'importants bouleversements politico-économiques ont influencé la relation entre la performance des actions et leur bêta. 
    La majorité des actions examinées ont connu des performances positives robustes, avec des rendements oscillant entre **+3 % et +2130 %**. 
    Notamment, six d'entre elles ont dépassé une performance de +500 %, avec Hermes qui s'est particulièrement distingué par sa surperformance sur le marché. 
    À l'opposé, un tiers des entreprises étudiées, représentant 13 entreprises, ont enregistré des rendements négatifs situés entre **-6.13 % et -77.15 %**.          
    <br>
    Nous avons identifié une corrélation négative entre les indicateurs examinés, qui est toutefois tempérée par des événements marquants tels que la crise financière, le Brexit et la pandémie de COVID-19. 
    Traditionnellement, un bêta supérieur à 1 suggère une volatilité supérieure à celle du marché (et donc un risque plus élevé), tandis qu'un bêta inférieur à 1 indique une volatilité moindre. 
    Cependant, nos analyses révèlent des exceptions à cette théorie générale.
    
    En effet, pour de nombreuses entreprises ayant un bêta entre 0,6 et 1, une droite de régression décroissante apparaît au-dessus des points du graphique, indiquant une performance inférieure malgré un risque moindre. 
    Des entreprises comme Thales, Orange et Sanofi illustrent cette tendance. Néanmoins, cette généralisation n'est pas universelle. 
    Par exemple, Dassault, Eurofins Scientific et Teleperformance ont affiché des performances positives notables avec un bêta situé entre 0.6 et 0.8. 
    Étonnamment, la droite de régression tend à coïncider avec des points lorsque le bêta se situe entre 1,1 et 1,45. 
    Cela nous incite à repenser l'idée conventionnelle selon laquelle risque et rendement sont toujours directement proportionnels, soulignant une complexité potentielle dans certains intervalles de bêta.
    <br> """, unsafe_allow_html=True)

    st.markdown("""<h4 style='text-decoration: underline;'>Analyse ciblée</h4>""", unsafe_allow_html=True)
                
    st.markdown("""Concernant les 6 entreprises que nous avons selectionné dans cette analyse, les observations sont interressantes.
    Les 3 entreprises "défensives", LVMH, Hermes et Danone n'ont pas suivi la même tendance en terme de performance mais aussi en terme de volatilité.
    Hermes à surperformé à hauteur de + 2130 % avec un beta de 0.657. Danone a faiblement performé avec une performance de -7 % et un beta de 0.61. Enfin, 
    LVMH a connu une augmentation de + 873% pour un beta de 1.04.<br>     
    C'est aussi le cas pour les 3 entreprise "offensives" : Dassault, Capgemini et Airbus.
    Dassault a surpris avec une forte performance de + 808 % et un beta de 0.653. Capgemini et Airbus, avec des performances respectives de + 295% et + 519% et des beta de 1.008 et 1.103.
    Il ressort de notre analyse que, contrairement aux attentes conventionnelles, la classification des entreprises en tant que "défensives" ou "offensives" ne prévoit pas nécessairement leur performance ou leur volatilité.
    Par exemple, bien que Hermes et Danone soient tous deux considérés comme "défensifs", ils affichent des performances très différentes malgré des betas similaires.<br>
    Cette variabilité souligne la complexité intrinsèque de la relation entre le risque (représenté par le beta) et la performance, et suggère que des facteurs spécifiques à chaque entreprise influencent également leurs trajectoires financières.
    """, unsafe_allow_html=True)

    


def load_lottie_file(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)

st.sidebar.markdown("""
    <style>
        .st-ae { margin-bottom: 20px; }  /* Ajuste l'espace entre les options */
        .spacer { height: 30vh; }  /* Cette classe est utilisée pour pousser le contenu vers le bas */
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    lottie_github = load_lottie_file('Anim - Github.json')

    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st_lottie(lottie_github, width=90, height=80, speed=5)

    with col2:
        st.markdown(
            """
            <div style="text-align: right; vertical-align: middle; height: 80px; display: flex; align-items: center; justify-content: flex-end; padding-right: 85px;">
                <a href="https://github.com/Ryanhoh/Finance.git" target="_blank" style="text-decoration: none; font-size: 14px;">Ryanh.o.git</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    lottie_linkedin = load_lottie_file('Anim - Link.json')

    
    col3, col4 = st.columns([1, 2])
    
    with col3:
        st.markdown('<div style="padding-left:20px;">', unsafe_allow_html=True)
        st_lottie(lottie_linkedin, width=70, height=60, speed=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown(
            """
            <div style="text-align: right; vertical-align: middle; height: 85px; display: flex; align-items: center; justify-content: flex-end; padding-right: 70px;">
                <a href="https://www.linkedin.com/in/ryan-ouanane/" target="_blank" style="text-decoration: none; font-size: 14px;">Ryan.LinkedIn</a>
            </div>
            """,
            unsafe_allow_html=True
        )







