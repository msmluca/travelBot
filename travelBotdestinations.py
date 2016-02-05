import csv

class travelBotdestinations():

	def load_destinations(self, file_destination):

		travelDestinations = {}
		 
		# Create dict of destination activities
		with open(file_destination, 'r') as csvfile:
			destinations = csv.reader(csvfile, delimiter=',', quotechar='"')
			next(destinations)
			for row in destinations:
				travelDestinations[row[0]] = {
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
					'Events':row[19],
					'Sights & Landmarks Rank':row[20],
					'Museums Rank':row[21],
					'Tours & Activities Rank':row[22],
					'Nature & Parks Rank':row[23],
					'Amusement Parks Rank':row[24],
					'Nightlife Rank':row[25],
					'Outdoor Activities Rank':row[26],
					'Shopping Rank':row[27],
					'Fun & Games Rank':row[28],
					'Theatre & Concerts Rank':row[29],
					'Boat Tours & Water Sports Rank':row[30],
					'Food & Drink Rank':row[31],
					'Spas & Wellness Rank':row[32],
					'Casinos & Gambling Rank':row[33],
					'Transportation Rank':row[34],
					'Classes & Workshops Rank':row[35],
					'Traveller Resources Rank':row[36],
					'Zoos & Aquariums Rank':row[37],
					'Events Rank':row[38]}

		return travelDestinations


if __name__ == "__main__":
	a = travelBotdestinations()
	b = a.load_destinations("./csv/DestinationActivityFreqRank.csv")
	print(b['Derby'])
