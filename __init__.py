from flask import Flask, request, send_file
from pymongo import MongoClient
import requests
from bson import ObjectId
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
        doc["bookID"] = str(document["_id"])
        doc["image"] = document["image"]
        doc["first"] = document["first"]
        rtn += [doc]
    return rtn
@app.route("/getpage", methods = ['POST', 'GET'])
def getpage():
    if request.method == "POST":
        id = request.form['bookID']
        page = request.form['page']
    else:
        id = request.args.get('bookID')
        page = request.args.get('page')
    client = MongoClient(uri)
    db = client['media']
    booksCollection = db['books']
    query = {"_id": ObjectId(id)}
    document = booksCollection.find_one(query)
    print(document) #debugging
    if str(page) in document["pages"]:
        return document["pages"][str(page)]
    else:
        return {"status_code": 202}

@app.route("/generatepage")
def generatePage():
    id = request.args.get('bookID')
    pageID = request.args.get('page')

    client = MongoClient(uri)
    db = client['media']
    booksCollection = db['books']
    query = {"_id": ObjectId(id)}
    document = booksCollection.find_one(query)

    api_key = "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"
    model = "gpt-3.5-turbo"
    prompt = "come up with a part of a short story about a day in the life of a Singaporean in continuation of the following passage: " + document["pages"]["0"]["content"] 
    currPage = ""
    for char in pageID[:-1]: #exclude last char
        currPage += char
        prompt += " " + document["pages"][currPage]["content"]
    prompt += " The main character decided to do this: " +  document["pages"][pageID[:-1]]["options"][int(pageID[-1])-1]["header"]
    prompt += "\n\n\n"
    prompt += "Include 4 options of continuing the story\n"
    prompt += "the theme is cultural preservation and historical\n"
    prompt += "the story should be presented in an role-playing format\n"
    prompt += "the option heading should being an action that the main character took such as check out the nearby painting\n"
    prompt += "the output should include:\n"
    prompt += "1. one short story between 50 and 100 words, enclosed in square brackets\n"
    prompt += "2. four options for continuing the story, hard limit on each option is 8 words, enclosing each option with <1>, <2>, <3>, and <4> respectively"

    res = requests.post(f"https://api.openai.com/v1/chat/completions",
          headers = {
              "Content-Type": "application/json",
              "Authorization": f"Bearer {api_key}"
          },
          json={
              "model": model,
              "messages": [{"role": "user", "content": f"{prompt}"}],
          }).json()
    #debug
    print(res['choices'][0]['message']['content'])
    text = res['choices'][0]['message']['content']
    content = text[text.find("[")+1:text.find("]")] #extract story
    print("\n", content, "\n")
    #extract options
    option1 = text[text.find("<1>")+3:text.find("<2>")]
    option2 = text[text.find("<2>")+3:text.find("<3>")]
    option3 = text[text.find("<3>")+3:text.find("<4>")]
    option4 = text[text.find("<4>")+3:]
    print("\n", option1, option2, option3, option4, "\n")
    #generating img
    res = requests.post(f"https://api.openai.com/v1/images/generations",
          headers = {
              "Content-Type": "application/json",
              "Authorization": f"Bearer {api_key}"
          },
          json={
              "n":1,
              "size":"1024x1024",
              "prompt": "give traditional art form to depict this story: " + content
          }).json()
    print(res)
    url = res['data'][0]['url']
    r = requests.get(url, allow_redirects=True)
    open(f"books/{id}/{pageID}.png", 'wb').write(r.content)

    opt = [{"header": option1,"linkedPage": pageID + "1"}, {"header": option2,"linkedPage": pageID + "2"}, {"header": option3,"linkedPage": pageID + "3"}, {"header": option4,"linkedPage": pageID + "4"}]
    subdoc = {"content": content, "audio": "URL", "image": f"http://ai.bdp.blue/images?book={id}&img={pageID}.png", "options": opt}
    document["pages"][pageID] = subdoc

    booksCollection.update_one(query, {'$set' :document})

    return {"status_code": 200}

@app.route("/images")
def getImages():
    book = request.args.get('book')
    img = request.args.get('img')
    path = f"books/{book}/{img}"
    return send_file(path)
if __name__ == "__main__":
    app.run()
