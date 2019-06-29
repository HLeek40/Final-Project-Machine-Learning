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
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

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

fred = session.query(Product.link_image).all()

def init_browser():
  # @NOTE: Replace the path with your actual path to the chromedriver
  executable_path = {"executable_path":"C:\\Users\\kcs34\\AppData\\chromedriver.exe"}
  return Browser("chrome", **executable_path, headless=False)

# browser = init_browser()
# output = []

for u in fred:
    print(u[0])
print(len(fred))
#    url = u[0]
#    browser.visit(url)
#    time.sleep(1)
#    html = browser.html
#    soup = bs(html, "html.parser")
#    fact = soup.find('div',id='imgTagWrapperId')
#    p = fact.find('img')
#    #output.append(p['src'])
#    #print(p['src'])
#    data = {'link_image':p['src']}
#    session.query(Product).filter(Product.link == url).update(data)
#    session.commit()
#    print('made update for\n{}'.format(url))
# browser.quit()

# print("All Done")