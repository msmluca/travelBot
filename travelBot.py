
from telegram import Updater, Bot, ReplyKeyboardMarkup, ForceReply, ReplyKeyboardHide
import travelBotdistance
import travelBotdestinations
import travelBotnltk
import time
import travelBotjourney
import travelBotrecommend

from random import randint, sample
import logging
import csv

class TravelBot:
	
	def __init__(self, auth_key):		
		self.chats = dict()
		self.users = dict()

		self.chat_user_actions = dict()

		self.bot = Updater(auth_key)
		self.manualbot = Bot(token=auth_key)
		
		# Initialize google distance class
		self.googleDist = travelBotdistance.travelBotdistance()
		self.googleDist.setUp()

		# Get the dispatcher to register handlers
		dp = self.bot.dispatcher

		# Register commands
		dp.addTelegramCommandHandler("start", self.start)
		#dp.addTelegramCommandHandler("search", self.search)
		dp.addTelegramCommandHandler("help", self.help)
		dp.addTelegramMessageHandler(self.echo)
		dp.addErrorHandler(self.error)

		dest = travelBotdestinations.travelBotdestinations()
		#self.travelDestinations = dest.load_destinations('./csv/destinations2.csv')
		self.botnltk = travelBotnltk.travelBotnltk()


	def message_event(self, bot, message):
		# Is it a new chat
		if (self.is_a_new_chat(message.chat.id)):
			logging.debug("new chat")
			self.chats[message.chat.id] = TravelChat(message)			
			result = bot.sendMessage(message.chat.id, text='Hallo ' + message.from_user.first_name)
		else:
			logging.debug("old chat")
			self.chats[message.chat.id].add_msg(message)

		# Is it a new user
		if (self.is_a_new_user(message.from_user.id)):
			logging.debug("new user")
			self.users[message.from_user.id] = TravelUser(message.from_user)			

		# Is it a msg with location
		# if (message.location is not None):
		# 	self.users[message.from_user.id].set_location(message.location.latitude, message.location.longitude)
		# 	result = bot.sendMessage(message.chat.id, text='I got the new position')

	def is_a_new_chat(self, chat_id):
		return not (chat_id in self.chats)


	def is_a_new_user(self, user_id):
		return not (user_id in self.users)


	def start(self, bot, update):
		self.message_event(bot,update.message)
		bot.sendMessage(update.message.chat_id, text='Hallo! I am Das Travel Bot.',reply_markup=ReplyKeyboardHide())
		time.sleep(1)
		bot.sendMessage(update.message.chat_id, text='Let\'s sort out your weekend travel plans!',reply_markup=ReplyKeyboardHide())
		time.sleep(1)

		self.search(bot,update)

	def help(self, bot, update):
		self.message_event(bot,update.message)
		bot.sendMessage(update.message.chat_id, text='Help me!')


	def reset(self, bot, update):
		chat.journey.start()


	def search(self, bot, update):
	#	self.message_event(bot,update.message)

		# do I've a location for this user?
		user = self.users[update.message.from_user.id]
		if not (isinstance(user.latitude, float) and isinstance(user.longitude,float)):
			bot.sendMessage(update.message.chat_id, text=user.first_name + ', where will you be travelling from? Send me your location!')
			self.chat_user_actions[(update.message.chat_id, update.message.from_user.id)] = [self.wait_location,None]
			return

		#Start the journey now!
		print("Search start")
		self.travelJourney(None, update.message.chat_id, update.message.from_user.id,None)
		#self.chat_user_actions[(update.message.chat_id, update.message.from_user.id)] = [self.travelJourney,None]


	def wait_location(self,question_key, chat_id, user_id, msg):
		if (msg.location is not None):
			self.users[user_id].set_location(msg.location.latitude, msg.location.longitude)
			result = self.manualbot.sendMessage(chat_id, text='Thanks, got it!')
			self.travelJourney(None, chat_id, user_id,None)
		else:
			result = self.manualbot.sendMessage(chat_id, text='Sorry I didn\'t get that...')
			

	def travelJourney(self, question_key, chat_id, user_id, msg):
		chat = self.chats[chat_id]

		print("Travel Journey call")

		# Check if I got an answer from a question
		if question_key != None:
			# extract from msg the answer
			print(msg.text)

			if chat.journey.has_options(question_key):
				ret, error_key = chat.journey.set_attribute(question_key, msg.text)
				if ret == -1:
					self.manualbot.sendMessage(chat_id, text=chat.journey.get_question(error_key))
					self.manualbot.sendMessage(chat_id, text=chat.journey.get_question(question_key))
					return
				chat.journey.complete_answer(question_key,1)
			else:
				ret, error_key = chat.journey.set_attribute(question_key, msg.text)
				if ret == -1:
					self.manualbot.sendMessage(chat_id, text=chat.journey.get_question(error_key))
					self.manualbot.sendMessage(chat_id, text=chat.journey.get_question(question_key))
					return
				chat.journey.complete_answer(question_key,1)
		

		next_key_journey = chat.journey.next_missing()
		if next_key_journey != None:
			# Next question
			if chat.journey.has_options(next_key_journey):
				print("question with keyboard")
				reply_markup = ReplyKeyboardMarkup(chat.journey.get_options(next_key_journey))
				print(reply_markup)
				self.manualbot.sendMessage(chat_id, text=chat.journey.get_question(next_key_journey), reply_markup = reply_markup)
				self.chat_user_actions[(chat_id, user_id)] = [self.travelJourney,next_key_journey]
			else:
				print("question WITHOUT keyboard")
				self.manualbot.sendMessage(chat_id, text=chat.journey.get_question(next_key_journey),reply_markup=ReplyKeyboardHide())
				self.chat_user_actions[(chat_id, user_id)] = [self.travelJourney,next_key_journey]
		else:
			#end of the journey
			if (chat_id, user_id) in self.chat_user_actions.keys():
				del self.chat_user_actions[(chat_id, user_id)]

			self.manualbot.sendMessage(chat_id, text="Danke! Let me see if I can find any good for you.",reply_markup=ReplyKeyboardHide())
			#need to reset user thing

			user = self.users[user_id]
			print chat.journey.get_attribute('ACTIVITIES')

			rec = travelBotrecommend.travelBotrecommend(str(user.latitude) + " " + str(user.longitude))
			res = rec.top_hotels(chat.journey.get_attribute('ACTIVITIES'), chat.journey.get_attribute('MAXTRAVELTIME'), chat.journey.get_attribute('MAXBUDGET'))
			print res

			if len(res.keys())> 0:
				i = 1
				bot_ans_keyboard = []
				#{'Price': '143.66', 'Star Rating': '5', 'Sat Temp': 10.29, 'Time': u'3 hours 40 mins', 'Sun Temp': 8.08, 'Position': 2, 'Review': '84.0'}
				for (place, hotel), details in res.items():
					bot_ans = "%d. In %s, %s from here, there is a nice hotel %s for only %s pound for two nights. The weather forecast is %s." % 	(
						i, place, details['Time'], hotel, details['Total Price'] ,details['Sat Weather'])
					self.manualbot.sendMessage(chat_id, text=bot_ans,reply_markup=ReplyKeyboardHide())
					bot_ans_keyboard.append([str(i)])
					chat.journey.add_results(i, (place, hotel), details, rec.getCoordinates(hotel,place))
					print rec.getCoordinates(hotel,place)
					i += 1

				reply_markup = ReplyKeyboardMarkup(bot_ans_keyboard)
				print(reply_markup)
				self.manualbot.sendMessage(chat_id, text="Any preference?", reply_markup = reply_markup)

				self.chat_user_actions[(chat_id, user_id)] = [self.selectSolution,None]
			else:
				self.manualbot.sendMessage(chat_id, text="Sorry I couldn't find anything for you. Try again.",reply_markup=ReplyKeyboardHide())
				
				if (chat_id, user_id) in self.chat_user_actions.keys():
					del self.chat_user_actions[(chat_id, user_id)]
				chat.journey.start()


	def selectSolution(self, question_key, chat_id, user_id, msg):	
		chat = self.chats[chat_id]
		
		if msg.text.isdigit():
			location = chat.journey.get_results(int(msg.text))
			lat = location['location'][0]
			lon = location['location'][1]

		self.manualbot.sendMessage(chat_id, text="The option " + str(msg.text) + " it\'s my favourite too",reply_markup=ReplyKeyboardHide())
		self.manualbot.sendMessage(chat_id, text="Do you know how to get there?",reply_markup=ReplyKeyboardHide())

		self.manualbot.sendLocation(chat_id, latitude=float(lat), longitude=float(lon))

		if (chat_id, user_id) in self.chat_user_actions.keys():
					del self.chat_user_actions[(chat_id, user_id)]


		chat.journey.start()
		print("we got everything")

	def echo(self, bot, update):
		if not (self.is_a_new_chat(update.message.chat.id)):
			if not (self.chats[update.message.chat.id].active):
				return

		self.message_event(bot,update.message)

		#msg_meaning = self.botnltk.classify(update.message.text)
		#bot.sendMessage(update.message.chat_id, text=msg_meaning)

		
		# Check if the msg is a reply to a previous command
		if (update.message.chat_id, update.message.from_user.id) in self.chat_user_actions:
			_call_method, question_key = self.chat_user_actions[(update.message.chat_id, update.message.from_user.id)]
			ret = _call_method( 
				question_key = question_key,
				chat_id = update.message.chat_id, 
				user_id = update.message.from_user.id, 
				msg = update.message)
			
#			bot.sendLocation(update.message.chat_id, latitude=float(ret['lat']), longitude=float(ret['lng']))

#			bot.sendMessage(update.message.chat_id, text='Got it!', reply_markup=ReplyKeyboardHide())				
#			del self.chat_user_actions[(update.message.chat_id, update.message.from_user.id)]


	def error(bot, update, error, error2):
		loggin.warn('Update "%s" caused error "%s"' % (update, error))
		raise ValueError('Parameter should...')



class TravelChat:
	
	def __init__(self, message):
		self.chat_id = message.chat.id
		self.messages = []		
		self.last_message_id = 0;	
		self.active = True;
		self.message_count = 0;
		self.users = []
		self.journey = travelBotjourney.travelBotjourney()

		self.add_msg(message)


	def add_msg(self, message):
		self.last_message_datetime = message['date']
		self.last_message_id = message['message_id']
		self.message_count += 1
		self.messages.append(message)

		if not message.from_user.id in self.users:
			self.users.append(message.from_user.id)

		if message.new_chat_participant <> None:
			if not message.new_chat_participant.id in self.users:
				self.users.append(message.new_chat_participant.id)

		if message.left_chat_participant <> None:
			if message.left_chat_participant.id in self.users:
				self.users.remove(message.left_chat_participant.id)


	def purge(self, older_than_unixtime):
		self.messages = [msg for msg in self.messages if msg.date <= older_than_unixtime]


	def disable(self):
		self.active = False


	def activate(self):
		self.active = True


class TravelUser:
	def __init__(self, user):
		self.id = user.id
		self.first_name = user.first_name
		self.last_name = user.last_name
		self.username = user.username
		self.enabled = False
		self.latitude = None
		self.longitude = None

	def set_location(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude




trbot = TravelBot('182627058:AAE-km8osu8MKE8n6Y3vOSJ89Kn6oLrlih8')

# Start the Bot
trbot.bot.start_polling()

	# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.


# App = TestApp(debot)
# App.run()

trbot.bot.idle()
