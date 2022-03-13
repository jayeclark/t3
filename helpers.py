import json

def evaluateQuestion(question, category, difficulty, questionIDs, db):
	isCategory = True if (category == "Any" or question['category'] == category) else False
	isDifficulty = True if (difficulty == "Any" or question['difficulty'] == difficulty) else False
	inList = question['id'] in questionIDs
	inAllQuestions = db.execute('SELECT id FROM questions WHERE id = ?', question['id'])
	if len(inAllQuestions) == 0:
		answers = question['answers']
		safeAnswers = {}
		for answer in answers:
			safeAnswer = answers[answer]
			if safeAnswer:
				safeAnswers[answer] = answers[answer].replace('\'', '').replace('?','')
		db.execute('INSERT INTO questions (id, question, description, answers, multiple_correct_answers, correct_answers, correct_answer, explanation, tip, tags, category, difficulty) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
		question['id'], str(question['question']), str(question['description']), json.dumps(safeAnswers), str(question['multiple_correct_answers']), json.dumps(question['correct_answers']), str(question['correct_answer']), str(question['explanation']), str(question['tip']), json.dumps(question['tags']), str(question['category']), str(question['difficulty'])
		) 
	if isCategory and isDifficulty and not inList:
		return True
	return False

def addToList(question, questions, questionIDs):
	questions += [question]
	questionIDs += [question['id']]