from flask_restful import Resource, reqparse
from datetime import datetime



class Suggestion(Resource):
		
	parser = reqparse.RequestParser()
	parser.add_argument("data", type=str, required=True, help="This field is required")

	@classmethod()
	def post():
		data = parser.parse_args()
		prescription = data['prescription']
		flight = data['fligh']
		delay = data['delay_prediction']
		pass


	
	def findTimeDifference(start, end):
        t1 = datetime.strptime(start, "%Y-%d-%m %H:%M:%S")
        t2 = datetime.strptime(end, "%Y-%d-%m %H:%M:%S")
		t3 = (t2 - t1)


	def findMaxProbability(delay):
		maxProbability = 0
		time = ""
		for pred in delay:
			if maxProbability < pred['probability']:
				maxProbability = pred['probability']
				time = pred['result']
		return [time, maxProbability]
