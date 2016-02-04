import csv

class travelBotdestinations():

	def load_destinations(self, file_destination):

		travelDestinations = {}

		# Create empty activities dictionary
		f = csv.reader(open(file_destination, 'r'), delimiter=',', quotechar='"')
		headers = f.next()
		activities = {activity:0 for activity in headers[1:]}

		# Create dict of destination activities
		with open(file_destination, 'r') as csvfile:
			destinations = csv.reader(csvfile, delimiter=',', quotechar='"')
			next(destinations)
			for row in destinations:
				for i, x in enumerate(activities.keys()):
					activities[x] = row[i+1]
				travelDestinations[row[0] + ', UK'] = activities
		 
		return travelDestinations


if __name__ == "__main__":
	a = travelBotdestinations()
	print(a.load_destinations("destinations_test.csv"))
