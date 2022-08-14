# import pyttsx3
# s = "A set of m of these quantities is listed in ascending order, and the k-th largest is compared to k over m times another quantity, in the Benjamini-Hochberg procedure. Negative two times the sum of the logarithms of a set of these quantities is analyzed in a method of meta-analysis named for Fisher. An upper bound on a set of m of these quantities is divided by m in a technique that applies the union bound to control the FWER, which is the Bonferroni correction. By definition, these quantities are uniformly distributed under H0 . The multiple comparisons problem can lead to the so-called “hacking” of these quantities, whose size is often depicted using one, two, or three asterisks when reporting the results of a hypothesis test. For 10 points, name these quantities whose size relative to the significance level determines whether the null hypothesis is rejected."

# engine = pyttsx3.init()
# engine.save_to_file(s, "test.mp3")
# engine.runAndWait()



# import os
# from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
# from datetime import datetime
# from tempfile import mkdtemp
# from werkzeug.security import check_password_hash, generate_password_hash
# import sqlite3
# from sqlite3 import Error
# import string
# import random
# import json
# import pyttsx3
# import time

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

def queryDB(query, vals = ()):
    myConn = create_connection(r"/mnt/c/Users/aepst/Documents/Projects/Project2/proj2.db")
    myConn.row_factory = sqlite3.Row
    cur = myConn.cursor()
    cur.execute(query, vals)
    myConn.commit()
    answer = cur.fetchall()
    myConn.close()
    return answer

# addingQs = False
# gettingQs = False
# print(queryDB("SELECT * FROM tossups", ()))
# #def addQuestions(textFile, database):
    

# # while True:
# #     if addingQs:
# #         question = input("Enter your question:\n")
# #         if question == "quit":
# #             addingQs = False
# #             continue
# #         answer = input("Enter the answer to the question:\n")
# #         queryDB("INSERT INTO tossups (body, answer) VALUES (?, ?)", (question, answer))
# #         print("--------------------------------------")
# #     elif gettingQs:
# #         correct = 0
# #         total = 0
# #         myQs = queryDB("SELECT * FROM tossups ORDER BY RANDOM()")
# #         done = False
# #         for q in myQs:
# #             q = dict(q)
# #             ques = q["body"]
# #             ans = q["answer"]
# #             print("Question: " + ques)
# #             input("Your answer: ")
# #             print("Answer: " + ans)
# #             gotIt = input("Enter y if you got it or n if not: ")
# #             if gotIt.lower() == "y":
# #                 correct += 1
# #             total += 1
# #             cont = input("Enter y for continue: ")
# #             if cont.lower() != "y":
# #                 done = True
# #                 break
# #             print("----------------------------------------")
# #         if done:
# #             print("Portion correct: " + str(correct) + "/" + str(total))
# #             gettingQs = False
# #     else:
# #         try:
# #             resp = int(input("Type 1 for add question or 2 for get question: "))
# #             if resp == 1:
# #                 addingQs = True
# #             else:
# #                 gettingQs = True
# #         except:

# #             break

# # from gtts import gTTS
# # tts = gTTS("Hello world Hello world Hello world Hello world Hello world Hello world Hello world Hello world Hello world Hello world Hello world")
# # tts.save("test.mp3")

# # # # import pyttsx3
# # # # engine = pyttsx3.init()
# # # # engine.setProperty('rate', 150)
# # # # engine.save_to_file("I love my mom", "test.mp3")
# # # # engine.runAndWait()
# # from mutagen.mp3 import MP3
# # audio = MP3("test.mp3")
# # print(audio.info.length)

import json
import re
s = "The answer is (definitely totally) what I think it should [maybe, probably] be!"
s = re.sub("\(.*\)", "", s)
print(s)
s = re.sub("\[.*\]", "", s)
print(s)
with open("sample_questions.json", "r") as myFile:
    data = json.load(myFile)
allTossups = data["data"]["tossups"]
queryDB("DELETE FROM tossups2", ())
for myTossup in allTossups:
    myQuestion = myTossup["text"]
    #clean question
    myQuestion = re.sub("\(.*?\)", "", myQuestion)
    myQuestion = re.sub("\[.*?\]", "", myQuestion)
    myQuestion = re.sub("  ", " ", myQuestion)

    myFormatQuestion = myTossup["formatted_text"]
    myAnswer = myTossup["formatted_answer"]
    myDifficulty = ""
    myCategory = ""
    mySubcategory = ""
    if "difficulty" in myTossup["tournament"]:
        myDifficulty = myTossup["tournament"]["difficulty"]
    if "name" in myTossup["category"]:
        myCategory = myTossup["category"]["name"]
    if "name" in myTossup["subcategory"]:
        mySubategory = myTossup["subcategory"]["name"]

    queryDB("INSERT INTO tossups2 (body, formatBody, answer, difficulty, category, subcategory) VALUES (?, ?, ?, ?, ?, ?)", (myQuestion, myFormatQuestion, myAnswer, myDifficulty, myCategory, mySubcategory))

print(queryDB("SELECT * FROM tossups2 ORDER BY RANDOM() LIMIT 5", ()))



# s = "A set of m of these quantities is listed in ascending order, and the kth largest is compared to k over m times another quantity, in the Benjamini-Hochberg procedure. Negative two times the sum of the logarithms of a set of these quantities is analyzed in a method of meta-analysis named for Fisher. An upper bound on a set of m of these quantities is divided by m in a technique that applies the union bound to control the FWER, which is the Bonferroni correction. By definition, these quantities are uniformly distributed under H0 . The multiple comparisons problem can lead to the so-called “hacking” of these quantities, whose size is often depicted using one, two, or three asterisks when reporting the results of a hypothesis test. For 10 points, name these quantities whose size relative to the significance level determines whether the null hypothesis is rejected."
# import pyttsx3

# engine = pyttsx3.init("espeak")
# engine.save_to_file(s, "test.mp3")
# engine.runAndWait()



# # for i in range(100):
# #     print(i)
# #     tts = gTTS("Hello " + str(i))
# #     tts.save("test.mp3")

# # import json
# # import codecs
# # import base64

# # myFile = open("tossup.mp3", "rb").read()
# # #myFile = b'\xff\xf3D\xc4\x00\x12\x18I\xf8'
# # print(myFile)
# # base64_data = codecs.encode(myFile, 'base64') #bytes to b64
# # #print(base64_data)
# # newData = base64_data.decode() #b64 to utf-8
# # #print(newData)
# # myDict = {"status": 200, "body": newData}
# # #print(myDict)
# # myJson = (json.dumps(myDict))
# # #print(myJson)
# # # print(type(myJson))

# # import base64
# # y = json.loads(myJson)
# # #print(y)
# # body = y["body"].encode('utf-8')
# # #print(body)
# # origFile = codecs.decode(body, "base64") #b64 to bytes
# # print(origFile)
# # # bytes_orig = b'\xff\xf3D\xc4\x00\x12\x18I\xf8'

# # myBytes = b'[{\'status\': 200, \'body\': ' + bytes_orig + b'}]'
# # print(myBytes)

# # my_json = myBytes.decode('utf8').replace("'", '"')
# # print(my_json)

# # data = json.loads(my_json)
# # print(data)
# # s = json.dumps(data, indent=4, sort_keys=True)
# # print(s)