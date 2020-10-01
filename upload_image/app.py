from flask import Flask



app = Flask(__name__)
app.secret_key = "secret key"
#app.config['DATABASE_FOLDER'] = DATABASE_FOLDER 
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
