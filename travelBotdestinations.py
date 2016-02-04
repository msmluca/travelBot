import csv

class travelBotdestinations():

	def load_destinations(self, file_destination):

		# travelDestinations = list()

		# with open(file_destination, 'r') as csvfile:
		# 	destinations = csv.reader(csvfile, delimiter=',', quotechar='"')
		# 	next(destinations)
		# 	for row in destinations:
		# 		travelDestinations.append(row[0]+" , UK")
		 
		# return travelDestinations

		return {
			'York':{'SightsLandmarks':1,
					'NatureParks':2,
					'Museums':3,
					'FunGames':4,
					'Nightlife':5,
					'TheatreConcerts':6,
					'Shopping':7,
					'FoodDrink':8,
					'Outdoor':9,
					'SpasWellness':10,
					'Tours':11,
					'BoatWater':12,
					'ClassWorkshops':13,
					'CasinosGambling':14,
					'Traveller':15},
			'Newcastle':{'SightsLandmarks':10,
					'NatureParks':11,
					'Museums':12,
					'FunGames':13,
					'Nightlife':14,
					'TheatreConcerts':15,
					'Shopping':16,
					'FoodDrink':17,
					'Outdoor':18,
					'SpasWellness':19,
					'Tours':20,
					'BoatWater':21,
					'ClassWorkshops':22,
					'CasinosGambling':23,
					'Traveller':24},
			'Leeds':{'SightsLandmarks':15,
					'NatureParks':14,
					'Museums':13,
					'FunGames':12,
					'Nightlife':11,
					'TheatreConcerts':10,
					'Shopping':9,
					'FoodDrink':8,
					'Outdoor':7,
					'SpasWellness':6,
					'Tours':5,
					'BoatWater':4,
					'ClassWorkshops':3,
					'CasinosGambling':2,
					'Traveller':1}
		}


if __name__ == "__main__":
	a = travelBotdestinations()
	print(a.load_destinations("destinations_test.csv"))
