import csv

class travelBotdestinations():

	def load_destinations(self, file_destination):

		travelDestinations = list()

		with open(file_destination, 'r') as csvfile:
			destinations = csv.reader(csvfile, delimiter=',', quotechar='"')
			next(destinations)
			for row in destinations:
				travelDestinations.append(row[0]+" , UK")
		 
		return travelDestinations



if __name__ == "__main__":
	a = travelBotdestinations()
	print(a.load_destinations("destinations.csv"))
