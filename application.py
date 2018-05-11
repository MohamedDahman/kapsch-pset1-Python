from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import base64


# Configure application
app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = sqlite3.connect("kapsch.db")


@app.route("/")
def index():

        flash("Wellcome")
        return render_template("index.html")



@app.route("/bindimage", methods=["GET", "POST"])
def bindimage():
    if request.method == "GET" :

        countimages = connection.cursor()
        countimages.execute("select count(*) from images where category is null ")
        numofImgae = countimages.fetchone()[0]
        if (numofImgae == 0):
            return redirect("/")
        if (numofImgae != 0):


            imagecursor = connection.cursor()
            imagecursor.execute("select * from   images where category is null")

            currentData = {}
            currentData = imagecursor.fetchone()

            imgid = currentData[0]
            imgbinary = currentData[1]
            with open("./static/image_name.jpg", "wb") as img:
                img.write(base64.b64decode(imgbinary))


            category = connection.cursor()
            category.execute("select * from category")

            categoryCount = connection.cursor()
            categoryCount.execute("select count(*) from category ")
            count = categoryCount.fetchone()[0]

            rowData = {}  # this is a dict
            listRowData = []  # this is list

            currentRow = 0
            while currentRow <= count - 1:
                rowData = {}
                currCategory = category.fetchone()
                rowData['description'] = currCategory[1]
                rowData['id'] = currCategory[0]
                listRowData.append(rowData)
                currentRow = currentRow + 1

            return render_template("bindImage.html",id=imgid,binary="./static/image_name.jpg" , category=listRowData)
    else:
            imgid = request.form['imgid']
            category = request.form.get('category')

            sql = "update  images set category= ? where id = ?"

            cursor = connection.cursor()
            cursor.execute(sql,  [category , imgid])
            connection.commit()
            return redirect("/bindimage")


@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        file = request.files['image']

        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f)

        with open(f, "rb") as imageFile:
            str1 = base64.b64encode(imageFile.read())
        sql1 ="INSERT INTO images (image) VALUES (?)"

        cursor = connection.cursor()
        cursor.execute(sql1, [str1])
        connection.commit()

        os.remove(f)
        return redirect("/")
    else:
        return render_template("upload_image.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code