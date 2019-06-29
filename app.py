import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from datetime import datetime
import re
import string

db_server = 'project-3-db.cnsppazvk5qa.us-east-2.rds.amazonaws.com'
db_port = 5432
db_pass = 'fred007!'
db_user = 'root'
db_name = 'projectDB'

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://{}:{}@{}/{}'.format(db_user,db_pass,db_server,db_name)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

Base = automap_base()

Base.prepare(db.engine, reflect=True)

Product = Base.classes.product
Reviews = Base.classes.reviews
Author = Base.classes.author

@app.route('/')
def index():
    out_dict = {}
    out_dict['category'] = []
    results = db.session.query(Product.product_cat).distinct(Product.product_cat).all()
    for i in results:
       out_dict['category'].append(i[0])
    return jsonify(out_dict)

@app.route('/products/<cat>')
def get_products(cat):
    out_dict = {}
    results = db.session.query(Product.product_id,Product.product_cat,Product.name,Product.link,Product.link_image,Product.amazon_price).filter(Product.product_cat == cat).all()
    for i in results:
        tmp_dict = {}
        tmp_dict['product_id'] = i[0]
        tmp_dict['product_cat'] = i[1]
        tmp_dict['name'] = i[2]
        tmp_dict['link'] = i[3]
        tmp_dict['link_image'] = i[4]
        tmp_dict['amazon_price'] = i[5]
        out_dict[i[0]] = tmp_dict
    return jsonify(out_dict)

if __name__ == "__main__":
    app.run()
