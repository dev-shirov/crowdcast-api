import csv
import sqlite3

con = sqlite3.connect("./src/data/predictions.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS boracay_predictions (id integer , month integer, year integer, days_rained integer, days_cloudy integer, days_sunny integer, tourists integer)"
)

with open("./src/data/boracay_forecast.csv", "r") as f:
    reader = csv.DictReader(f)
    to_db = [
        (
            i["id"],
            i["month"],
            i["year"],
            i["days_rained"],
            i["days_cloudy"],
            i["days_sunny"],
            i["tourists"],
        )
        for i in reader
    ]

cur.executemany(
    "INSERT OR IGNORE INTO boracay_predictions (id, month, year, days_rained, days_cloudy, days_sunny, tourists) VALUES (?, ?, ?, ? ,? ,?, ?);",
    to_db,
)
con.commit()
con.close()
