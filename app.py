
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
import sys
import requests

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        # receive input from name content in html
        Title = request.form['artName']
        print("Get title: ", Title)
        try:
            print("to db: ", db_url)       
            resp = requests.post(url=db_url,json={'artName':Title})
            art_obj_url = resp.content.decode('utf-8')
            print(type(art_obj_url),art_obj_url)
            art_obj = {"Title": Title,
                       "image_src": art_obj_url, 
                       "Artist":"None"}
            return render_template('index.html', art_obj=art_obj)

        except:
            return 'There was an issue loading art_name'
            
    else:
        # go query all db datapoint order by date created and return
        art_obj = {"Title":"No Input",
                   "image_src":"None", 
                   "Artist":"None"}
        return render_template('index.html', art_obj=art_obj)
    



if __name__=="__main__":
    # determine what the URL for the database should be, port is always 8082 for DB
    if(len(sys.argv) == 2):
        db_url = 'http://' + sys.argv[1] + ':8082'
    else:
        db_url = "http://0.0.0.0:8082/"  
   
    app.run(host='0.0.0.0', port=8081, debug=True)


      
# # GCP
# CLOUDSQL_USER = 'root'
# CLOUDSQL_PASSWORD = 'ArtSearchAm295'
# CLOUDSQL_DATABASE = 'artsearch'
# CLOUDSQL_CONNECTION_NAME = 'ac295-data-science-289013:us-east1:artimages'

# LIVE_SQLALCHEMY_DATABASE_URI = (
#     'mysql+pymysql://{nam}:{pas}@localhost/{dbn}?unix_socket=/cloudsql/{con}').format (
#     nam=CLOUDSQL_USER,
#     pas=CLOUDSQL_PASSWORD,
#     dbn=CLOUDSQL_DATABASE,
#     con=CLOUDSQL_CONNECTION_NAME,
# )

# app.config['SQLALCHEMY_DATABASE_URI'] = LIVE_SQLALCHEMY_DATABASE_URI
#     #'mysql+pymysql://root:ArtSearchAm295@127.0.0.1/artsearch'

# db = SQLAlchemy(app)
# class art(db.Model):
#     Title = db.Column(db.String(255), primary_key=True)
#     Artist = db.Column(db.String(255), nullable=False)
#     image_src = db.Column(db.String(255), nullable=False)

#     def __repr__(self):
#         return '<art %r>' % self.Title

