
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:ArtSearchAm295@127.0.0.1/artsearch')

app = Flask(__name__)

      
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        # receive input from name content in html
        Title = request.get_json()['artName'] 
        print("Get title: ", Title)
        try:
            
            sql = "SELECT `Artist`, `Title`, `image_src` FROM `artsimg` WHERE `Title`=%s"
            #engine.execute(sql, ('Bambocciata (Childishness)',))
            art_obj = engine.execute(sql, (Title,)).fetchall()[0]
            
            return '{};{};{}'.format(art_obj[0], art_obj[1], art_obj[2]) 
        except:
            art_obj = {"Title":"No Input",
                   "image_src":"None", 
                   "Artist":"None"}
            return art_obj
            
    else:
        return "maindb.py - This is get method - try using post -- "


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)  
