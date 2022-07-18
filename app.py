
from flask import Flask, render_template

app = Flask(__name__)

#The decorator @app.route(‘/hello’) indicates the URL endpoint of the webpage.
#And what the webpage will show is written in the function below.
@app.route('/index')
def index():
    return render_template("index.html")



# start the serveur and mention the port -> 5000 itself
app.run(host='localhost', port=5000)