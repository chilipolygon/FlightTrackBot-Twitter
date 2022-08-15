import json
import re
import time
import tweepy
from datetime import datetime, timezone
from FlightRadar24.api import FlightRadar24API
import sys
import os
import config
os.system('cls' if os.name == 'nt' else 'clear')

class FlightTrackerBot():
    def __init__(self, ) -> None:
        self.auth()
        self.handleTweet()

    def log(self, message, error=None):
        if (error):
            print("[{}] {}".format(self.__class__.__name__, error))
        print("[{}] {}".format(self.__class__.__name__, message))
        sys.stdout.flush()

    def auth(self):
        self.client = tweepy.Client(
            bearer_token=config.BEARER_TOKEN,
            consumer_key=config.API_KEY,
            consumer_secret=config.API_KEY_SECRET,
            access_token=config.ACCESS_TOKEN,
            access_token_secret=config.ACCESS_TOKEN_SECRET,
        )
        self.client_id = int(self.client.get_me().data.id)
        self.mention_id = 1
        init = self.client.get_users_mentions(self.client_id)
        if init.data:
            self.mention_id = init.data[0].id

    def searchFlight(self, id):
        try:
            iata = id[:2]
            icao = id[:3]
            
            flightAPI = FlightRadar24API()
            airlines = flightAPI.get_airlines()
            for airline in airlines:
                if airline["Code"] == iata or airline["ICAO"] == icao:
                    iata = airline["Code"]
                    icao = airline["ICAO"] 

            flightStatus = flightAPI.get_flights(airline=icao)
            flightNumber = str(re.findall(r'\d+', id)).strip("[']")

            for flight in flightStatus:
                if f"{iata}{flightNumber}" == flight.number or f"{icao}{flightNumber}" == flight.number:
                    flight.set_flight_details(flightAPI.get_flight_details(flight.id))
                    self.flightData = {
                        "name": flight.airline_short_name,
                        "number": flight.number,
                        "depTime": f"{self.getTime(flight.time_details['real']['departure'])}",
                        "dep": flight.origin_airport_name,
                        "eta": f"{self.getTime(flight.time_details['other']['eta'])}",
                        "alt": f"{flight.altitude} Feet" if flight.altitude > 0 else "Landed",
                        "des": flight.destination_airport_name,
                    }

                    self.icaoURL = f"{icao}{flightNumber}" #will be used for linking flightaware
                    return self.flightData

        except Exception as e:
            self.log(e)


    def replyDraft(self, data):
        if not data:
            return "There was no flight number found or the flight is not active at the moment."
        
        content = f"""{data['name']} {data['number']}:
Departure: {data['dep']}
Departure time: {data['depTime']}
Destination: {data['des']}
Arrival time: {data['eta']}
Current Altitude: {data['alt']}
https://flightaware.com/live/flight/{self.icaoURL}"""

        return content
        
    def processTweet(self, tweet):
        try:
            if tweet.in_reply_to_user_id is None and len(tweet.text.split(" ")) > 1:
                flight_number = tweet.text.split(" ")[1]
                flightConfig = self.searchFlight(flight_number)
                replyContent = self.replyDraft(flightConfig)
                self.publishReply(tweet.id, replyContent)
                self.client_id = tweet.id
            else:
                self.mention_id = tweet.id
        except Exception as e:
            self.log(e)

    def publishReply(self, id, reply):
        try:
            self.client.create_tweet(in_reply_to_tweet_id=id, text=reply)
        except tweepy.errors.TweepyException as error:
            self.log(error)

    def getTime(self, id=0):
        if id & id!=0:
            time = (datetime.fromtimestamp(id, timezone.utc)).strftime("%d-%m-%Y %H:%M UTC")
            return time
        return "Could Not Find"
        
    def handleTweet(self):
        while True:
            try:
                mentions = self.client.get_users_mentions(self.client_id, since_id=self.mention_id, expansions=["in_reply_to_user_id"])
                if mentions.data:
                    for tweet in mentions.data:
                        self.log(tweet)
                        self.processTweet(tweet)
                self.log(f'Monitoring.. {datetime.now().strftime("%H:%M:%S")}')
                time.sleep(5)
            except KeyboardInterrupt:
                sys.exit()

if __name__ == "__main__":
    FlightTrackerBot()