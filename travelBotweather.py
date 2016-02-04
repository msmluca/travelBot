
from datetime import datetime
import time
import random



class travelBotWeather():

	def timeDist(self, end_locations):

		results = {}


		for x in end_locations:
			results[x] = [random.randrange(15,25)]
		
		return results


if __name__ == "__main__":
    a = travelBotWeather()
    print(a.timeDist(["abc","london","brighton"]))