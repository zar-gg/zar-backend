from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_patient0():
    return "Hello Patient 0 you fkin noob. Dont Try HArd fk u"
@app.route("/faraz")
def hello_patient01():
    return "Hello Patient 0 you fkin noob. Dont Try HArd fk u"


if __name__ == '__main__':
    app.run("0.0.0.0",port=8000)