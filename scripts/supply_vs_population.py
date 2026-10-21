import json, time
import pandas as pd

def main():
    # 1) Lire l'offre par arrêt  et la population par commune (étape 2)
    stops = pd.read_csv("data/gtfs_static/stops_frequency.csv")
    communes = pd.read_csv("data/reference/communes.csv")

    # 2) Regrouper les arrêts par commune : nombre d'arrêts, total des passages,
    #    et passages de l'arrêt le plus fréquenté
    supply = (
        stops.groupby("nearest_commune")
        .agg(n_stops=("stop_id", "count"),
             stop_visits=("daily_trip_count", "sum"),
             busiest_stop=("daily_trip_count", "max"))
        .reset_index()
        .rename(columns={"nearest_commune": "commune"})
    )

    # 3) Joindre avec la population ; une commune sans arrêt aura 0
    df = communes.merge(supply, on="commune", how="left").fillna(0)

    # 4) Passages par jour pour 1 000 habitants
    df["visits_per_1000"] = (df["stop_visits"] / df["population"] * 1000).round(1)

    # Part de l'offre qui vient d'un seul arrêt (proche de 1 = suspect : dépôt ou
    # point d'échange)
    df["busiest_stop_share"] = (
        df["busiest_stop"] / df["stop_visits"].where(df["stop_visits"] > 0)
    ).fillna(0).round(3)

    # 5) Trier de la mieux desservie à la moins bien desservie
    df = df.sort_values("visits_per_1000", ascending=False)

    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "metric_label": "Scheduled stop-visits per weekday per 1,000 residents "
                        "(population = proxy for demand, not measured ridership)",
        "rows": [
            {
                "commune": r.commune,
                "population": int(r.population),
                "n_stops": int(r.n_stops),
                "stop_visits_weekday": int(r.stop_visits),
                "visits_per_1000_residents": float(r.visits_per_1000),
                "busiest_stop_share": float(r.busiest_stop_share),
            }
            for r in df.itertuples()
        ],
    }
    with open("docs/data/supply.json", "w") as f:
        json.dump(out, f, indent=2)

    print(df[["commune", "population", "n_stops", "stop_visits",
              "visits_per_1000", "busiest_stop_share"]].to_string(index=False))
    print("Wrote docs/data/supply.json")

if __name__ == "__main__":
    main()
