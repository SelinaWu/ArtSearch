
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
 
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        # receive input from name content in html
        art_name = request.form['artName']
        
        try:
            df = pd.read_csv("./metadata.csv")
            # find art object
            row = df.loc[df.Title==art_name][['Title','image_src','Artist']]
            art_obj = row.to_dict('records')[0]
            #TODO: Art.query.get_or_404(art_name)
            return render_template('index.html', art_obj=art_obj)
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
