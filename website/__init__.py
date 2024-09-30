from flask_restful import Api, Resource
from flask import Flask, jsonify, render_template, Blueprint
from requests import get, exceptions
from pprint import PrettyPrinter
from os import path
import sqlite3
from .data_model import get_db_connection, create_stats_table

BASE_URL = "http://ergast.com/api/f1/"
printer = PrettyPrinter()

DB_PATH = "stats_database.db"



def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "oop"
    
    create_stats_table()
    
    from .views import views
    
    app.register_blueprint(views, url_prefix="/")
    
    
        
    # def load_stat(id):
    #     return Stats.query.get(int(id))
    
    return app



