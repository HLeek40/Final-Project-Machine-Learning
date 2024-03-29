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
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
    return render_template("index.html")

@app.route('/storeRev/<pid>/<text1>')
def sReview(pid,text1):
    ret = db.session.query(Author.author_id).filter(Author.author_id == 'testUser').first()
    if not ret:
        auth = Author(author_id = 'testUser')
        db.session.add(auth)
    vader = SentimentIntensityAnalyzer().polarity_scores(text1)
    tDay = datetime.now()
    data = Reviews(product_id = pid, text = text1, vNegative = vader['neg'], vPositive = vader['pos'], vNeutral = vader['neu'], vCompound = vader['compound'], input_time = tDay)
    db.session.add(data)
    db.session.commit()
    return 'done'

@app.route('/cat_list')
def get_cat():
    out_dict = []
    results = db.session.query(Product.product_cat).distinct(Product.product_cat).all()
    for i in results:
       out_dict.append(i[0])
    return(jsonify(out_dict))

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

@app.route('/reviews/<product_id>')
def get_reviews(product_id):
    out_dict = {}
    results = db.session.query(Reviews.text,Reviews.tPolarity,Reviews.tSubjectivity,Reviews.vNegative,Reviews.vPositive,Reviews.vNeutral,Reviews.vCompound,Reviews.input_time).filter(Reviews.product_id == product_id).order_by(Reviews.input_time).all()
    for i in results:
        tmp_dict = {}
        tmp_dict['product_id'] = product_id
        tmp_dict['text'] = i[0]
        tmp_dict['tPolarity'] = i[1]
        tmp_dict['tSubjectivity'] = i[2]
        tmp_dict['vNegative'] = i[3]
        tmp_dict['vPositive'] = i[4]
        tmp_dict['vNeutral'] = i[5]
        tmp_dict['vCompound'] = i[6]
        tmp_dict['input_time'] = i[7]
        out_dict[i[0]] = tmp_dict
    return jsonify(out_dict)

@app.route('/cat_reviews/<product_cat>')
def get_cat_reviews(product_cat):
    out_dict = {}
    results = db.session.query(Product.product_id).filter(Product.product_cat == product_cat).all()
    for i in results:
        results1 = db.session.query(Reviews.id,Reviews.tPolarity,Reviews.tSubjectivity,Reviews.vNegative,Reviews.vPositive,Reviews.vNeutral,Reviews.vCompound).filter(Reviews.product_id == i[0]).all()
        for j in results1:
            tmp_dict = {}
            tmp_dict['tPolarity'] = j[1]
            tmp_dict['tSubjectivity'] = j[2]
            tmp_dict['vNegative'] = j[3]
            tmp_dict['vPositive'] = j[4]
            tmp_dict['vNeutral'] = j[5]
            tmp_dict['vCompound'] = j[6]
            out_dict[j[0]] = tmp_dict
    scores = {}
    for rev in out_dict.keys():
        if 'pos' in scores:
            scores['pos'] = scores['pos'] + out_dict[rev]['vPositive']
        else:
            scores['pos'] = out_dict[rev]['vPositive']
        if 'neg' in scores:
            scores['neg'] = scores['neg'] + out_dict[rev]['vNegative']
        else:
            scores['neg'] = out_dict[rev]['vNegative']
        if 'neu' in scores:
            scores['neu'] = scores['neu'] + out_dict[rev]['vNeutral']
        else:
            scores['neu'] = out_dict[rev]['vNeutral']
        if 'com' in scores:
            scores['com'] = scores['com'] + out_dict[rev]['vCompound']
        else:
            scores['com'] = out_dict[rev]['vCompound']
    for key in scores:
        scores[key] = (scores[key] / len(out_dict)) * 100

    return jsonify(scores)

if __name__ == "__main__":
    app.run()
