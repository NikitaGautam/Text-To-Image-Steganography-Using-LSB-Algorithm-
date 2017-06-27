import os
from flask import Flask, render_template, request
from Services import MainServices
from werkzeug.utils import secure_filename
import MainImplementation
from PIL import Image

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = '/Users/Nikita/StegoImage/'
app.config['UPLOAD_FOLDER'] = '/Users/Nikita/PycharmProjects/TextToImageStego/static/pics/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'tiff'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    MainServices.clean_dir()
    return render_template('index.html')
    # return render_template('retrieveM.html')


@app.route('/upload', methods=['POST'])
def upload():
    MainServices.clean_dir()
    filename = None
    file = request.files['file']
    if file and allowed_file(file.filename):
        print (os.path.realpath(file.filename))
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    message = request.form.get("message", "")
    MainImplementation.messageHide(message)
    print("filename ---", filename)
    return render_template('retrieveM.html',message='', displayVal = False, originalFile = filename)



@app.route('/retrieve', methods=['POST'])
def getMsg():
    message = MainImplementation.messageRetrieve()
    print("secret message----", message)
    return render_template('retrieveM.html', displayVal= True, message=message)


@app.errorhandler(Exception)
def all_exception_handler(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run()
