from flask import Flask, request
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

DATABASE_FOLDER= 'arts_database/static/database/gap_images/gap_images'
UPLOAD_FOLDER= 'arts_database/static/uploads'

def cos_similarity(A,B):

    # TODO calculate the similarity of two images
    return 1

def read_database():
    image_list = []
    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(DATABASE_FOLDER):
        for item in f:
            if '.jpg' in item:
                image_list.append(os.path.join(r, item))
    return image_list
    
@app.route("/",methods=['POST','GET'])
def search_image():

    # TODO: find the image with the closest similarity in database
    file_path = os.path.join(UPLOAD_FOLDER, request.get_json()['upload'])
    image_file = plt.imread(file_path)
    return_image = None
    filename = ''

    image_list = read_database()
    sim = 0
    for img in image_list[:10]:
        img_obj = plt.imread(img)
        new_sim = cos_similarity(image_file, img_obj)
        if new_sim > sim:
            sim = new_sim
            return_image = img_obj
            filename = img
    
    return_filename = filename.split('/')[-1]
    return return_filename
    #return return_image, filename



if __name__=="__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)  