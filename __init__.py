from flask import Flask, request, send_file
from pymongo import MongoClient
app = Flask(__name__)
uri = "mongodb://api:Team4096isthebest@34.87.15.250:37017"
@app.route("/")
def hello():
    x = request.args.get('x')
    return "Hi" + x
@app.route("/test")
def testFunc():
    return "test"
@app.route("/listbooks")
def getBooks():
    client = MongoClient(uri)
    db = client['media']
    booksCollection = db['books']
    query = {}
    cursor = booksCollection.find(query)
    rtn = []
    for document in cursor:
        print(document) #debugging
        doc = {}
        doc["title"] = document["title"]
        doc["image"] = document["image"]
        doc["first"] = document["first"]
        rtn += [doc]
    return rtn
@app.route("/getpage", methods = ['POST', 'GET'])
def getpage():
    if request.method == "POST":
        title = request.form['bookTitle']
        page = request.form['page']
    else:
        title = request.args.get('bookTitle')
        page = request.args.get('page')
    client = MongoClient(uri)
    db = client['media']
    booksCollection = db['books']
    query = {"title": title}
    document = booksCollection.find_one(query)
    print(document) #debugging
    return document["pages"][str(page)]
@app.route("/images")
def getImages():
    book = request.args.get('book')
    img = request.args.get('img')
    path = f"books/{book}/{img}"
    return send_file(path)
if __name__ == "__main__":
    app.run()
