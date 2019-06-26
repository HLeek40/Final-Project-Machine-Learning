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
import string
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

Base.prepare(engine, reflect=True)

Product = Base.classes.product
Reviews = Base.classes.reviews
Author = Base.classes.author

session = Session(engine)
array = []
array2 = []

fred = session.query(Reviews.text).all()
for i in fred:
    #joe = i[0].lower()
    # joe = re.sub(r'[^\w]','',joe)
    # print(joe)
    #f = joe.translate(str.maketrans('','',string.punctuation))
    array.append(i[0].lower().translate(str.maketrans('','',string.punctuation)))
    array2.append(i[0])
for j in array:
    print(j)

