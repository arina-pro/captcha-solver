import os

from werkzeug.utils import secure_filename

from flask import Flask, request

def create_app():
    app = Flask(__name__)

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'C:/code/captcha-solver/tmp'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from solver import solve_captcha

    @app.route('/', methods=('GET', 'POST'))
    def captcha():
        if request.method == 'POST':
            file = request.files['file']
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            solved = solve_captcha(path)
            if solved:
                os.remove(path)
                return str(solved)
            #file.seek(0)
            #return file.read()
            #solved = solve_captcha(request.files['file'])
            #if solved:
                #return str(solved)
        return '''
    <!doctype html>
    <title>Upload CAPTCHA image</title>
    <h1>Upload CAPTCHA image</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    
    return app