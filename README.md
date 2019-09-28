# yeahlow-backend

[![Build Status](https://travis-ci.org/yeahlow-ch/yeahlow-backend.svg?branch=master)](https://travis-ci.org/yeahlow-ch/yeahlow-backend)

## How to run

Install all the necessary requirements via pip and then execute:

```
python app/index.py
```

The app is available http://localhost:3000 and provides some default data.
Refer to the API documention on how to delete the default data.

## API

### GET /api/votes

Returns an aggregated list of all votes as hotspots.

Example return value:

```
[
    {
        "hotness": 87.33333333333333,
        "hotness_color": "#700000",
        "latitude": 47.39,
        "longitude": 8.516,
        "place": "Foundation Technopark Zurich"
    },
    {
        "hotness": 41,
        "hotness_color": "#ff6600",
        "latitude": 47.387,
        "longitude": 8.574,
        "place": "Zoo Zürich"
    }
]
```

### POST /api/votes

Adds a vote to the specified location.

Example POST message body:

```
{
    "latitude": 47.39,
    "longitude": 8.516,
    "vote" : 1
}
```

### GET /api/events

Returns a list of all events.

Example return value:
```
[
    {
        "description": "Save the penguins!",
        "end_time": "Sat, 28 Sep 2019 17:30:00 GMT",
        "id": 5,
        "latitude": 47.386245,
        "longitude": 8.574252,
        "name": "Penguin Parade",
        "start_time": "Sat, 28 Sep 2019 15:30:00 GMT",
        "type": "animal"
    },
    {
        "description": "Beer, sausages and other stuff",
        "end_time": "Sat, 28 Sep 2019 17:30:00 GMT",
        "id": 6,
        "latitude": 47.38531,
        "longitude": 8.519118,
        "name": "Rüdig guet",
        "start_time": "Sat, 28 Sep 2019 15:30:00 GMT",
        "type": "party"
    }
]
```

### GET /api/events/surprise?longitude={}&latitude={}&range={}

Returns a random event that is approximately as far a way as specified
by the range parameter from the coordinates defined through the longitude
and latitude parameters. If no event is within range, the next closest event 
is returned that is less far away than range.

Example return value:

```
{
    "description": "Beer, sausages and other stuff",
    "end_time": "Sat, 28 Sep 2019 17:30:00 GMT",
    "id": 6,
    "latitude": 47.38531,
    "longitude": 8.519118,
    "name": "Rüdig guet",
    "start_time": "Sat, 28 Sep 2019 15:30:00 GMT",
    "type": "party"
}
```

### DELETE /api/db/votes

Delets all votes in the database. No parameters required.

### POST /api/db/votes

Adds generated votes into the database. No parameters required.

### DELETE /api/db/events

Deletes all events in the database. No parameters required.

### POST /api/db/events

Adds events into the database. No parameters required.