from flask import Flask, request
import os
import cv2
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras.models import load_model

META_FOLDER = 'static/database/gap_images'

from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:ArtSearchAm295@34.73.0.192/artsearch')
app = Flask(__name__)

from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:ArtSearchAm295@34.73.0.192/artsearch')
app = Flask(__name__)

def cos_similarity(A,B):
    # A and B are both (32,) numpy array
    res = np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))
    return res

def cos_similarity_2(A,B):
    # A and B are both (32,) numpy array
    res = np.dot(A.reshape(1,128),B.reshape(128,1))/(np.linalg.norm(A)*np.linalg.norm(B))
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

def read_image_2():
    image_file = request.files['upload']
    img_str = image_file.read()
    image_file.close()
    autoencoder = load_model('autoencoder.h5')
    encoder =  Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('encoder').output)
    # CV2
    nparr = np.fromstring(img_str, np.uint8)
    img_obj = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
    img_obj = cv2.cvtColor(img_obj, cv2.COLOR_BGR2GRAY)
    img_obj = cv2.resize(img_obj, dsize = (32,32))
    img = img_obj
    img = img.astype('float32') / 1023.
    img = img.reshape(1, 32, 32, 1)
    img = np.asarray(encoder.predict(img)).reshape(1,-1)
    return img

def search_image_2():
    img_obj = read_image_2()
    filename = ''
    sim = -float('Inf')
     # TODO: read dataframe from DB
    df = pd.read_csv(os.path.join(META_FOLDER, 'image_info_cnn.csv'), index_col=0)
    for i in range(len(df)):
        img_info = df.iloc[i,:].values
        new_sim = cos_similarity_2(img_info, img_obj)
        if new_sim > sim:
            sim = new_sim
            filename = df.iloc[i,]['file_id']
    
    if filename == '':
        url = ''
    else:
        # TODO: read metadata from db
        Title = filename
        sql = "SELECT `image_src` FROM `artsimg` WHERE `file_id`=%s"
        url = engine.execute(sql, (Title,)).fetchall()[0]
        
        # meta = pd.read_csv(os.path.join(META_FOLDER, 'metadata.csv'))
        # url = meta[meta['file_id'] == filename]['image_src'].values[0]

    return url
    
def search_image():
    img_obj = read_image()
    filename = ''
    sim = -float('Inf')

    # TODO: read dataframe from DB
    # df = pd.read_csv(os.path.join(META_FOLDER, 'image_info.csv'), index_col=0)
    # for i in range(len(df)):
    #     img_info = df.iloc[i,:].values
    #     new_sim = cos_similarity(img_info, img_obj)
    #     if new_sim > sim:
    #         sim = new_sim
    #         filename = df.index[i]
    df = pd.read_sql("SELECT * FROM imageinfo", con=engine)
    for i in range(len(df)):
        img_info = df.iloc[i,:-1].values
        
        new_sim = cos_similarity(img_info, img_obj)
        if new_sim > sim:
            sim = new_sim
            filename = df.iloc[i,]['file_id']
    
    if filename == '':
        url = ''
    else:
        # TODO: read metadata from db
        Title = filename
        sql = "SELECT `image_src` FROM `artsimg` WHERE `file_id`=%s"
        url = engine.execute(sql, (Title,)).fetchall()[0]
        
        # meta = pd.read_csv(os.path.join(META_FOLDER, 'metadata.csv'))
        # url = meta[meta['file_id'] == filename]['image_src'].values[0]

    return url[0]

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

      
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        # receive input from name content in html
        if request.get_json():
            art_obj = match_image()
            return art_obj
        elif request.files:
            # url = search_image()
            # return url
            # receive input from name content in html
            val = request.files['button'].read().decode("utf-8") 
            if val  == 'Submit':
                print('hi')
                url = search_image()
            else:
                url = search_image_2()
            return url         

            
    else:
        return "maindb.py - This is get method - try using post -- "

############################## filename_frontend #######################################





if __name__=="__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)  
