from flask import Blueprint, render_template, request, flash, jsonify
import json
import requests
from .data_model import create_stats_table, get_db_connection

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
