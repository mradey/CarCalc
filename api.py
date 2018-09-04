from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

from uber_rides.session import Session as UberSession
from uber_rides.client import UberRidesClient

from geopy.geocoders import Nominatim

from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
from lyft_rides.client import LyftRidesClient

import requests
import json

geolocator = Nominatim(user_agent="uberVcar")

#UBER CREDENTIALS
session = UberSession(server_token='hWrizMQl5BAsAs_Xxsb0D49J6_IDkpsvad4ShfYX')
uber_client = UberRidesClient(session)

        
#LYFT CREDENTIALS
auth_flow = ClientCredentialGrant(
    '2E3iq4LPcDDL',
    'Q5IsU-VbuZeNsBQvmwOm9dMnjpTO9MZh',
    'public',
)
session = auth_flow.get_session()
lyft_client = LyftRidesClient(session)

# api-endpoint
URL = "https://dev.tollguru.com/beta00/calc/gmaps"
 

headers = {"x-api-key": "k98AnfwbGz7LGKSMR7dIq8Z9xhg2oxnU8w5KJ7Kj" }

app = Flask(__name__)
api = Api(app)

states_names = {
    'AL':	'Alabama',
    'AK':	'Alaska',
    'AZ':	'Arizona',
    'AR':	'Arkansas',
    'CA':	'California',
    'CO':	'Colorado',
    'CT':	'Connecticut',
    'DE':	'Delaware',
    'FL':	'Florida',
    'GA':	'Georgia',
    'HI':	'Hawaii',
    'ID':	'Idaho',
    'IL':	'Illinois',
    'IN':	'Indiana',
    'IA':	'Iowa',
    'KS':	'Kansas',
    'KY':	'Kentucky',
    'LA':	'Louisiana',
    'ME':	'Maine',
    'MD':	'Maryland',
    'MA':	'Massachusetts',
    'MI':	'Michigan',
    'MN':	'Minnesota',
    'MS':	'Mississippi',
    'MO':	'Missouri',
    'MT':	'Montana',
    'NE':	'Nebraska',
    'NV':	'Nevada',
    'NH':	'New Hampshire',
    'NJ':	'New Jersey',
    'NM':	'New Mexico',
    'NY':	'New York',
    'NC':	'North Carolina',
    'ND':	'North Dakota',
    'OH':	'Ohio',
    'OK':	'Oklahoma',
    'OR':	'Oregon',
    'PA':	'Pennsylvania',
    'RI':	'Rhode Island',
    'SC':	'South Carolina',
    'SD':	'South Dakota',
    'TN':	'Tennessee',
    'TX':	'Texas',
    'UT':	'Utah',
    'VT':	'Vermont',
    'VA':	'Virginia',
    'WA':	'Washington',
    'WV':	'West Virginia',
    'WI':	'Wisconsin',
    'WY':	'Wyoming'
}
states_insurace = {
    'Alaska':318,
    'Alabama':419,
    'Arkansas': 397,
    'Arizona':496,
    'California':491,
    'Colorado':506,
    'Connecticut':761,
    'DC':745,
    'Delaware':805,
    'Florida':884	,
    'Georgia':532	,
    'Hawaii':555	,
    'Iowa':294	,
    'Idaho':319	,
    'Illinois':383,
    'Indiana':400	,
    'Kansas':397	,
    'Kentucky':	745,
    'Louisiana':	705,	
    'Massachusetts':	539,	
    'Maryland':	710	,
    'Maine'	:359	,
    'Michigan':2012	,
    'Minnesota'	:579,	
    'Missouri'	:409,	
    'Mississippi'	:398,	
    'Montana'	:323	,
    'North Carolina'	:347	,
    'North Dakota'	:363	,
    'Nebraska'	:329	,
    'New Hampshire'	:485,
    'New Jersey'	:677,	
    'New Mexico'	:424,	
    'Nevada'	:623	,
    'New York'	:812	,
    'Ohio'	:383,
    'Oklahoma'	:444,	
    'Oregon'	:690,	
    'Pennsylvania'	:480,	
    'Rhode Island'	:751,	
    'South Carolina'	:484,	
    'South Dakota'	:267	,
    'Tennessee'	:404	,
    'Texas'	:465	,
    'Utah'	:531	,
    'Virginia'	:372,	
    'Vermont'	:337,	
    'Washington'	:466,	
    'Wisconsin'	:373	,
    'West Virginia'	:493,	
    'Wyoming'	:339	
}

states_registration = {
    'Alaska':21.25,
    'Alabama':68,
    'Arkansas': 8,
    'Arizona':17,
    'California':28,
    'Colorado':19,
    'Connecticut':70,
    'DC':55,
    'Delaware':20,
    'Florida':27.10	,
    'Georgia':20	,
    'Hawaii':47.95	,
    'Iowa':	14,
    'Idaho':25.25,
    'Illinois':48,
    'Indiana':12.75	,
    'Kansas':27.25	,
    'Kentucky':	14.5,
    'Louisiana':	10,	
    'Massachusetts':30,	
    'Maryland':	35	,
    'Maine'	:23	,
    'Michigan':29,
    'Minnesota'	:99,	
    'Missouri'	:21,	
    'Mississippi'	:23.75,	
    'Montana'	:10.25	,
    'North Carolina'	:20	,
    'North Dakota'	:36	,
    'Nebraska'	:17.5	,
    'New Hampshire'	:19.2,
    'New Jersey'	:25,	
    'New Mexico'	:23,	
    'Nevada'	:33	,
    'New York'	:17.25	,
    'Ohio'	:22.25,
    'Oklahoma'	:20,	
    'Oregon'	:30,	
    'Pennsylvania'	:24,	
    'Rhode Island'	:30,	
    'South Carolina'	:24,	
    'South Dakota'	:21	,
    'Tennessee'	:23	,
    'Texas'	:40.8	,
    'Utah'	:21	,
    'Virginia'	:42,	
    'Vermont'	:26.5,	
    'Washington'	:33,	
    'Wisconsin'	:45	,
    'West Virginia'	:30,	
    'Wyoming'	:15	
}

state_gas= { 
    'Alabama':2.554,	
    'Alaska'	:3.347,	
    'Arizona'	:2.882,	
    'Arkansas'	:2.584,
    'California':3.597,	
    'Colorado'	:2.809,	
    'Connecticut'	:3.054,	
    'Delaware'	:2.760,
    'District of Columbia':3.007,
    'Florida':	2.783	,
    'Georgia':	2.737	,
    'Hawaii':3.772	,
    'Idaho':3.230	,
    'Illinois':2.905,
    'Indiana':2.891	,
    'Iowa':2.711	,
    'Kansas':2.658	,
    'Kentucky':2.744,	
    'Louisiana':2.618,	
    'Maine':2.855	,
    'Maryland':2.802,
    'Massachusetts':2.891,
    'Michigan':2.928,
    'Minnesota':2.772,
    'Mississippi':2.562,
    'Missouri':2.593,
    'Montana':2.939,
    'Nebraska':2.744,
    'Nevada':3.188,
    'New Hampshire':2.802	,
    'New Jersey':2.882	,
    'New Mexico':2.781	,
    'New York':3.002	,
    'North Carolina':2.684,
    'North Dakota':2.837	,
    'Ohio':2.785	,
    'Oklahoma':2.614,
    'Oregon':3.257,
    'Pennsylvania':3.052,
    'Rhode Island':2.896,
    'South Carolina':2.550,
    'South Dakota':2.865	,
    'Tennessee':2.616,
    'Texas'	:2.608	,
    'Utah'	:3.173	,
    'Vermont'	:2.914	,
    'Virginia'	:2.607,
    'Washington'	:3.381,
    'West Virginia'	:2.853,
    'Wisconsin'	:2.801,
    'Wyoming'	:2.960
}


class Cars(Resource):
    
    def get(self, start_end):
        endIndex1 = start_end.index('+',7)
        endIndex2 = start_end.index('+',endIndex1+1)
        endIndex3 = start_end.index('+',endIndex2+1)
        endIndex4 = start_end.index('+',endIndex3+1)
        endIndex5 = start_end.index('+',endIndex4+1)
        endIndex6 = start_end.index('+',endIndex5+1)


        start_address = start_end[6:endIndex1]
        end_address = start_end[start_end.index('=', endIndex1)+1:endIndex2]
        num_people = int(start_end[start_end.index('=', endIndex2)+1:endIndex3])
        parking_cost = int(start_end[start_end.index('=', endIndex3)+1:endIndex4])
        mpg_city = int(start_end[start_end.index('=', endIndex4)+1:endIndex5])
        mpg_hwy = int(start_end[start_end.index('=', endIndex5)+1:endIndex6])
        STATE_NAME = states_names[start_end[start_end.index('=', endIndex6)+1:]]
                
        location1 = geolocator.geocode(start_address)
        location2 = geolocator.geocode(end_address)

        # UBER
        response = uber_client.get_price_estimates(
            start_latitude = location1.latitude,
            start_longitude = location1.longitude,
            end_latitude = location2.latitude,
            end_longitude = location2.longitude,
            seat_count = num_people
        )

        estimateUber = response.json.get('prices')
        
        # LYFT
        response = lyft_client.get_ride_types(location1.latitude, location1.longitude)
        estimateLyft = response.json.get('ride_types')


 
        # defining a params dict for the parameters to be sent to the API
        payload = { 
        "from": {
            "address": start_address
        }, 
        "to": {
            "address": end_address
        },
        "vehicleType": "2AxlesAuto",
        "fuelPrice": state_gas[STATE_NAME],
        "fuelPriceCurrency": "USD",
        "fuelEfficiency": {
            "city": mpg_city,
            "hwy": mpg_hwy,
            "units": "mpg"
            }
        }
 
        # sending get request and saving the response as response object
        r = requests.post(URL, data=json.dumps(payload), headers=headers)
        resp = r.json()

        distanceString = resp["routes"][0]["summary"]["distance"]["text"]
        daily_commute_distance = 2*float(distanceString[:distanceString.index(' ')])
        monthlyMaintenance = 99

        estimateCar = (parking_cost + states_insurace[STATE_NAME] + states_registration[STATE_NAME])/12 + (state_gas[STATE_NAME]*daily_commute_distance/mpg_hwy)*20 + monthlyMaintenance
        lyft = {}
        for item in estimateLyft:
            lyft[item['display_name']] = (item['pricing_details']['base_charge']/100 + daily_commute_distance * item['pricing_details']['cost_per_mile']/100) * 20

        uber = {}
        for item in estimateUber:
            uber[item['localized_display_name']] = (item['high_estimate']+item['low_estimate'])*10
        bigDict = {}
        bigDict['lyft'] = lyft
        bigDict['uber'] = uber
        bigDict['personalCar'] = estimateCar
        return bigDict



api.add_resource(Cars, '/cars/<string:start_end>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')


