import json
import random

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

def getRegex(category, difficulty):
	categories = ["long", "short", "number", "form"]
	functions = [getLongRegex, getShortRegex, getNumberRegex, getFormRegex]
	if category == "any":
		category = categories[random.randint(0,3)]
	for index in range(0,len(categories)):
		if categories[index] == category:
			func = functions[index]
			regex = func(difficulty)
	return {'id': random.randint(0,100000), 'regex': regex}

def getLongRegex(difficulty):
	params = numGroups(difficulty)
	expression = ''
	if params['lookbehind'] == True:
		expression += '(?<=' + getRandomShortSnippet() + ")"
	count = 1
	while count < params['number']:
		expression += getRandomLongSnippet()
		count += 1
	if params['lookahead'] == True:
		expression += '(?=' + getRandomShortSnippet() + ")"
	return expression

def getRandomLongSnippet():
	options = [
		'\w{NUMBER1,NUMBER2}',
		'\w{NUMBER1,}',
		'[ABCabc]{NUMBER1,NUMBER2}',
		'[XYZ]{NUMBER1,NUMBER2}',
		'(The\s|A\s|Any\s)',
		'(Beep\s){NUMBER1, NUMBER2}',
		'\w\w[A-Z]{NUMBER1, NUMBER2}-\w\w',
		'\w\w[^A-Z]{1,}\w\w',
		'\(\w{NUMBER1, NUMBER2}\)',
		'\[[^a-z]{NUMBER1, NUMBER2}\]'
	]
	randomNum1 = random.randint(0,9)
	randomNum2 = random.randint(0,9)
	randomNum2str = str(randomNum2)
	if randomNum2str == '0':
		randomNum2str = '' 
	return options[random.randint(0,len(options) - 1)].replace('NUMBER1', str(randomNum1)).replace('NUMBER2', randomNum2str if randomNum2str == '' else str(randomNum1 + randomNum2))

def getShortRegex(difficulty):
	params = numGroups(difficulty)
	expression = ''
	if params['lookbehind'] == True:
		expression += '(?<=' + getRandomShortSnippet() + ")"
	count = 1
	while count < params['number']:
		expression += getRandomShortSnippet()
		count += 1
	if params['lookahead'] == True:
		expression += '(?=' + getRandomShortSnippet() + ")"
	return expression

def getRandomShortSnippet():
	options = [
		'\w{NUMBER1,NUMBER2}',
		'\w{NUMBER1,}',
		'[ABCabc]{NUMBER1,NUMBER2}',
		'[XYZ]{NUMBER1,NUMBER2}',
		'(The\s|A\s|Any\s)',
		'\w\w[A-Z]{NUMBER1, NUMBER2}-\w\w',
		'\w\w[^A-Z]{1,}\w\w',
		'\(\w{NUMBER1, NUMBER2}\)',
		'\[[^a-z]{NUMBER1, NUMBER2}\]'
	]
	randomNum1 = random.randint(0,3)
	randomNum2 = random.randint(0,2)
	randomNum2str = str(randomNum2)
	if randomNum2str == '0':
		randomNum2str = '' 
	return options[random.randint(0,len(options) - 1)].replace('NUMBER1', str(randomNum1)).replace('NUMBER2', randomNum2str if randomNum2str == '' else str(randomNum1 + randomNum2))


def getNumberRegex(difficulty):
	params = numGroups(difficulty)
	expression = ''
	if params['lookbehind'] == True:
		expression += '(?<=' + getRandomNumberSnippet() + ")"
	count = 1
	while count < params['number']:
		expression += getRandomNumberSnippet()
		count += 1
	if params['lookahead'] == True:
		expression += '(?=' + getRandomNumberSnippet() + ")"
	return expression

def getRandomNumberSnippet():
	options = [
		'\d{NUMBER1,NUMBER2}',
		'\d{NUMBER1,}',
		'[468]{NUMBER1,NUMBER2}',
		'[069]{NUMBER1,NUMBER2}',
		'(47\s|43\s|42\s)',
		'\d\d[2-5]{NUMBER1, NUMBER2}\d-\d',
		'\d\d[^0-9]{1,}\d\d',
		'(\d{NUMBER1, NUMBER2})',
		'\[[1-8]{NUMBER1, NUMBER2}\]'
	]
	randomNum1 = random.randint(0,3)
	randomNum2 = random.randint(0,2)
	randomNum2str = str(randomNum2)
	if randomNum2str == '0':
		randomNum2str = '' 
	return options[random.randint(0,len(options) - 1)].replace('NUMBER1', str(randomNum1)).replace('NUMBER2', randomNum2str if randomNum2str == '' else str(randomNum1 + randomNum2))


def getFormRegex(difficulty):
	params = numGroups(difficulty)
	options = [
		'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*',
		'[\+]?[(]?[0-9]{3,3}[)]?[-\s\.]?[0-9]{3,3}[-\s\.]?[0-9]{4,6}',
		"[(]{0,1}[0-9]{3}[)]{0,1}\s[0-9]{3}[-\s][0-9]{4}",
		"[0-9]{4,4}[\s-][0-9]{4,4}[\s-][0-9]{4,4}[\s-][0-9]{4,4}",
		"(42|44)[0-9]{2,2}[\s-][0-9]{4,4}[\s-][0-9]{4,4}[\s-][0-9]{4,4}",
		"((\-?|\+?)?\d+(\.\d+)?),\s*((\-?|\+?)?\d+(\.\d+)?)",
		"[0-3]?[0-9]/[0-3]?[0-9]/(?:[0-9]{2,2})?[0-9]{2,2}",
		"[0-3][0-9]/[0-3][0-9]/(?:[0-9][0-9])?[0-9][0-9]",
		"\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+",
		"[a-z ,.'-]+$",
		"[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}",
		"[^i*&2@]",
		"//[^\r\n]*[\r\n]",
		"b[aeiou]bble",
		"[b-chm-pP]at|ot",
		"[Bb]rainf\*\*k",
		"\d+(\.\d\d)?",
		"mi.....ft",
		"mi..n..ft"
	]
	expression = ''
	if params['lookbehind'] == True:
		expression += '(?<=' + getRandomNumberSnippet() + ")"
	expression += options[random.randint(0, len(options))]
	if params['lookahead'] == True:
		expression += '(?=' + getRandomNumberSnippet() + ")"
	return expression

def numGroups(difficulty):
	if difficulty == "easy":
		return {'number': 2, 'lookahead': False, 'lookbehind': False}
	if difficulty == "medium":
		return {'number': 3, 'lookahead': True, 'lookbehind': False}
	if difficulty == "hard":
		return {'number': 4, 'lookahead': True, 'lookbehind': False}
	lookahead = True if random.randint(0,1) == 1 else False
	lookbehind = False
	number = random.randint(0,2) + 2
	return { 'number': number, 'lookahead': lookahead, 'lookbehind': lookbehind}
	