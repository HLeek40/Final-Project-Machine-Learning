import pandas as pd
import re

def fix_names(x):
    reg = re.compile(r'[^\x00-\x7f]+',re.UNICODE)
    if(isinstance(x,str)):
        newStr = re.sub(reg,'',x)
        if(len(newStr) < 1):
            newStr = 'no information'
        return newStr
    else:
        return 'no usable text'


df = pd.read_csv('amazon_reviews_no_unicodev1.csv')
new_text = df['review text'].apply(fix_names)
df['review text'] = new_text
new_title = df['title'].apply(fix_names)
df['title'] = new_title
new_author = df['author'].apply(fix_names)
df['author'] = new_author
df.to_csv('amazon_reviews_no_unicodev2.csv')

print(df.dtypes)
for j in df.columns:
    big = 0
    for p in df[j]:
        if(isinstance(p,str)):
            if(len(p) > big):
                big = len(p)
    print("longest STR in column {} is {} bytes".format(j,str(big)))
