import csv

class travelBotdestinations():

	def load_destinations(self, file_destination):

		travelDestinations = {}

		# Create empty activities dictionary
		# f = csv.reader(open(file_destination, 'r'), delimiter=',', quotechar='"')
		# headers = f.next()
		# activities = {activity:0 for activity in headers[1:]}

		# Create dict of destination activities
		# with open(file_destination, 'r') as csvfile:
		# 	destinations = csv.reader(csvfile, delimiter=',', quotechar='"')
		# 	next(destinations)
		# 	for row in destinations:
		# 		for i, x in enumerate(activities.keys()):
		# 			activities[x] = row[i+1]
		# 		travelDestinations[row[0] + ', UK'] = activities
		 
		# Create dict of destination activities
		with open(file_destination, 'r') as csvfile:
			destinations = csv.reader(csvfile, delimiter=',', quotechar='"')
			next(destinations)
			for row in destinations:
				travelDestinations[row[0] + ', UK'] = {
					'Sights & Landmarks':row[1],
					'Museums':row[2],
					'Tours & Activities':row[3],
					'Nature & Parks':row[4],
					'Amusement Parks':row[5],
					'Nightlife':row[6],
					'Outdoor Activities':row[7],
					'Shopping':row[8],
					'Fun & Games':row[9],
					'Theatre & Concerts':row[10],
					'Boat Tours & Water Sports':row[11],
					'Food & Drink':row[12],
					'Spas & Wellness':row[13],
					'Casinos & Gambling':row[14],
					'Transportation':row[15],
					'Classes & Workshops':row[16],
					'Traveller Resources':row[17],
					'Zoos & Aquariums':row[18],
					'Events':row[19]}

		return travelDestinations


if __name__ == "__main__":
	a = travelBotdestinations()
	b = a.load_destinations("destinations.csv")
	print(b['Derby, UK'])
