
from telegram import Updater, Bot, ReplyKeyboardMarkup, ForceReply, ReplyKeyboardHide
import travelBotdistance
import travelBotdestinations
import travelBotnltk
import travelBotjourney

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
		dp.addTelegramCommandHandler("search", self.search)
		dp.addTelegramCommandHandler("help", self.help)
		dp.addTelegramMessageHandler(self.echo)
		dp.addErrorHandler(self.error)

		dest = travelBotdestinations.travelBotdestinations()
		self.travelDestinations = dest.load_destinations('destinations_test.csv')
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
		if (message.location is not None):
			self.users[message.from_user.id].set_location(message.location.latitude, message.location.longitude)
			result = bot.sendMessage(message.chat.id, text='I got the new position')

	def is_a_new_chat(self, chat_id):
		return not (chat_id in self.chats)


	def is_a_new_user(self, user_id):
		return not (user_id in self.users)


	def start(self, bot, update):
		self.message_event(bot,update.message)
		bot.sendMessage(update.message.chat_id, text='Hallo! I\'m Das travel Bot.')


	def help(self, bot, update):
		self.message_event(bot,update.message)
		bot.sendMessage(update.message.chat_id, text='Help me!')

	def search(self, bot, update):
		self.message_event(bot,update.message)

		# do I've a location for this user?
		user = self.users[update.message.from_user.id]
		if not (isinstance(user.latitude, float) and isinstance(user.longitude,float)):
			bot.sendMessage(update.message.chat_id, text=user.first_name + ' send me your location.')
			return

		#bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
		print("Looking for a place...")
		places = self.googleDist.timeDist(str(user.latitude) + " " + str(user.longitude), self.travelDestinations)
		print(places)
		bot_answer = places['destination_addresses']

		i=0

		for key, value in places.iteritems():
			if key == 'rows':
				for row_key, row_value in value[0].iteritems():
					for result in row_value:
						bot_answer[i] = bot_answer[i] + " " + result['duration']['text']
						i += 1
			
		
		#reply_markup = ReplyKeyboardMarkup([bot_answer])
		for answer in bot_answer:
			bot.sendMessage(update.message.chat_id, text=answer)
		
		#self.chat_user_actions[(update.message.chat_id, update.message.from_user.id)] = self.whereeat.select_place

	def echo(self, bot, update):
		if not (self.is_a_new_chat(update.message.chat.id)):
			if not (self.chats[update.message.chat.id].active):
				return

		self.message_event(bot,update.message)

		msg_meaning = self.botnltk.classify(update.message.text)
		bot.sendMessage(update.message.chat_id, text=msg_meaning)

		logging.debug(update.message)
		
		# Check if the msg is a reply to a previous command
		if (update.message.chat_id, update.message.from_user.id) in self.chat_user_actions:
			_call_method = self.chat_user_actions[(update.message.chat_id, update.message.from_user.id)]
			ret = _call_method( chat_id = update.message.chat_id, user_id = update.message.from_user.id, is_admin = self.is_security_cleared(update.message.from_user.id), msg = update.message.text)
			
			bot.sendLocation(update.message.chat_id, latitude=float(ret['lat']), longitude=float(ret['lng']))

			bot.sendMessage(update.message.chat_id, text='Got it!', reply_markup=ReplyKeyboardHide())				
			del self.chat_user_actions[(update.message.chat_id, update.message.from_user.id)]


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
