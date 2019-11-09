
from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from flask import request

class Suggestion(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('data',
        type=str,
        required=True,
        help="This field is required"
    )
    
    times = {
        "LESS_THAN_30_MINUTES" : 30,
        "BETWEEN_30_AND_60_MINUTES" : 60,
        "BETWEEN_60_AND_120_MINUTES" : 120,
        "OVER_120_MINUTES_OR_CANCELLED" : 10000
    }

    def post(self):
        prescriptions = []
        result = {"prescription" : prescriptions}
        data = request.get_json()['data']
        pres = data['prescription']
        flight = data['flight_detail']
        delay = data['delay_prediction']['data']
        start = flight['departureDate'] + " "+flight['departureTime']
        end = flight['arrivalDate'] + " " + flight['arrivalTime']
        time, pro = self.findMaxProb(delay)
        start = self.giveDateFormat(start)
        end = self.giveDateFormat(end)
        if float(pro) > 0.10:
            end = self.addTime(end, self.times[time])
        return self.analysePrescriptions(start, end, flight['departureDate'], pres), 200



    def addTime(self, start, minutes):
        return start+timedelta(minutes = minutes)

    def analysePrescriptions(self ,start, end, startDate, prescriptions):
        result = []
        for each in prescriptions:
            doses = each['doses']
            for t in doses:
                tt = self.giveDateFormat(startDate+" "+t)
                print("dose - {}".format(tt))
                print('start -{}'.format(start))
                print("end - {}".format(end))
                if tt < end:
                    if tt> start:
                        result.append(each)
                        break 
                    else:
                        if end.day > start.day:
                            result.append(each)
                            break
                        continue       
                else:
                    continue
        return result



    def giveDateFormat(self, t):
        return datetime.strptime(t, "%Y-%m-%d %H:%M:%S")

    def findTimeDifference(self, start, end):
        t1 = datetime.strptime(start, "%Y-%d-%m %H:%M:%S")
        t2 = datetime.strptime(end, "%Y-%d-%m %H:%M:%S")
        t3 = t2-t1
        day = t3.days
        hours = t3.seconds//3600
        mins = (t3.seconds//60)%60
        totalMins = day*24*60 + hours*60 + min
        return totalMins

    def findHourDiff(self, start, end):
        t1 = datetime.strptime(start, "%H:%M:%S")
        t2 = datetime.strptime(end, "%H:%M:%S")
        d3=  t2-t1

    def findMaxProb(self, delay):
        maxPro = 0.0
        time = ""
        for pred in delay:
            print(pred['probability'])
            if float(maxPro) < float(pred['probability']):
                maxPro = pred['probability']
                time = pred['result']
        return [time, maxPro]




