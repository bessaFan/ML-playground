
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    f = open("main.html","r") #opens file with name of "test.txt"
    return f.read()

if __name__ == "__main__":
    app.run()
