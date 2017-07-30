from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

@app.route("/FaceRecognition")
def index():
    return render_template("client.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
    
