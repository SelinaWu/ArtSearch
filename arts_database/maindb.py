from flask import Flask, request
import os
import cv2
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

app = Flask(__name__)

DATABASE_FOLDER= 'arts_database/static/database/gap_images/gap_images'
META_FOLDER = 'arts_database/static/database/gap_images'
UPLOAD_FOLDER= 'arts_database/static/uploads'

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

    
@app.route("/",methods=['POST','GET'])
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
        meta = pd.read_csv(os.path.join(META_FOLDER, 'metadata.csv'))
        url = meta[meta['file_id'] == filename]['image_src'].values[0]

    return url



if __name__=="__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)  