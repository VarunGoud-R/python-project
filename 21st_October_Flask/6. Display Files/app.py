from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, static_folder='img')
# app.config['UPLOAD_FOLDER'] = 'img'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

global filePath
filePath = app.static_folder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    # filePath = path
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)
        # Check if the file has an allowed extension
        if file and allowed_file(file.filename):
            # Save the file to the uploads folder
            filename = os.path.join(filePath, file.filename)
            print(filename)
            file.save(filename)
            return redirect(url_for('index'))
    # Display the list of uploaded files
    files = os.listdir(filePath)
    print(files)
    return render_template('index.html', files=files, path=filePath)

if __name__ == '__main__':
    # path = app.static_folder
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    app.run(debug=True)
