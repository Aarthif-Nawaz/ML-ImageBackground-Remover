import os
from flask import Flask,redirect,render_template,request
from werkzeug.utils import secure_filename
import requests
import shutil
import shlex
import json
import subprocess
import random

Background = os.path.join('static', 'Background-Images')
keys = ['cR5VuqsG332s9idv336LrFB4','BJckx2EsNiChs7EmXxq5gRkU','Fx7h8ohWhpsZSZ4GWdbt75Pf','QwebGn4QUwrbwtmpR9VX7GgS','gJJfbMfeHi6782ofpjitppB3','8HUvQ1tmMsDzUqdANBAUoewp','bV84X5XMLP9stMjm2ZTpdH9s']

app = Flask(__name__)
app.config['SECRET_KEY'] = "073129749013740932ABFG879076543"
app.config['UPLOAD_FOLDER'] = Background
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        for file in os.listdir(os.getcwd()+"/static/Background-Images"):
            os.remove(os.path.join(os.getcwd()+"/static/Background-Images", file))
        for file in os.listdir(os.getcwd()+"/"+"static/Non-Background-Images"):
            os.remove(os.path.join(os.getcwd()+"/"+"static/Non-Background-Images",file))
        image = request.files["image"]
        print(image)
        if image.filename == "":
            print("No filename")
            return redirect(request.url)
        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            while True:
                try:
                    response = requests.post(
                        'https://api.remove.bg/v1.0/removebg',
                        files={'image_file': open(filepath, 'rb')},
                        data={'size': 'auto'},
                        headers={'X-Api-Key': random.choice(keys)},
                    )
                    if response.status_code == requests.codes.ok:
                        with open(filename, 'wb') as out:
                            out.write(response.content)
                        shutil.move(os.getcwd() + "/" + filename, os.getcwd() + "/static/Non-Background-Images")
                        return render_template('index.html', con=filename, data=filepath)
                    else:
                        print("Error:", response.status_code, response.text)
                        cmd = f'''curl -X POST -F "file=@{filepath}" "https://api.boring-images.ml/v1.0/transparent-net?api_key=ak-broad-haze-7fff750"'''
                        args = shlex.split(cmd)
                        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = process.communicate()
                        if (str(stdout).__contains__("error")):
                            pass
                        else:
                            response = json.loads(stdout.decode('utf-8'))
                            img = response['result']
                            return render_template('index.html', uri=img, data=filepath)
                except:
                    pass
        else:
            print("That file extension is not allowed")
            return redirect(request.url)
    return render_template('index.html')

if __name__== '__main__':
    app.run(debug=True)


