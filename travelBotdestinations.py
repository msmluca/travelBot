import csv
import pandas as pd

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
					'Events':row[19]}

		return travelDestinations


if __name__ == "__main__":
	a = travelBotdestinations()
	b = a.load_destinations("./csv/destinations2.csv")
	print(b['Derby'])
