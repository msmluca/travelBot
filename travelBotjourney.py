import csv
import random

class travelBotjourney:

	def __init__(self):
		# Read questions
		self.start()

	def start(self):
		file_destination = './csv/travelBot_questions.csv'

		with open(file_destination, 'r') as csvfile:
		 	questions = csv.reader(csvfile, delimiter=',', quotechar='"')
		 	next(questions)
		 	self.bot_results = dict()
		 	self.answer = dict()
		 	self.questions = dict()
		 	self.answers_status = dict()

		 	for row in questions:
		 		self.answer[row[0]]=[]

		 		if row[0] in self.questions:
		 			self.questions[row[0]].append(row[1])
		 		else:
		 			self.questions[row[0]]=[row[1]]

		 		if row[2] == 'NONE':
		 			self.answers_status[row[0]] = {'type':row[2],'complete':1}
		 		else:
		 			self.answers_status[row[0]] = {'type':row[2],'complete':0}

		 		print row
		 		if len(row[3])>0:
		 			self.answers_status[row[0]]['answers'] = {}
		 			for ans in row[3].split(","):
		 				answer, value = ans.split(":",1)
						self.answers_status[row[0]]['answers'][answer]=value

		 	print self.questions

	def has_options(self, key):
		if 'answers' in self.answers_status[key].keys():
			return True
		return False

	def get_options(self, key):
		ret = [[x] for x in self.answers_status[key]['answers'].keys()]
		return ret

	def valid_option(self, key, ans):
		if ans in self.answers_status[key]['answers'].keys():
			return self.answers_status[key]['answers'][ans]
		return None

	def set_attribute(self, key, value):
		if key in self.answers_status:
			# Question with limit list of options
			if self.has_options(key):
				ret = self.valid_option(key, value)
				if ret != None:
					self.answer[key] = ret

			# question that accept any int
			elif self.answers_status[key]['type'] == 'INT':
				if value.isdigit():
					if key == 'MAXBUDGET' and int(value) < 50:
						return -1, 'ERROR_' + key
					else:
						self.answer[key] = int(value)
				else:
				 return -1, 'ERROR'
			else:
				self.answer[key] = value

		print self.answer
		return 1, 'OK'

	# def set_attribute(self, key, value):
	# 	if key in self.answers_status:
	# 		if self.answers_status[key]['type'] == 'LIST':
	# 			self.answer[key].append(value)
	# 		elif self.answers_status[key]['type'] == 'INT':
	# 			if value.isdigit():
	# 				if key == 'MAXTRAVELTIME' and int(value) < 1:
	# 					return -1, 'ERROR_' + key
	# 				if key == 'MAXBUDGET' and int(value) < 50:
	# 					return -1, 'ERROR_' + key
	# 				self.answer[key] = int(value)
	# 			else:
	# 			 return -1, 'ERROR'
	# 		else:
	# 			self.answer[key] = value

	# 	print self.answer
	# 	return 1, 'OK'

	def complete_answer(self, key, complete):
		if key in self.answers_status:
			self.answers_status[key]['complete'] = complete

	def get_answer_type(self, key):
		if key in self.answers_status:
			return self.answers_status[key]['type']
		return None

	def get_attribute(self, key):
		if key in self.answers_status:
			return self.answer[key]
		else:
			return None

	def add_results(self, i, key, details):
		self.bot_results[i] = {'location': key, 'details' : details}

	def get_results(self, i):
		return self.bot_results[i]

	def next_missing(self):
		for key, value in self.answers_status.items():
			if value['complete'] == 0:
				print("NExt question is",key)
				return key
		return None

	def get_question(self, key):
		if key in self.answers_status:
			return random.choice(self.questions[key])
		return None


if __name__ == "__main__":
	a = travelBotjourney()
	key = a.next_missing()
	print a.get_question(key)