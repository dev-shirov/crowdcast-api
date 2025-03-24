import csv
import sqlite3

con = sqlite3.connect("./src/data/predictions.db")
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS 
        predictions 
            (id integer, 
            location varchar, 
            month integer, 
            days_rained integer, 
            days_cloudy integer, 
            days_sunny integer, 
            tourists integer,
            crowded varchar,
            water_sports_score integer,
            hiking_score integer,
            staycation_score integer,
            nightlife_score integer
            )
    """
)

with open("./src/data/llm_dataset.csv", "r") as f:
    reader = csv.DictReader(f)
    to_db = [
        (
            i["id"],
            i["location"],
            i["month"],
            i["days_rained"],
            i["days_cloudy"],
            i["days_sunny"],
            i["tourists"],
            i["crowded"],
            i["water_sports_score"],
            i["hiking_score"],
            i["staycation_score"],
            i["nightlife_score"],
        )
        for i in reader
    ]

insert_query = """
                INSERT OR IGNORE INTO predictions 
                    (id, 
                    location, 
                    month, 
                    days_rained, 
                    days_cloudy, 
                    days_sunny, 
                    tourists,
                    crowded,
                    water_sports_score,
                    hiking_score,
                    staycation_score,
                    nightlife_score
                    ) 
                VALUES (?, ?, ?, ? ,? ,?, ?, ?, ?, ?, ? , ?);
                """
cur.executemany(
    insert_query,
    to_db,
)
con.commit()
con.close()
