from flask import Flask, render_template, request
import requests
import json
import re
from cs50 import SQL
from helpers import evaluateQuestion, addToList, getRegex

app = Flask(__name__)
db = SQL("sqlite:///data.db")

@app.route("/")
def home():
    return render_template('index.html', page="home")

@app.route("/about")
def about():
    return render_template('about.html', page="about")

@app.route("/checkanswer", methods=['POST'])
def checkanswer():
    questionID = request.json['questionID']
    question = db.execute('SELECT correct_answers FROM questions WHERE id = ?', int(questionID))
    return json.loads(question[0]['correct_answers'])

@app.route("/checkregex", methods=['POST'])
def checkregex():
    regex = request.json['regex'].replace('&lt;','<').replace('&gt;','>')
    guess = request.json['guess']
    print(regex, guess)
    my_regex = r''+regex
    matchExists = True if not re.search(my_regex, guess) == None else False
    return 'true' if matchExists == True else 'false'

@app.route("/regex", methods=['GET','POST'])
def regex():
    if request.method == 'POST':
        category = request.form['category']
        limit = request.form['limit']
        difficulty = request.form['difficulty']
        questions = []
        questionIDs = []
        while len(questions) < int(limit):
            response = getRegex(category, difficulty)
            if (response['id'] not in questionIDs):
                questions += [response]
        return render_template('regex.html', page="regex", loaded=True, data=questions, len=len(questions))
    return render_template('regex.html', page="regex", loaded=False)


@app.route("/untimed/", methods=['GET','POST'])
def untimed():
    if request.method == 'POST':
        category = request.form['category']
        limit = request.form['limit']
        difficulty = request.form['difficulty']
        questions = []
        questionIDs = []
        headers = {
            'X-Api-Key': 'we8GiS6gSJC4TpYB1KCPMjGvgyWnrbvTNQNUfqX7' 
        }
        while len(questions) < int(limit):
            response = requests.get('https://quizapi.io/api/v1/questions', headers=headers).json()
            for question in response:
                shouldAdd = evaluateQuestion(question, category, difficulty, questionIDs, db)
                if shouldAdd and len(questions) < int(limit):
                    addToList(question, questions, questionIDs)
        return render_template('quiz.html', page="untimed", loaded=True, data=questions, len=len(questions), timed=False)
    return render_template('quiz.html', page="untimed", loaded=False, timed=False)

@app.route("/timed/", methods=['GET','POST'])
def timed():
    if request.method == 'POST':
        category = request.form['category']
        mode = request.form['limit']
        limit = 9
        available = 120000
        if mode == "five":
            limit = 18
            available = 300000
        elif mode == "max":
            limit = 48
            available = 600000
        difficulty = request.form['difficulty']
        questions = []
        questionIDs = []
        headers = {
            'X-Api-Key': 'we8GiS6gSJC4TpYB1KCPMjGvgyWnrbvTNQNUfqX7' 
        }
        while len(questions) < int(limit):
            response = requests.get('https://quizapi.io/api/v1/questions', headers=headers).json()
            for question in response:
                shouldAdd = evaluateQuestion(question, category, difficulty, questionIDs, db)
                if shouldAdd and len(questions) < int(limit):
                    addToList(question, questions, questionIDs)
        return render_template('quiz.html', page="timed", loaded=True, data=questions, len=len(questions), timed=True, available=available)
    return render_template('quiz.html', page="timed", loaded=False, timed=True)