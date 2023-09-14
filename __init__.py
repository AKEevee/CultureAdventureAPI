from flask import Flask
from flask import request
app = Flask(__name__)
@app.route("/")
def hello():
    x = request.args.get('x')
    return "Hi" + x
@app.route("/test")
def testFunc():
    return "test"
if __name__ == "__main__":
    app.run()
