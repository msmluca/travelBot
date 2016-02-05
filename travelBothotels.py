import csv

class travelBothotels():

	def load_hotels(self, file_hotels):

		destinationHotels = {}

		# Create dict of destination hotels
		with open(file_hotels, 'r') as csvfile:
			hotels = csv.reader(csvfile, delimiter=',', quotechar='"')
			next(hotels)
			for row in hotels:
				destinationHotels[(row[0],row[1])] = {'Price':row[2],
											'Star Rating':row[3],
											'Review':row[4]}

		return destinationHotels


if __name__ == "__main__":
	a = travelBothotels()
	# print(a.load_hotels("./csv/hotel_info.csv", 'Manchester'))
	print(a.load_hotels("./csv/hotel_info.csv"))
