from flask import Flask, render_template, request
import requests
import json
from cs50 import SQL

app = Flask(__name__)
db = SQL("sqlite:///data.db")

@app.route("/")
def home():
    return render_template('index.html', page="home")

@app.route("/checkanswer", methods=['POST'])
def checkanswer():
    questionID = request.json['questionID']
    question = db.execute('SELECT correct_answers FROM questions WHERE id = ?', int(questionID))
    return json.loads(question[0]['correct_answers'])

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
                isCategory = question['category'] == category
                isDifficulty = question['difficulty'] == difficulty
                inList = question['id'] in questionIDs
                inAllQuestions = db.execute('SELECT id FROM questions WHERE id = ?', question['id'])
                if isCategory and isDifficulty and len(questions) < int(limit) and not inList:
                    questions += [question]
                    questionIDs += [question['id']]
                if len(inAllQuestions) == 0:
                    db.execute('INSERT INTO questions (id, question, description, answers, multiple_correct_answers, correct_answers, correct_answer, explanation, tip, tags, category, difficulty) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                    question['id'], str(question['question']), str(question['description']), json.dumps(question['answers']), str(question['multiple_correct_answers']), json.dumps(question['correct_answers']), str(question['correct_answer']), str(question['explanation']), str(question['tip']), json.dumps(question['tags']), str(question['category']), str(question['difficulty'])
                    ) 
        return render_template('untimed.html', page="untimed", loaded=True, data=questions, len=len(questions), datastream=json.dumps(questions), timed=False)
    return render_template('untimed.html', page="untimed", loaded=False, timed=False)