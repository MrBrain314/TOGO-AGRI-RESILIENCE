# -*- coding: utf-8 -*-
"""
RESILIENCE AGRI-TOGO - Dashboard analytique
Data Challenge Agriculture - Defi 2 | Togo AI Lab
Auteur : OURO-TAGBA Bastou
"""

import os
import re
import math

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster, FastMarkerCluster
from streamlit_folium import st_folium

# ------------------------------------------------------------------
# CONFIGURATION GENERALE
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Résilience Agri-Togo | Défi 2",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

# Palette du theme "Vert Togo & Jaune" (style institutionnel)
C_DEEP = "#0B5D26"      # vert fonce (bandeaux)
C_EMERALD = "#1E8A3C"   # vert Togo
C_GOLD = "#F2C500"      # jaune vif
C_GOLD_L = "#FFD84D"    # jaune clair
C_CREAM = "#F2F3F5"     # gris clair (fond)
C_INK = "#1C1C1C"       # encre
C_RED = "#C0392B"       # alerte
C_BLUE = "#2E86C1"      # eau

PALETTE = [C_EMERALD, C_GOLD, C_BLUE, C_RED, "#5D9C6B", "#8E7CC3"]

# ------------------------------------------------------------------
# STYLE
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.stApp { background: #F2F3F5; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E8A3C 0%, #0B5D26 100%);
    margin: 16px;
    border-radius: 24px;
    height: calc(100vh - 32px);
    box-shadow: 8px 8px 20px rgba(0,0,0,.20);
    width: 280px !important;
    min-width: 280px !important;
}
section[data-testid="stSidebar"] .stMarkdown ul {
    list-style: none;
    padding-left: 0;
    text-align: center;
}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown em {
    text-align: center;
}
section[data-testid="stSidebar"] .stCheckbox {
    margin-left: 42px;
}
section[data-testid="stSidebar"] > div {
    height: 100%;
    overflow-y: auto;
}
section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * { color: #1C1C1C !important; }
section[data-testid="stSidebar"] img {
    background: #FFFFFF; border-radius: 50%; padding: 8px;
    border: 6px solid #F2C500;
    box-shadow: 0 6px 16px rgba(0,0,0,.35);
}
section[data-testid="stSidebar"] .stCheckbox label {
    padding: 3px 10px; border-radius: 8px; margin-bottom: 1px;
}
section[data-testid="stSidebar"] .stCheckbox label:has(input:checked) p {
    color: #F2C500 !important; font-weight: 700;
}

.hero {
    background: linear-gradient(120deg, #0B5D26 0%, #1E8A3C 100%);
    border-radius: 16px;
    padding: 18px 30px 16px 30px;
    margin-bottom: 30px;
    box-shadow: 0 6px 18px rgba(11,93,38,.30);
}
.hero h1 {
    font-family: 'Poppins', sans-serif;
    color: #F2C500;
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 0 5px 0;
    letter-spacing: .2px;
}
.hero .gold { color: #FFFFFF; }
.hero p { color: #EAF5EC; font-size: .9rem; margin: 0; max-width: 950px; font-weight: 400; }
.hero p b { color: #FFD84D; }
.hero .badge {
    display: inline-block; margin-top: 10px;
    background: #F2C500; border: none;
    color: #0B5D26; padding: 4px 14px; border-radius: 999px;
    font-size: .72rem; font-weight: 700; letter-spacing: .8px;
}
.hero .badge-author {
    display: inline-block; margin-top: 10px;
    background: transparent; border: 1.5px solid #F2C500;
    color: #F2C500; padding: 4px 14px; border-radius: 999px;
    font-size: .72rem; font-weight: 500; letter-spacing: .5px;
}
.hero .badge-author b { color: #FFD84D; }

.kpi {
    background: linear-gradient(145deg, #E3E5E8 0%, #F6F7F8 45%, #FDFDFD 100%);
    border-radius: 24px;
    padding: 14px 12px;
    border: none;
    box-shadow: 8px 8px 18px rgba(0,0,0,.16),
                -6px -6px 14px rgba(255,255,255,1),
                inset 4px 4px 10px rgba(0,0,0,.10),
                inset -4px -4px 10px rgba(255,255,255,.95);
    height: 122px;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    text-align: center;
    overflow: hidden;
}
.kpi .v {
    font-family: 'Poppins', sans-serif;
    font-size: 1.8rem; font-weight: 800; color: #0B5D26; line-height: 1.15;
}
.kpi .l { font-size: .8rem; color: #1C1C1C; font-weight: 700; margin-top: 2px; line-height: 1.2; }
.kpi .s { font-size: .72rem; color: #6B6B6B; margin-top: 3px; font-weight: 500; }

.reco {
    background: linear-gradient(145deg, #F8F9FA 0%, #E7E9EC 100%);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 6px 6px 14px rgba(0,0,0,.12), -4px -4px 10px rgba(255,255,255,.95);
    height: 230px;
}
.reco .l { font-size: .95rem; color: #0B5D26; font-weight: 700; margin-bottom: 6px; }
.reco .s { font-size: .82rem; color: #444444; line-height: 1.45; }

h2, h3, h4 { font-family: 'Poppins', sans-serif !important; color: #0B5D26 !important; font-weight: 700 !important; }

.section-note {
    background: #0B5D26;
    border-radius: 12px; padding: 13px 20px;
    color: #FFFFFF; font-size: .92rem;
    margin-bottom: 28px;
    box-shadow: 0 4px 10px rgba(11,93,38,.25);
}
.section-note b { color: #F2C500; }

.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: #D9DCE0; border-radius: 10px;
    border: none;
    padding: 9px 18px; color: #3A3A3A; font-weight: 600;
    box-shadow: 2px 2px 6px rgba(0,0,0,.12);
}
.stTabs [aria-selected="true"] {
    background: #0B5D26 !important; color: #FFFFFF !important;
    box-shadow: inset 3px 3px 7px rgba(0,0,0,.40), inset -2px -2px 5px rgba(255,255,255,.12);
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* Conteneurs de contenu : meme langage neumorphique doux */
[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, #FBFCFC 0%, #EDEFF1 100%);
    border-radius: 18px;
    padding: 12px 0;
    box-shadow: 6px 6px 14px rgba(0,0,0,.12), -4px -4px 10px rgba(255,255,255,.95);
    overflow: hidden;
}
[data-testid="stDataFrame"] {
    background: linear-gradient(145deg, #FBFCFC 0%, #EDEFF1 100%);
    border-radius: 18px;
    padding: 12px;
    box-shadow: 6px 6px 14px rgba(0,0,0,.12), -4px -4px 10px rgba(255,255,255,.95);
}
iframe[title="streamlit_folium.st_folium"] {
    border-radius: 18px;
    box-shadow: 6px 6px 14px rgba(0,0,0,.12), -4px -4px 10px rgba(255,255,255,.95);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# OUTILS GEOMETRIE (WKT sans geopandas)
# ------------------------------------------------------------------
def extract_centroid(geom_str):
    """Extrait un point representatif (lat, lon) d'une geometrie WKT."""
    if not isinstance(geom_str, str):
        return None, None
    m = re.search(r'POINT\s*\(([0-9.\-]+)\s+([0-9.\-]+)\)', geom_str)
    if m:
        return float(m.group(2)), float(m.group(1))
    coords = re.findall(r'([0-9.\-]+)\s+([0-9.\-]+)', geom_str)
    if coords:
        lons = [float(c[0]) for c in coords]
        lats = [float(c[1]) for c in coords]
        return sum(lats) / len(lats), sum(lons) / len(lons)
    return None, None


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def norm01(s):
    """Normalisation min-max robuste d'une serie."""
    if s.max() == s.min():
        return pd.Series(0.5, index=s.index)
    return (s - s.min()) / (s.max() - s.min())


def plot(fig):
    """Affiche un graphique Plotly avec titre centre et taille uniforme."""
    if fig.layout.title.text:
        fig.update_layout(title_x=0.5, title_xanchor="center", title_font_size=15)
    st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------------
# CHARGEMENT DES DONNEES
# ------------------------------------------------------------------
@st.cache_data(show_spinner="Chargement des données...")
def load_data():
    def read(name):
        df = pd.read_csv(os.path.join(DATA_DIR, name), encoding="utf-8")
        if "geometry" in df.columns:
            pts = df["geometry"].apply(extract_centroid)
            df["lat"] = pts.apply(lambda t: t[0])
            df["lon"] = pts.apply(lambda t: t[1])
        return df

    elevage = read("elevage_etablissements.csv")
    abattoirs = read("abattoirs.csv")
    pisci = read("zones_pisciculture.csv")
    retenues = read("retenues_eau.csv")
    digues = read("digues_barrages.csv")
    # Fusion en memoire des 4 indicateurs Banque mondiale (1 fichier par source)
    wb = None
    for fname in ["va_agricole_pct_pib.csv", "va_agricole_croissance.csv",
                  "va_agricole_usd_2015.csv", "va_agricole_par_travailleur.csv"]:
        d = pd.read_csv(os.path.join(DATA_DIR, fname))
        wb = d if wb is None else wb.merge(d, on="annee", how="outer")
    wb = wb.sort_values("annee").reset_index(drop=True)
    rural = pd.read_csv(os.path.join(DATA_DIR, "agriculture_dev_rural.csv"))
    return elevage, abattoirs, pisci, retenues, digues, wb, rural


@st.cache_data(show_spinner=False)
def build_canton_index(elevage, abattoirs, pisci, retenues, digues):
    """Construit l'Indice de Resilience Agricole Territoriale (IRAT) par canton."""
    keys = ["region_nom_bdd", "prefecture_nom_bdd", "canton_nom_bdd"]

    def count_by(df, col):
        d = df.dropna(subset=["canton_nom_bdd"]).groupby(keys).size()
        return d.rename(col)

    base = pd.concat([
        count_by(elevage, "n_elevage"),
        count_by(pisci, "n_pisci"),
        count_by(retenues, "n_retenues"),
        count_by(digues, "n_digues"),
        count_by(abattoirs, "n_abattoirs"),
    ], axis=1).fillna(0).reset_index()

    # Centroide approximatif du canton = moyenne des points d'elevage (ou autres actifs)
    pts = pd.concat([
        elevage[keys + ["lat", "lon"]],
        retenues[keys + ["lat", "lon"]],
        pisci[keys + ["lat", "lon"]],
    ]).dropna()
    cent = pts.groupby(keys)[["lat", "lon"]].mean().reset_index()
    base = base.merge(cent, on=keys, how="left")

    # Distance au plus proche abattoir
    ab = abattoirs.dropna(subset=["lat", "lon"])
    def dist_ab(row):
        if pd.isna(row["lat"]):
            return None
        return min(haversine_km(row["lat"], row["lon"], a.lat, a.lon) for a in ab.itertuples())
    base["dist_abattoir_km"] = base.apply(dist_ab, axis=1)

    # ---- Composantes de l'indice (0 a 1) ----
    base["score_eau"] = norm01(base["n_retenues"] + base["n_digues"])
    base["score_abattoir"] = 1 - norm01(base["dist_abattoir_km"].fillna(base["dist_abattoir_km"].max()))
    base["score_diversification"] = norm01(base["n_pisci"])
    # Encadrement : infrastructures d'eau disponibles par etablissement d'elevage
    ratio = (base["n_retenues"] + base["n_digues"]) / base["n_elevage"].clip(lower=1)
    base["score_encadrement"] = norm01(ratio.clip(upper=ratio.quantile(0.95)))

    # ---- IRAT : indice composite pondere ----
    base["IRAT"] = (
        0.35 * base["score_eau"]
        + 0.25 * base["score_abattoir"]
        + 0.20 * base["score_diversification"]
        + 0.20 * base["score_encadrement"]
    ).round(3)

    # ---- Priorite d'investissement : forte activite x faible resilience ----
    base["score_priorite"] = (norm01(base["n_elevage"]) * (1 - base["IRAT"])).round(3)

    base["statut"] = pd.cut(
        base["IRAT"], bins=[-0.01, 0.25, 0.45, 1.01],
        labels=["Vulnérable", "Intermédiaire", "Résilient"]
    )
    return base


elevage, abattoirs, pisci, retenues, digues, wb, rural = load_data()
canton = build_canton_index(elevage, abattoirs, pisci, retenues, digues)

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    logo_path = os.path.join(BASE_DIR, "images", "LOGO.jpg")
    if os.path.exists(logo_path):
        cols = st.columns([1.5, 4, 1.5])
        with cols[1]:
            st.image(logo_path, width=170)
    st.markdown("## Résilience Agri-Togo")
    st.markdown("*Défi 2 - Togo AI Lab*")
    st.markdown("---")

    st.markdown("**Région**")
    regions = sorted(canton["region_nom_bdd"].dropna().unique())
    tout = st.checkbox("Tout cocher", value=True)
    sel_regions = []
    for r in regions:
        if st.checkbox(r, value=True, key=f"reg_{r}", disabled=tout):
            sel_regions.append(r)
    if tout:
        sel_regions = list(regions)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center'>"
        "<p><b>Sources</b></p>"
        "<p style='margin:0'>geodata.gouv.tg</p>"
        "<p style='margin:0'>opendata.gouv.tg</p>"
        "<p style='margin:0 0 16px 0'>Banque mondiale</p>"
        "<p><b>Auteur</b></p>"
        "<p style='margin:0'>OURO-TAGBA Bastou</p>"
        "</div>",
        unsafe_allow_html=True
    )

def freg(df):
    if len(sel_regions) == len(regions):
        return df
    return df[df["region_nom_bdd"].isin(sel_regions)]

canton_f = freg(canton)
elevage_f, abattoirs_f = freg(elevage), freg(abattoirs)
pisci_f, retenues_f, digues_f = freg(pisci), freg(retenues), freg(digues)

# ------------------------------------------------------------------
# EN-TETE
# ------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
  <h1>Résilience agricole <span class="gold">&</span> performance des territoires</h1>
  <p>Où les infrastructures agricoles du Togo soutiennent-elles réellement l'économie locale,
  et où investir en priorité ? Réponse avec l'<b>Indice de Résilience Agricole Territoriale (IRAT)</b>, calculé par canton.</p>
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
    <span class="badge">DATA CHALLENGE AGRICULTURE - DÉFI 2 &nbsp;|&nbsp; TOGO AI LAB</span>
    <span class="badge-author">Développé par <b>Bastou OURO-TAGBA</b></span>
  </div>
</div>
""", unsafe_allow_html=True)

# KPIs
n_vuln = int((canton_f["statut"] == "Vulnérable").sum())
k1, k2, k3, k4, k5 = st.columns(5)
for col, val, lab, sub in [
    (k1, f"{len(elevage_f):,}".replace(",", " "), "Établissements d'élevage", "Actifs recensés"),
    (k2, f"{len(retenues_f) + len(digues_f):,}".replace(",", " "), "Ouvrages d'eau", f"{len(retenues_f)} retenues, {len(digues_f)} digues"),
    (k3, str(len(abattoirs_f)), "Abattoirs", "Établissements"),
    (k4, str(canton_f["canton_nom_bdd"].nunique()), "Cantons analysés", "Mailles territoriales"),
    (k5, str(n_vuln), "Cantons vulnérables", "IRAT inférieur à 0,25"),
]:
    col.markdown(f'<div class="kpi"><div class="v">{val}</div><div class="l">{lab}</div><div class="s">{sub}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# ONGLETS
# ------------------------------------------------------------------
tabs = st.tabs([
    "🗺️ Vue d'ensemble",
    "🧭 Indice de résilience",
    "💧 Accès à l'eau",
    "🥩 Élevage & abattoirs",
    "📈 Économie agricole",
    "🎯 Zones prioritaires",
])

# ================= TAB 1 : VUE D'ENSEMBLE =================
with tabs[0]:
    st.markdown('<div class="section-note">Carte générale des infrastructures agricoles. '
                'Les cercles numérotés regroupent les points proches : vert = peu, jaune = moyen, orange = beaucoup.</div>',
                unsafe_allow_html=True)

    center = [8.6, 1.0]
    if len(sel_regions) < len(regions) and not elevage_f["lat"].dropna().empty:
        center = [elevage_f["lat"].mean(), elevage_f["lon"].mean()]
    m = folium.Map(location=center, zoom_start=7, tiles="CartoDB positron")

    # Couches volumineuses : FastMarkerCluster (clustering cote navigateur, tres rapide)
    fast_layers = [
        (elevage_f, "Élevage"),
        (retenues_f, "Retenues d'eau"),
        (digues_f, "Digues & barrages"),
    ]
    for df, name in fast_layers:
        pts = df.dropna(subset=["lat", "lon"])[["lat", "lon"]].values.tolist()
        fg = folium.FeatureGroup(name=name)
        FastMarkerCluster(pts).add_to(fg)
        fg.add_to(m)

    # Couches legeres : marqueurs individuels avec popup
    detail_layers = [
        (abattoirs_f, "Abattoirs", C_RED),
        (pisci_f, "Pisciculture", C_BLUE),
    ]
    for df, name, color in detail_layers:
        fg = folium.FeatureGroup(name=name)
        mc = MarkerCluster()
        for r in df.dropna(subset=["lat", "lon"]).itertuples():
            folium.CircleMarker(
                [r.lat, r.lon], radius=5, color=color, fill=True,
                fill_opacity=0.85, weight=1,
                popup=f"{name}<br>{getattr(r, 'prefecture_nom_bdd', '')} / {getattr(r, 'canton_nom_bdd', '')}",
            ).add_to(mc)
        mc.add_to(fg)
        fg.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    legend = f"""
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;
         padding:10px 14px;border-radius:8px;box-shadow:2px 2px 6px rgba(0,0,0,.3);font-size:12px;">
    <b>Légende</b><br>
    <span style="color:{C_EMERALD}">●</span> Élevage &nbsp;
    <span style="color:{C_RED}">●</span> Abattoirs<br>
    <span style="color:{C_BLUE}">●</span> Pisciculture &nbsp;
    <span style="color:#4C93B8">●</span> Retenues d'eau<br>
    <span style="color:#7A6FA8">●</span> Digues & barrages
    </div>"""
    m.get_root().html.add_child(folium.Element(legend))
    st_folium(m, height=560, use_container_width=True, returned_objects=[])

    c1, c2 = st.columns(2)
    with c1:
        d = elevage_f.groupby("region_nom_bdd").size().reset_index(name="n").sort_values("n")
        fig = px.bar(d, x="n", y="region_nom_bdd", orientation="h",
                     title="Établissements d'élevage par région",
                     color_discrete_sequence=[C_EMERALD], text="n")
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="", xaxis_title="Établissements")
        plot(fig)
    with c2:
        infra = pd.DataFrame({
            "Infrastructure": ["Élevage", "Retenues d'eau", "Digues & barrages", "Pisciculture", "Abattoirs"],
            "Nombre": [len(elevage_f), len(retenues_f), len(digues_f), len(pisci_f), len(abattoirs_f)],
        })
        fig = px.treemap(infra, path=["Infrastructure"], values="Nombre",
                         title="Poids relatif des infrastructures recensées",
                         color="Infrastructure", color_discrete_sequence=PALETTE)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        plot(fig)

# ================= TAB 2 : INDICE DE RESILIENCE =================
with tabs[1]:
    st.markdown("""
    <div class="section-note">
    <b>Méthodologie de l'IRAT</b> - indice composite de 0 (fragile) à 1 (résilient), calculé par canton :
    <b>35 %</b> accès à l'eau (retenues + digues) &nbsp;|&nbsp; <b>25 %</b> proximité d'un abattoir &nbsp;|&nbsp;
    <b>20 %</b> diversification (pisciculture) &nbsp;|&nbsp; <b>20 %</b> encadrement (infrastructures d'eau par élevage).
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([5, 4])
    with c1:
        d = canton_f.dropna(subset=["lat", "lon"])
        fig = px.scatter_map(
            d, lat="lat", lon="lon", color="IRAT", size="n_elevage",
            hover_name="canton_nom_bdd",
            hover_data={"prefecture_nom_bdd": True, "IRAT": ":.2f", "n_elevage": True,
                        "lat": False, "lon": False},
            color_continuous_scale=["#C0392B", "#F2C500", "#1E8A3C"],
            size_max=22, zoom=6.2, height=560,
            title="Carte de l'IRAT par canton (taille = activité d'élevage)",
        )
        fig.update_layout(map_style="carto-positron", paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=0, r=0, t=40, b=0))
        plot(fig)
    with c2:
        st.markdown("<div style='height:55px'></div>", unsafe_allow_html=True)
        d = canton_f["statut"].value_counts().reset_index()
        d.columns = ["Statut", "Cantons"]
        fig = px.pie(d, names="Statut", values="Cantons", hole=0.55,
                     title="Répartition des cantons par statut de résilience",
                     color="Statut",
                     color_discrete_map={"Vulnérable": C_RED, "Intermédiaire": C_GOLD, "Résilient": C_EMERALD})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=450,
                          legend=dict(orientation="h", yanchor="bottom", y=-0.15, x=0.5, xanchor="center"))
        plot(fig)

    pref = canton_f.groupby("prefecture_nom_bdd")["IRAT"].mean().reset_index().sort_values("IRAT", ascending=False)
    fig = px.bar(pref.head(20), x="prefecture_nom_bdd", y="IRAT",
                 title="Préfectures les plus résilientes (IRAT moyen)",
                 color="IRAT", color_continuous_scale=["#F2C500", "#1E8A3C"], text_auto=".2f")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                      xaxis_title="", yaxis_title="IRAT moyen",
                      coloraxis_showscale=False, height=420)
    fig.update_traces(textposition="outside")
    plot(fig)

    st.markdown("#### Cantons les plus vulnérables")
    vuln = canton_f.nsmallest(15, "IRAT")[
        ["region_nom_bdd", "prefecture_nom_bdd", "canton_nom_bdd",
         "n_elevage", "n_retenues", "n_digues", "dist_abattoir_km", "IRAT"]
    ].rename(columns={
        "region_nom_bdd": "Région", "prefecture_nom_bdd": "Préfecture",
        "canton_nom_bdd": "Canton", "n_elevage": "Élevages",
        "n_retenues": "Retenues", "n_digues": "Digues",
        "dist_abattoir_km": "Dist. abattoir (km)",
    })
    vuln["Dist. abattoir (km)"] = vuln["Dist. abattoir (km)"].round(1)

    def color_irat(v):
        if pd.isna(v):
            return "background-color:#FDECEA;color:#C0392B"
        if v < 0.10:
            return "background-color:#FDECEA;color:#C0392B;font-weight:bold"
        if v < 0.25:
            return "background-color:#FCF3CF;color:#7D6608"
        return "background-color:#E8F6EC;color:#0B5D26"

    def color_dist(v):
        if pd.isna(v):
            return "background-color:#FDECEA;color:#C0392B"
        if v > 40:
            return "background-color:#FDECEA;color:#C0392B;font-weight:bold"
        if v > 20:
            return "background-color:#FCF3CF;color:#7D6608"
        return "background-color:#E8F6EC;color:#0B5D26"

    styled = (vuln.reset_index(drop=True).style
              .map(color_irat, subset=["IRAT"])
              .map(color_dist, subset=["Dist. abattoir (km)"])
              .format({"IRAT": "{:.3f}", "Dist. abattoir (km)": "{:.1f}",
                       "Élevages": "{:.0f}", "Retenues": "{:.0f}", "Digues": "{:.0f}"},
                      na_rep="Aucun point")
              .set_table_styles([
                  {"selector": "", "props": [("width", "100%"), ("border-collapse", "collapse"),
                                             ("background", "#FFFFFF"), ("border-radius", "12px")]},
                  {"selector": "th",
                   "props": [("background-color", "#0B5D26"), ("color", "#F2C500"),
                             ("font-weight", "700"), ("text-align", "left"),
                             ("padding", "9px 14px")]},
                  {"selector": "td",
                   "props": [("padding", "8px 14px"), ("border-bottom", "1px solid #E5E7EB"),
                             ("color", "#1C1C1C")]},
              ])
              .hide(axis="index"))
    st.markdown(styled.to_html(), unsafe_allow_html=True)

# ================= TAB 3 : ACCES A L'EAU =================
with tabs[2]:
    st.markdown('<div class="section-note">L\'eau est la première condition de la résilience agricole : '
                'irrigation, abreuvement du bétail et pisciculture en dépendent directement.</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        eau = pd.concat([
            retenues_f.assign(type_infra="Retenues d'eau"),
            digues_f.assign(type_infra="Digues & barrages"),
        ])
        d = eau.groupby(["region_nom_bdd", "type_infra"]).size().reset_index(name="n")
        fig = px.bar(d, x="region_nom_bdd", y="n", color="type_infra", barmode="group",
                     title="Infrastructures d'eau par région",
                     color_discrete_sequence=[C_BLUE, "#8E7CC3"])
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          xaxis_title="", yaxis_title="Nombre",
                          legend=dict(orientation="h", y=1.12, title=""))
        plot(fig)
    with c2:
        d = canton_f.copy()
        d["eau_totale"] = d["n_retenues"] + d["n_digues"]
        fig = px.scatter(d, x="n_elevage", y="eau_totale", color="statut", size="n_elevage",
                         hover_name="canton_nom_bdd",
                         title="Activité d'élevage vs infrastructures d'eau (par canton)",
                         color_discrete_map={"Vulnérable": C_RED, "Intermédiaire": C_GOLD, "Résilient": C_EMERALD},
                         labels={"n_elevage": "Établissements d'élevage", "eau_totale": "Infrastructures d'eau"})
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          legend=dict(orientation="h", y=1.12, title=""))
        plot(fig)

    if "barrage_utilisation" in retenues_f.columns:
        usages = (retenues_f["barrage_utilisation"].dropna().astype(str)
                  .str.strip("{}").str.split(",").explode().str.strip())
        usages = usages[usages != ""].value_counts().head(10).reset_index()
        usages.columns = ["Usage", "Nombre"]
        fig = px.bar(usages, x="Nombre", y="Usage", orientation="h",
                     title="Usages déclarés des retenues d'eau",
                     color_discrete_sequence=[C_BLUE], text="Nombre")
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", yaxis_title="")
        plot(fig)

# ================= TAB 4 : ELEVAGE & ABATTOIRS =================
with tabs[3]:
    st.markdown('<div class="section-note">Un élevage sans accès à un abattoir formel perd de la valeur : '
                'pertes sanitaires, circuits informels, prix plus faibles. La distance au premier abattoir est un '
                'indicateur direct de performance économique.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(canton_f.dropna(subset=["dist_abattoir_km"]), x="dist_abattoir_km", nbins=30,
                           title="Distance à l'abattoir le plus proche (par canton)",
                           color_discrete_sequence=[C_EMERALD],
                           labels={"dist_abattoir_km": "Distance (km)"})
        med = canton_f["dist_abattoir_km"].median()
        fig.add_vline(x=med, line_dash="dash", line_color=C_RED,
                      annotation_text=f"Médiane : {med:.0f} km")
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", yaxis_title="Cantons")
        plot(fig)
    with c2:
        d = canton_f.groupby("region_nom_bdd").agg(
            dist_moy=("dist_abattoir_km", "mean"), elevages=("n_elevage", "sum")).reset_index()
        fig = px.bar(d.sort_values("dist_moy"), x="dist_moy", y="region_nom_bdd", orientation="h",
                     title="Distance moyenne à un abattoir, par région",
                     color="dist_moy", color_continuous_scale=["#1E8A3C", "#F2C500", "#C0392B"],
                     labels={"dist_moy": "Distance moyenne (km)"})
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="", coloraxis_showscale=False)
        plot(fig)

    if "activite_categorie" in elevage_f.columns:
        cats = (elevage_f["activite_categorie"].dropna().astype(str)
                .str.strip("{}").str.split(",").explode().str.strip())
        cats = cats[cats != ""].value_counts().head(8).reset_index()
        cats.columns = ["Catégorie", "Nombre"]
        fig = px.bar(cats, x="Nombre", y="Catégorie", orientation="h",
                     title="Catégories d'élevage recensées",
                     color_discrete_sequence=[C_GOLD], text="Nombre")
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", yaxis_title="")
        plot(fig)

# ================= TAB 5 : ECONOMIE AGRICOLE =================
with tabs[4]:
    st.markdown('<div class="section-note">Séries de la Banque mondiale : la valeur ajoutée agricole replace les '
                'infrastructures locales dans la trajectoire macroéconomique du pays.</div>',
                unsafe_allow_html=True)

    wb_recent = wb[wb["annee"] >= 1990]
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=wb_recent["annee"], y=wb_recent["va_pct_pib"],
                                 fill="tozeroy", line=dict(color=C_EMERALD, width=3),
                                 fillcolor="rgba(30,138,60,.15)", name="% du PIB"))
        fig.update_layout(title="Valeur ajoutée agricole (% du PIB)",
                          plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="% du PIB", xaxis_title="")
        plot(fig)
    with c2:
        d = wb_recent.dropna(subset=["va_croissance"])
        fig = px.bar(d, x="annee", y="va_croissance",
                     title="Croissance annuelle de la valeur ajoutée agricole (%)",
                     color=d["va_croissance"] > 0,
                     color_discrete_map={True: C_EMERALD, False: C_RED})
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          showlegend=False, yaxis_title="%", xaxis_title="")
        plot(fig)

    c3, c4 = st.columns(2)
    with c3:
        d = wb_recent.dropna(subset=["va_usd_2015"])
        fig = px.line(d, x="annee", y="va_usd_2015",
                      title="Valeur ajoutée agricole (USD constants 2015)")
        fig.update_traces(line=dict(color=C_GOLD, width=3))
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="USD constants 2015", xaxis_title="")
        plot(fig)
    with c4:
        d = wb_recent.dropna(subset=["va_par_travailleur"])
        fig = px.line(d, x="annee", y="va_par_travailleur",
                      title="Valeur ajoutée agricole par travailleur (USD 2015)")
        fig.update_traces(line=dict(color=C_BLUE, width=3))
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="USD par travailleur", xaxis_title="")
        plot(fig)

    st.markdown("#### Agriculture & développement rural")
    rural_recent = rural[rural["annee"] >= 1990]
    c5, c6 = st.columns(2)
    with c5:
        d = rural_recent.dropna(subset=["rendement_cereales_kg_ha"])
        fig = px.line(d, x="annee", y="rendement_cereales_kg_ha",
                      title="Rendement des céréales (kg par hectare)")
        fig.update_traces(line=dict(color=C_EMERALD, width=3))
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="kg / ha", xaxis_title="")
        plot(fig)
    with c6:
        d = rural_recent.dropna(subset=["indice_production_vegetale", "indice_production_animale"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d["annee"], y=d["indice_production_vegetale"],
                                 name="Production végétale", line=dict(color=C_EMERALD, width=3)))
        fig.add_trace(go.Scatter(x=d["annee"], y=d["indice_production_animale"],
                                 name="Production animale", line=dict(color=C_GOLD, width=3)))
        fig.update_layout(title="Indices de production agricole (base 100 = 2014-2016)",
                          plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="Indice", xaxis_title="",
                          legend=dict(orientation="h", y=1.12, title=""))
        plot(fig)

    c7, c8 = st.columns(2)
    with c7:
        d = rural_recent.dropna(subset=["terres_agricoles_pct", "terres_arables_pct"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d["annee"], y=d["terres_agricoles_pct"],
                                 name="Terres agricoles", fill="tozeroy",
                                 line=dict(color=C_EMERALD, width=2),
                                 fillcolor="rgba(30,138,60,.15)"))
        fig.add_trace(go.Scatter(x=d["annee"], y=d["terres_arables_pct"],
                                 name="Terres arables", fill="tozeroy",
                                 line=dict(color=C_BLUE, width=2),
                                 fillcolor="rgba(46,134,193,.15)"))
        fig.update_layout(title="Terres agricoles et arables (% du territoire)",
                          plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="% du territoire", xaxis_title="",
                          legend=dict(orientation="h", y=1.12, title=""))
        plot(fig)
    with c8:
        d = rural_recent.dropna(subset=["population_rurale_pct"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d["annee"], y=d["population_rurale_pct"],
                                 name="Population rurale", line=dict(color=C_EMERALD, width=3)))
        d2 = rural_recent.dropna(subset=["emploi_agricole_pct"])
        fig.add_trace(go.Scatter(x=d2["annee"], y=d2["emploi_agricole_pct"],
                                 name="Emploi agricole", line=dict(color=C_RED, width=3, dash="dot")))
        fig.update_layout(title="Population rurale et emploi agricole (% du total)",
                          plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title="%", xaxis_title="",
                          legend=dict(orientation="h", y=1.12, title=""))
        plot(fig)

# ================= TAB 6 : ZONES PRIORITAIRES =================
with tabs[5]:
    st.markdown("""
    <div class="section-note">
    <b>Score de priorité d'investissement</b> = intensité de l'activité d'élevage x déficit de résilience (1 - IRAT).
    Il cible les cantons où l'activité économique existe déjà mais reste fragilisée par le manque d'infrastructures :
    c'est là que chaque franc investi a le plus d'effet de levier.
    </div>""", unsafe_allow_html=True)

    top10 = canton_f.nlargest(10, "score_priorite").copy()
    top10["Rang"] = range(1, len(top10) + 1)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<h4 style='text-align:center'>🏆 Top 10 des cantons<br><span style='margin-left:40px'>prioritaires</span></h4>", unsafe_allow_html=True)
        t = top10[["Rang", "canton_nom_bdd", "prefecture_nom_bdd", "region_nom_bdd",
                   "n_elevage", "IRAT", "score_priorite"]].rename(columns={
            "canton_nom_bdd": "Canton", "prefecture_nom_bdd": "Préfecture",
            "region_nom_bdd": "Région", "n_elevage": "Élevages",
            "score_priorite": "Priorité"})
        st.dataframe(t, use_container_width=True, hide_index=True, height=397)
    with c2:
        st.markdown("<h4 style='text-align:center'>📍 Localisation des 10 zones<br><span style='margin-left:26px'>prioritaires</span></h4>", unsafe_allow_html=True)
        d = top10.dropna(subset=["lat", "lon"])
        fig = px.scatter_map(
            d, lat="lat", lon="lon", size="score_priorite", color="score_priorite",
            hover_name="canton_nom_bdd",
            hover_data={"prefecture_nom_bdd": True, "n_elevage": True,
                        "IRAT": ":.2f", "lat": False, "lon": False, "score_priorite": ":.2f"},
            color_continuous_scale=["#F2C500", "#C0392B"], size_max=28,
            height=420,
            labels={"score_priorite": "Priorité"},
        )
        fig.update_layout(map_style="carto-positron", paper_bgcolor="rgba(0,0,0,0)",
                          map_center=dict(lat=d["lat"].mean(), lon=d["lon"].mean()),
                          map_zoom=6.8,
                          coloraxis_colorbar=dict(title="Priorité"),
                          margin=dict(l=0, r=0, t=10, b=0))
        plot(fig)

    st.markdown("#### Recommandations d'investissement")
    r1, r2, r3 = st.columns(3)
    r1.markdown(f"""<div class="reco"><div class="l">💧 Eau d'abord</div>
    <div class="s">Dans les cantons prioritaires, le déficit le plus fréquent est l'infrastructure d'eau.
    Prioriser retenues collinaires et petits barrages à usage mixte (abreuvement + maraîchage),
    qui renforcent à la fois l'élevage et la diversification.</div></div>""", unsafe_allow_html=True)
    r2.markdown(f"""<div class="reco"><div class="l">🥩 Abattoirs de proximité</div>
    <div class="s">Avec seulement {len(abattoirs)} abattoirs recensés pour {len(elevage):,} établissements d'élevage,
    des aires d'abattage modernes dans les préfectures éloignées réduiraient pertes sanitaires
    et circuits informels.</div></div>""".replace(",", " "), unsafe_allow_html=True)
    r3.markdown("""<div class="reco"><div class="l">🐟 Diversification piscicole</div>
    <div class="s">La pisciculture reste concentrée sur peu de zones. L'adosser aux retenues d'eau existantes
    dans les cantons intermédiaires offre un second revenu et amortit les chocs climatiques.</div></div>""",
    unsafe_allow_html=True)

st.markdown("<br><hr style='border-color:#D9DCE0'>", unsafe_allow_html=True)
st.markdown(
    f"<div style='text-align:center;color:#555555;font-size:.85rem'>"
    f"Résilience Agri-Togo - Data Challenge Agriculture Défi 2 | Togo AI Lab - "
    f"Données : geodata.gouv.tg, opendata.gouv.tg, Banque mondiale - OURO-TAGBA Bastou</div>",
    unsafe_allow_html=True)
