from flask import Flask, request
import os
import cv2
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
META_FOLDER = 'arts_database/static/database/gap_images'

def cos_similarity(A,B):
    # A and B are both (32,) numpy array
    res = np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))
    return res

def read_image():
    image_file = request.files['upload']
    img_str = image_file.read()
    image_file.close()

    # CV2
    nparr = np.fromstring(img_str, np.uint8)
    img_obj = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
    img_obj = cv2.cvtColor(img_obj, cv2.COLOR_BGR2GRAY)
    img_obj = cv2.resize(img_obj, dsize = (32,32))
    pca = PCA(n_components=1)
    img = pca.fit_transform(img_obj).reshape(32,)

    return img

    
def search_image():
    img_obj = read_image()
    filename = ''
    sim = -float('Inf')

    # TODO: read dataframe from DB
    df = pd.read_csv(os.path.join(META_FOLDER, 'image_info.csv'), index_col=0)
    for i in range(len(df)):
        img_info = df.iloc[i,:].values
        new_sim = cos_similarity(img_info, img_obj)
        if new_sim > sim:
            sim = new_sim
            filename = df.index[i]
    
    if filename == '':
        url = ''
    else:
        # TODO: read metadata from db
        # Title = filename
        # sql = "SELECT `image_src` FROM `artsimg` WHERE `Title`=%s"
        # url = engine.execute(sql, (Title,)).fetchall()[0]

        meta = pd.read_csv(os.path.join(META_FOLDER, 'metadata.csv'))
        url = meta[meta['file_id'] == filename]['image_src'].values[0]

    return url

def match_image():
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


############################## filename_frontend #######################################
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:ArtSearchAm295@127.0.0.1/artsearch')
app = Flask(__name__)

      
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        # receive input from name content in html
        if request.get_json():
            art_obj = match_image()
            return art_obj
        elif request.files:
            url = search_image()
            return url
            
    else:
        return "maindb.py - This is get method - try using post -- "

############################## filename_frontend #######################################





if __name__=="__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)  