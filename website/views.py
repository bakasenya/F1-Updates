from flask import Blueprint, render_template, request, flash, jsonify
import json
import requests
from .data_model import create_stats_table, get_db_connection, create_drivers_table

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@views.route("/seasons", methods=["GET"])
def seasons_page():
    response = requests.get("http://ergast.com/api/f1/seasons.json?limit=1000")
    data = response.json()
    seasons = data["MRData"]["SeasonTable"]["Seasons"]
    
    seasons_list = []
    
    create_stats_table()
    
    con, cur = get_db_connection()
    for id, season in enumerate(seasons):
        year = season["season"]
        url = season["url"]
        seasons_list.append((id, year, url))
        
        cur.execute("""
                    INSERT OR IGNORE INTO stats (ID, year, url)
                    VALUES (?, ?, ?)
        """, (id, year, url))
        
    con.commit()
    con.close()
        
        
    con, cur = get_db_connection()
    db_seasons = con.execute("SELECT * FROM stats").fetchall()
    con.close()    
    
    return render_template("seasons.html", seasons=db_seasons)


@views.route("/drivers", methods=["GET"])
def drivers_page():
    all_drivers = []
    offset = 0
    gap = 100
    
    create_drivers_table()
    
    
    for _ in range(9):
        response = requests.get(f"https://ergast.com/api/f1/drivers.json?limit=100&offset={offset}")

        if response.status_code == 200:
            data = response.json()
            drivers = data["MRData"]["DriverTable"]["Drivers"]
        else:
            print("Error fetching data")
            break
        
        for driver in drivers:
            all_drivers.append(driver)
            con, cur = get_db_connection()
            cur.execute("""
                        INSERT OR IGNORE INTO drivers (driverId, givenName, familyName, dateOfBirth, nationality, url)
                        VALUES (?, ?, ?, ?, ?, ?)
            """, (driver["driverId"], driver["givenName"], driver["familyName"], driver["dateOfBirth"], driver["nationality"], driver["url"]))
            con.commit()
            con.close()
        
        offset += gap
        
    
    
    return render_template("drivers.html", drivers=all_drivers)
    
