import pickle
import nltk
import csv
import os.path

from nltk.corpus import movie_reviews, names
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer



word_features = []


class travelBotnltk():
	def __init__(self):

		# load last classifier
		if os.path.isfile("naivebayes.pickle") :
			classifier_f = open("naivebayes.pickle", "rb")
			self.classifier = pickle.load(classifier_f)
			classifier_f.close()
		if os.path.isfile("all_words.pickle"): 
			all_words_f = open("all_words.pickle", "rb")
			self.all_words = pickle.load(all_words_f)
			all_words_f.close()

	def train(self):
		train_set = self.load_training_set("./travelBot_chat.csv")
		self.t, self.all_words = self.create_train(train_set)
		self.classifier = nltk.NaiveBayesClassifier.train(self.t)
		self.classifier.show_most_informative_features(20)

	def save(self):
		save_classifier = open("naivebayes.pickle","wb")
		pickle.dump(self.classifier, save_classifier)
		save_classifier.close()
		save_all_words = open("all_words.pickle","wb")
		pickle.dump(self.all_words, save_all_words)
		save_all_words.close()

	def classify(self, text):
		test = self.create_test(text, self.all_words)
		res = self.classifier.classify(test)
		return res

	def load_training_set(self, file_name):
		training_set = []
		with open(file_name, 'r') as csvfile:
			sentence = csv.reader(csvfile, delimiter=',', quotechar='"')
			# skip the header
			next(sentence)
			for row in sentence:
				training_set.append((row[0],row[1]))
				
		return training_set

	def create_train(self, train_set):
		all_words = set()
		ps = PorterStemmer()
		t = []
		words_tag = []
		for passage in train_set:			
			words_token = word_tokenize(passage[0].lower())		
			words_token = [ps.stem(w) for w in words_token]
			# convert numbers to keyword DIGIT
			words_tag.append((['DIGIT' if word[1] == 'CD' else word[0] for word in pos_tag(words_token)],passage[1]))		
			for word in words_tag[-1][0]:							
				all_words.add(word)			

		for passage in words_tag:		
			t.append(({word: (word in passage[0]) for word in all_words}, passage[1]))

		return t, all_words


	def create_test(self, test_sentence, all_words):
		ps = PorterStemmer()
		words_token = word_tokenize(test_sentence.lower())		
		words_token = [ps.stem(w) for w in words_token]
		# convert numbers to keyword DIGIT
		words_tag = ['DIGIT' if word[1] == 'CD' else word[0] for word in pos_tag(words_token)]
		t = {word: (word in words_tag) for word in all_words}
		return t

			#words = word_tokenize(row[0].lower())
		
			#words = [ps.stem(w) for w in words]
			
			#stop_words = set(stopwords.words('english'))
			#words_out = {}
			#for w in words:
			# 	if not w in stop_words:
			# 		words_out[w] = 1

			# for w in words:
			# 	all_words.append(w.lower())
# training.append([words,row[1]])
# 		all_words = nltk.FreqDist(all_words)
						
			#tokenized = pos_tag(words)
			#print tokenized

			#chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
			#chunkParser = nltk.RegexpParser(chunkGram)
			#chunked = chunkParser.parse(tokenized)
			#chunked.draw()     			



if __name__ == "__main__":
	a = travelBotnltk()
	#a.train()
	#a.save()
	b = a.classify("can travel for more than 2 hours")
	print(b)