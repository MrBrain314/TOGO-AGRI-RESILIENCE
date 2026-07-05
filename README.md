# 🌾 Résilience Agri-Togo - Dashboard analytique

Identifier les zones du Togo où les infrastructures agricoles (élevage, eau, pisciculture, abattoirs) soutiennent réellement l'économie locale, et celles où de nouveaux investissements seraient les plus pertinents.

**Data Challenge Agriculture - Défi 2** organisé par Togo AI Lab (deadline : 06 juillet 2026).

🔗 **Dashboard en ligne :** [togo-agri-resilience.streamlit.app](https://togo-agri-resilience.streamlit.app/)

---

## 🧭 L'Indice de Résilience Agricole Territoriale (IRAT)

Indice composite calculé par canton, de 0 (fragile) à 1 (résilient) :

| Composante | Poids | Mesure |
|---|---|---|
|  Accès à l'eau | 35 % | Retenues collinaires + digues et petits barrages |
|  Proximité abattoir | 25 % | Distance du canton à l'abattoir le plus proche (haversine) |
|  Diversification | 20 % | Présence de zones de pisciculture |
|  Encadrement | 20 % | Infrastructures d'eau rapportées au nombre d'élevages |

**Score de priorité d'investissement** = intensité d'activité d'élevage x déficit de résilience (1 - IRAT). Il cible les cantons où l'activité économique existe mais reste fragilisée par le manque d'infrastructures.

### 📊 Résultats clés

- **363 cantons analysés** : 209 vulnérables, 136 intermédiaires, 18 résilients
- Distance médiane à un abattoir : **15,2 km**
- Seulement **36 abattoirs** pour plus de 3 000 établissements d'élevage

## 📁 Structure du projet

```
AGRI_DASHBOARD/
+-- app.py                       # Application Streamlit
+-- requirements.txt             # Dépendances Python
+-- data/                                  # 10 fichiers = les 10 sources du cahier des charges
|   +-- elevage_etablissements.csv         (3 004 enregistrements)
|   +-- abattoirs.csv                      (36 enregistrements)
|   +-- zones_pisciculture.csv             (141 enregistrements)
|   +-- retenues_eau.csv                   (611 enregistrements)
|   +-- digues_barrages.csv                (300 enregistrements)
|   +-- agriculture_dev_rural.csv          (7 indicateurs, 1960-2025)
|   +-- va_agricole_pct_pib.csv            (% du PIB, 1963-2025)
|   +-- va_agricole_croissance.csv         (croissance annuelle, 1966-2025)
|   +-- va_agricole_usd_2015.csv           (USD constants 2015, 1965-2025)
|   +-- va_agricole_par_travailleur.csv    (par travailleur, 1991-2025)
+-- images/
|   +-- LOGO.jpg
+-- Rapport d'Analyse/
|   +-- Presentation_Defi2.pptx        # Présentation des analyses et résultats
+-- README.md
```

## 🗂️ Les 6 onglets du dashboard

1. 🗺️ **Vue d'ensemble** - carte générale des infrastructures avec clusters, poids relatifs
2. 🧭 **Indice de résilience** - carte IRAT par canton, statuts, cantons vulnérables
3. 💧 **Accès à l'eau** - infrastructures par région, croisement activité/eau, usages des retenues
4. 🥩 **Élevage & abattoirs** - distances aux abattoirs, catégories d'élevage
5. 📈 **Économie agricole** - séries Banque mondiale : valeur ajoutée agricole, rendements céréaliers, indices de production, terres agricoles, population rurale et emploi agricole (1990-2025)
6. 🎯 **Zones prioritaires** - Top 10 des cantons pour investissements + recommandations

## 📚 Sources de données

- [geodata.gouv.tg](https://geodata.gouv.tg/) / [opendata.gouv.tg](https://opendata.gouv.tg/) : élevage, abattoirs, pisciculture, retenues d'eau, digues et barrages
- [Banque mondiale](https://donnees.banquemondiale.org/) : valeur ajoutée agricole (% PIB, croissance, USD constants 2015, par travailleur)

Les géométries WKT (POINT, POLYGON, MULTIPOLYGON, MULTILINESTRING) sont parsées par expressions régulières Python, sans GeoPandas.

## ⚙️ Installation et lancement

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ✍️ Auteur

**OURO-TAGBA Bastou**
Data Challenge Agriculture - Défi 2 - Togo AI Lab, juillet 2026