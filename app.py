from selenium import webdriver
import time
import os
from flask import Flask,redirect,render_template,request
from werkzeug.utils import secure_filename
from pathlib import Path

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd()+"/"+"static/Non-Background-Images/",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
#chrome_options.add_argument('--headless')



def convert(image,name):
    while True:
        try:
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
            driver.get('https://www.slazzer.com/upload')
            print("Started")
            break
        except:
            pass
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/input').send_keys(image)
            break
        except:
            pass
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div/div[1]/div/div[1]/button').click()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div/div[1]/div/div[1]/div/a[2]/span').click()
            break
        except:
            pass
    my_file = Path(os.getcwd() + "/" + f"static/Non-Background-Images/{name}")
    while True:
        if my_file.is_file():
            driver.close()
            break
        else:
            pass
    return True
Background = os.path.join('static', 'Background-Images')

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
            p = Path(filepath)
            p = p.rename(p.with_suffix('.png'))
            filename1 = str(p).split("/")[-1]
            print(filename1)
            c = convert(os.getcwd()+"/"+str(p),filename1)
            return render_template('index.html', con=filename1, data=str(p))
        else:
            print("That file extension is not allowed")
            return redirect(request.url)
    return render_template('index.html')






if __name__== '__main__':
    app.run(debug=True)


