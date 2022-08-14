import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from sqlite3 import Error
import string
import random
import json
import pyttsx3
from gtts import gTTS
import codecs
from pydub import AudioSegment
import re

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

def queryDB(query, vals = ()):
    myConn = create_connection(r"proj2.db")
    myConn.row_factory = sqlite3.Row
    cur = myConn.cursor()
    cur.execute(query, vals)
    myConn.commit()
    answer = cur.fetchall()
    myConn.close()
    return answer

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def convertTTS(text):
    # tts = gTTS(text)
    # tts.save("tossup.mp3")
    print("initializing")
    engine = pyttsx3.init()
    #engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
    print("saving")
    engine.save_to_file(text, "tossup.mp3")
    print("running")
    engine.runAndWait()
    print('saved')


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        print("posted")
        categories = request.form.get("categories").split(",")
        difficulties = request.form.get("difficulties").split(",")
        print(categories)
        print(difficulties)
        allCategories = ["Current Events", "Fine Arts", "Geography", "History", "Literature", "Mythology", "Philosophy", "Religion", "Science", "Social Science", "Trash"]
        allDifficulties = ["Middle School", "Easy High School", "Regular High School", "Hard High School", "National High School", "Easy College", "Regular College", "Hard College", "Open"]

        if len(categories) == 0:
            categories = allCategories
        else:
            categories = [allCategories[int(x)] for x in categories]
        
        if len(difficulties) == 0:
            difficulties = allDifficulties
        else:
            difficulties = [allDifficulties[int(x)] for x in difficulties]

        categories = ["category = '" + c + "'" for c in categories]
        difficulties = ["difficulty = '" + d + "'" for d in difficulties]
        qStr = "SELECT * FROM tossups WHERE (" + " OR ".join(categories) + ") AND (" + " OR ".join(difficulties) + ") ORDER BY RANDOM() LIMIT 1"
        print(qStr)
        tossup = queryDB(qStr, ())
        tossup = dict(tossup[0])
        myBody = tossup["body"]
        
        myBody = re.sub("\(\*\)", "", myBody)
        myBody = re.sub("\(...*?\)", "", myBody)
        myBody = re.sub("\[...*?\]", "", myBody)
        myBody = re.sub("^[0-9]*\.", "", myBody)
        myBody = re.sub("\s+", " ", myBody)
        print(myBody)

        myAns = tossup["answer"]
        convertTTS(myBody)
        myFile = open("tossup.mp3", "rb").read()
        # print(myFile)
        # print(type(myFile))
        myFile = codecs.encode(myFile, "base64")
        audio = AudioSegment.from_file("tossup.mp3")
        myDict = {"status": 200, "body": myFile.decode(), "question_text": tossup["formatBody"], "answer_text": myAns, "difficulty": tossup["difficulty"], "duration": audio.duration_seconds}
        #print(myDict)
        #print(json.dumps(myDict))
        #print(json.dumps(myFile))
        return json.dumps(myDict)
        #return HttpResponse(myFile, mimetype="audio/mpeg") 
    else:
        return render_template('index.html')


