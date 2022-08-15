# FlightTrackBot-Twitter


This bot will tweets information about flights based on their numbers. <br>
Use it by tagging it with [@TrackFlightBot](https://twitter.com/TrackFlightBot) and following it with a flight number like this: `/@FlightStatusBot AA127`

A reply will be sent to the user by the bot:
* Flight number and airline name 
* Name of the original airport 
* Departure time in UTC timezone 
* Name of the arrival airport 
* Estimated Time of Arrival in UTC timezone 
* The altitude of the plane, in feet 
* A map image of the plane's status

> > For the bot to function, the plane's transponder must be on, meaning the flight must be active.

## Setup

Create a Twitter App via [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard) and get the tokens need for [config.json](https://github.com/chilipolygon/FlightTrackBot-Twitter/blob/main/config.json)
<br>
Make sure that your Twitter App have permission to both `READ & WRITE` otherwise you will get a `403 forbidden error` 

Fill in your app's keys in [.env](https://github.com/chilipolygon/FlightTrackBot-Twitter/blob/master/.env)
```shell
API_KEY = 12345
API_KEY_SECRET = 12345
ACCESS_TOKEN = 12345
ACCESS_TOKEN_SECRET = 12345
BEARER_TOKEN = 12345
```

After that, install the requriments in [requirement.txt](https://github.com/chilipolygon/FlightTrackBot-Twitter/blob/main/requirements.txt)
```shell
python -m pip install -r requirements.txt
```

Finally, you're good to run the bot with `main.py`

## License
This project is licensed under MIT License. See [LICENSE](https://github.com/chilipolygon/FlightTrackBot-Twitter/blob/main/LICENSE) for more details.
