import csv
import random

class TravelJourney:

	def __init__(self):
		# Read questions
		file_destination = './csv/travelBot_questions.csv'

		with open(file_destination, 'r') as csvfile:
		 	questions = csv.reader(csvfile, delimiter=',', quotechar='"')
		 	next(questions)
		 	self.keywords = dict()
		 	self.questions = dict()

		 	for row in questions:
		 		self.keywords[row[0]]=None
		 		if row[0] in self.questions:
		 			self.questions[row[0]].append(row[1])
		 		else:
		 			self.questions[row[0]]=[row[1]]

	def set_attribute(self, key, value):
		if key in self.keywords:
			self.keywords[key] = value
		print ("Value %s updated with %d",(key,value))

	def get_attribute(self, key):
		if key in self.keywords:
			return self.keywords[key]
		else:
			return None

	def next_missing(self):
		for key, value in self.keywords.items():
			if value == None:
				return key
		return None

	def get_question(self, key):
		if key in self.keywords:
			return random.choice(self.questions[key])
		return None


if __name__ == "__main__":
	a = TravelJourney()
	key = a.next_missing()
	print a.get_question(key)