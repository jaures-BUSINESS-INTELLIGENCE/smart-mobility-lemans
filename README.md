# Smart Mobility Le Mans 
<!-- Mobilité intelligente au Mans  -->

A live dashboard about the SETRAM public transport network (Le Mans
Métropole): real-time delays, service alerts, and a comparison between the
scheduled transport supply and the population of each commune.
<!-- Un tableau de bord sur le réseau de transport SETRAM (Le Mans Métropole) :
retards en temps réel, alertes de service, et une comparaison entre l'offre de
transport prévue et la population de chaque commune. -->

**Live page:** https://jaures-business-intelligence.github.io/smart-mobility-lemans/
<!-- Page en ligne -->

## The question
<!-- La question -->

If Le Mans Métropole had limited resources to improve its public transport
network, where and when should it prioritize interventions?
<!-- Si Le Mans Métropole avait des ressources limitées pour améliorer son réseau
de transport public, où et quand devrait-elle intervenir en priorité ? -->

## How it works: two automated pipelines
<!-- Comment ça marche : deux pipelines automatiques -->

**1. Static reference (monthly, `build_static_reference.yml`)**
<!-- 1. Référence statique (mensuelle) -->

- Downloads SETRAM's official GTFS timetable.
  <!-- Télécharge l'horaire GTFS officiel de SETRAM. -->
- Picks a representative Tuesday and counts the scheduled trips at each stop.
  <!-- Choisit un mardi type et compte les passages prévus à chaque arrêt. -->
- Assigns each stop to the nearest commune and saves `data/gtfs_static/`.
  <!-- Rattache chaque arrêt à la commune la plus proche et enregistre
  data/gtfs_static/. -->
- `scripts/supply_vs_population.py` then computes the scheduled stop-visits per
  1,000 residents for each commune (`docs/data/supply.json`).
  <!-- Le script supply_vs_population.py calcule ensuite les passages prévus pour
  1 000 habitants dans chaque commune (docs/data/supply.json). -->

**2. Real-time snapshot (every 15 minutes, `collect_snapshot.yml`)**
<!-- 2. Instantané temps réel (toutes les 15 minutes) -->

- Reads the GTFS-RT feeds: delays of the vehicles and active service alerts.
  <!-- Lit les flux GTFS-RT : retards des véhicules et alertes de service. -->
- Summarizes one row per route and appends it to `data/history/` (it never
  overwrites the history).
  <!-- Résume une ligne par ligne de bus et l'ajoute à data/history/ (l'historique
  n'est jamais écrasé). -->
- Rewrites `docs/data/current_state.json`, which the web page reads.
  <!-- Réécrit docs/data/current_state.json, que la page web lit. -->

## Repository structure
<!-- Structure du dépôt -->

- `data/reference/communes.csv`: the 20 communes (coordinates and population)
- `data/gtfs_static/`: generated schedule data (trips per stop, routes)
- `data/history/`: growing log of delays and alerts
- `scripts/`: the three Python scripts
- `docs/`: the web page and the generated JSON files
- `.github/workflows/`: the two automations
- `REFLECTIONS.md`: my written answers to the TD questions

## Main findings and limits
<!-- Principaux résultats et limites -->

- **Population is only a proxy for demand.** No transit agency publishes real
  ridership data, so the "supply vs. demand" comparison is approximate.
  <!-- La population n'est qu'un substitut de la demande. Aucune agence ne publie
  le vrai nombre de voyageurs : la comparaison offre/demande est approximative. -->
- **The supply ranking is misleading for some communes.** Each stop is assigned
  to the commune with the nearest center, not to the commune where it really
  is. Stops from the north of Le Mans (for example in an industrial zone or near
  the university) are counted in small neighbouring communes such as
  La-Chapelle-Saint-Aubin, which looks very well served (about 1,010 visits per
  1,000 residents) while Le Mans itself (about 154) looks poorly served.
  <!-- Le classement de l'offre est trompeur pour certaines communes. Chaque arrêt
  est rattaché à la commune dont le centre est le plus proche, pas à la commune
  où il se trouve vraiment. Des arrêts du nord du Mans (par exemple dans une zone
  industrielle ou près de l'université) sont comptés dans de petites communes
  voisines comme La-Chapelle-Saint-Aubin, qui paraît très bien desservie
  (environ 1 010 passages pour 1 000 habitants) alors que Le Mans (environ 154)
  paraît mal desservie. -->
- **Real-time delays are noisy.** A route with only one observed bus gives an
  unreliable average, and some data can be frozen in the feed.
  <!-- Les retards en temps réel sont bruités. Une ligne avec un seul bus observé
  donne une moyenne peu fiable, et certaines données peuvent être figées dans le
  flux. -->
- **Early buses are colored green.** A bus that is very early can strand a
  passenger just like a late bus; the color scale does not show this.
  <!-- Les bus en avance sont colorés en vert. Un bus très en avance peut laisser
  un voyageur à quai comme un bus en retard ; l'échelle de couleurs ne le montre
  pas. -->
- **Repeated delays need history.** The real-time data has no archive, so
  patterns and predictions need weeks of collected snapshots.
  <!-- Les retards répétés demandent de l'historique. Les données temps réel n'ont
  pas d'archive : repérer des motifs et faire des prévisions demande des semaines
  d'instantanés. -->

## Data sources
<!-- Sources des données -->

- Static GTFS timetable: SETRAM, via data.gouv.fr
- Real-time feeds (TripUpdate and Alert): SETRAM, via transport.data.gouv.fr
- Population of the communes: INSEE (to be re-checked before professional use)
