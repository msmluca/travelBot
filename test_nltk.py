import pickle
import nltk
import csv

from nltk.corpus import movie_reviews, names
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer



word_features = []

def find_features(document):
	ps = PorterStemmer()
	words = set(document)
	words = [ps.stem(w) for w in words]
	stop_words = set(stopwords.words('english'))
	words = [w for w in words if not w in stop_words]

	features = {}
	print words
	for w in word_features:    	
		features[w] = (w in words)

	print features
	return features

def load_training_set(file_name):
	training = list()

	ps = PorterStemmer()
	
	all_words = []	
	training_set = []

	with open(file_name, 'rb') as csvfile:
		sentence = csv.reader(csvfile, delimiter=',', quotechar='"')
		next(sentence)
		for row in sentence:
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
			training_set.append((row[0],row[1]))
			
	#	print training_set

	return training_set


def create_train(train_set):

	all_words = set()

	t = []
	words_tag = []
	for passage in train_set:			
		words_token = word_tokenize(passage[0].lower())		
		words_tag.append((['DIGIT' if word[1] == 'CD' else word[0] for word in pos_tag(words_token)],passage[1]))		
		for word in words_tag[-1][0]:							
			all_words.add(word)			

	for passage in words_tag:		
		t.append(({word: (word in passage[0]) for word in all_words}, passage[1]))
	##t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train_set]
	return t, all_words

def create_test(test_set, all_words ):
	
	t = []
	words_tag = []
	for passage in test_set:					
		words_token = word_tokenize(passage.lower())		
		
		words_tag.append(['DIGIT' if word[1] == 'CD' else word[0] for word in pos_tag(words_token)])			
		t = {word: (word in words_tag) for word in all_words}

		
	return t


train_set = load_training_set("./travelBot_chat.csv")
t, all_words = create_train(train_set)

#print t

classifier = nltk.NaiveBayesClassifier.train(t)

classifier.show_most_informative_features(20)

save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()


classifier_f = open("naivebayes.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

test_sentence = ["max 200 pounds"]
test = create_test(test_sentence, all_words)

#{word.lower(): (word in word_tokenize(test_sentence.lower())) for word in all_words}


print classifier.classify(test)

#print find_features(word_tokenize('I can spend up to 250'.lower()))

#print training