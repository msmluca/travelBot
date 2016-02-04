import csv
import random

class travelBotjourney:

	def __init__(self):
		# Read questions
		file_destination = './csv/travelBot_questions.csv'

		with open(file_destination, 'r') as csvfile:
		 	questions = csv.reader(csvfile, delimiter=',', quotechar='"')
		 	next(questions)
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
		 			

	def set_attribute(self, key, value):
		if key in self.answers_status:
			if self.answers_status[key]['type'] == 'LIST':
				self.answer[key].append(value)
			elif self.answers_status[key]['type'] == 'INT':
				if value.isdigit():
					self.answer[key] = int(value)
				else:
				 return -1
			else:
				self.answer[key] = value

		print self.answer

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