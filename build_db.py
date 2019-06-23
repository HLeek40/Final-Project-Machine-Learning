import json
import os
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Boolean
import psycopg2
import sys
import re
from datetime import datetime

db_server = 'project-3-db.cnsppazvk5qa.us-east-2.rds.amazonaws.com'
db_port = 5432
db_pass = 'fred007!'
db_user = 'root'
db_name = 'projectDB'

Base = automap_base()

try:
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(db_user,db_pass,db_server,db_name))
except:
    print(sys.exc_info()[0])
    exit
meta = MetaData()

df = pd.read_csv('amazon_reviews_no_unicodev4.csv')

product = Table(
    'product', meta,
    Column('product_id',String(15),primary_key=True),
    Column('product_cat',String(50)),
    Column('name',String(200)),
    Column('link',String(40)),
    Column('link_image',String(250)),
    Column('amazon_price',String(25))
)

review = Table(
    'reviews', meta,
    Column('id',Integer,primary_key=True),
    Column('product_id',String(15)),
    Column('author_id',String(110)),
    Column('review_url',String(100)),
    Column('title',String(250)),
    Column('text',String(4200)),
    Column('input_date',DateTime(),nullable=True),
    Column('input_time',DateTime(),nullable=True),
    Column('stars',Integer),
    Column('vine',Boolean),
    Column('verified',Boolean)
)

author = Table(
    'author', meta,
    Column('author_id',String(110),primary_key=True),
    Column('city',String(100)),
    Column('state',String(50)),
    Column('longitude',String(50)),
    Column('latitude',String(50))
)

meta.create_all(engine)

Base.prepare(engine, reflect=True)

Product = Base.classes.product
Reviews = Base.classes.reviews
Author = Base.classes.author

session = Session(engine)

# for index, row in df.iterrows():
#     tStr = row['inputtime'] + " " + row['inputtime1'] + row['inputtime2']
#     dt = datetime.strptime(tStr, '%m/%d/%Y %I:%M:%S%p')
#     ret = session.query(Product.product_id).filter(Product.product_id == row['product']).first()
#     if not ret:
#         prod = Product(product_id = row['product'],product_cat = row['product category'],name = row['name'], link = row['Product Link'])
#         session.add(prod)
#         print("adding product record for {}".format(row['product']))
#     ret = session.query(Reviews.review_url).filter(Reviews.review_url == row['reviewlink']).first()
#     if not ret:
#         rev = Reviews(product_id = row['product'],author_id = row['author'],review_url = row['reviewlink'],title = row['title'],text = row['review text'],input_time = dt, stars = row['stars'],vine = row['vine'],verified = row['verified'])
#         session.add(rev)
#         print('adding review record for {} by {}'.format(row['product'],row['author']))
#     ret = session.query(Author.author_id).filter(Author.author_id == row['author']).first()
#     if not ret:
#         auth = Author(author_id = row['author'])
#         session.add(auth)
#         print("adding author record for {}".format(row['author']))
#     session.commit()

products = session.query(Reviews.review_url).all()

for i in products:
    print(i)
print(str(len(products)))