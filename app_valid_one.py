
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:ArtSearchAm295@127.0.0.1/artsearch')

app = Flask(__name__)

      
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

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        # receive input from name content in html
        Title = request.form['artName']
        #print("Get title: ", Title)
        try:
            ## code for direct read from csv
            #df = pd.read_csv("./metadata.csv")
            ## find art object
            #row = df.loc[df.Title==art_name][['Title','image_src','Artist']]
            #art_obj = row.to_dict('records')[0]
            ## code for read from db
            # print(db) # code to check if connection works
            # for t in db.metadata.tables.items():
            #     print(t)
            sql = "SELECT `Artist`, `Title`, `image_src` FROM `arts` WHERE `Title`=%s"
            #engine.execute(sql, ('Bambocciata (Childishness)',))
            art_obj = engine.execute(sql, (Title,)).fetchall()
            print(art_obj[0])
            return render_template('index.html', art_obj=art_obj[0])
        except:
            return 'There was an issue loading art_name'
            
    else:
        # go query all db datapoint order by date created and return
        art_obj = {"Title":"No Input",
                   "image_src":"None", 
                   "Artist":"None"}
        return render_template('index.html', art_obj=art_obj)
    


if __name__ == "__main__":
    app.run(debug=True)
