api_key = "e175a962d1b467e879961811c7ff0e82"

def get_user(client, user_id):
  data = client.fm.find_one({"_id": user_id})
  if not data:
    return None
  return data['username']

async def set_user(client, user_id, username):
  params  = {
      "method": 'user.getInfo', 
      "user": username,
      "api_key": api_key, 
      "format": 'json'
  }
  async with client.session.get("http://ws.audioscrobbler.com/2.0/", params=params) as body:
      res = await body.json()
  if "user" not in res:
    return None
  if not client.fm.find_one({"_id": user_id}):
    client.fm.insert_one({"_id": user_id, "username": username})
  else:
    client.fm.update_one({"_id": user_id}, {"$set": {"username": username}})
  return res['user']['url']

async def get_recent_track_data(client, username):
  params  = {
      "method": 'user.getrecenttracks',
      "user": username,
      "api_key": api_key,
      "limit": 2,
      "format": 'json'
  }
  async with client.session.get("http://ws.audioscrobbler.com/2.0/", params=params) as body:
      body = await body.json()
  try:
      track_1 = body['recenttracks']['track'][0]
  except:
      return None, None, None, None, None, None, None
  if '@attr' in track_1:
      return body['recenttracks']['@attr']['total'], track_1['artist']['#text'], track_1['name'], track_1['album']['#text'], track_1['url'], track_1['image'][-1]['#text'], track_1['@attr']['nowplaying']
  return body['recenttracks']['@attr']['total'], track_1['artist']['#text'], track_1['name'], track_1['album']['#text'], track_1['url'], track_1['image'][-1]['#text'], track_1['date']['uts']

async def get_scrobbles(client, username, artist, song):
  params  = {
      "method": 'track.getInfo',
      "artist": artist,
      "track": song,
      "user": username,
      "autocorrect": 1, 
      "api_key": api_key,
      "format": 'json'
  }
  async with client.session.get("http://ws.audioscrobbler.com/2.0/", params=params) as body:
      body = await body.json()
  try:
      body["track"]['userplaycount']
  except:
      return "?"
  return body["track"]['userplaycount']

async def get_artist_real_name(client, artist):
  params  = {
      "method": 'artist.getInfo',
      "artist": artist,
      "autocorrect": 1,
      "api_key": api_key,
      "format": 'json'
  }
  async with client.session.get("http://ws.audioscrobbler.com/2.0/", params=params) as body:
      body = await body.json()
  try:
      body['artist']['name'], body['artist']['url']
  except:
      return None, None
  return body['artist']['name'], body['artist']['url']

async def get_recent_10(client, username):
  params  = {
      "method": 'user.getrecenttracks',
      "user": username,
      "api_key": api_key,
      "limit": 10,
      "format": 'json'
  }
  async with client.session.get("http://ws.audioscrobbler.com/2.0/", params=params) as body:
      body = await body.json()
  return body['recenttracks']['track']

async def get_user_info(client, username):
  params = {
      "method": 'user.getInfo',
      "user": username,
      "api_key": api_key,
      "format": 'json'
  }
  async with client.session.get("http://ws.audioscrobbler.com/2.0/", params=params) as body:
      d = await body.json()
  return d['user']['registered']['#text'], d['user']['name'], d['user']['url'], d['user']['image'][-1]['#text'], d['user']['playcount']

async def get_top_artists(client, username):
  top_artists_params = {
      "period": "overall",
      "limit": '1000', 
      "user": username,
      "api_key": api_key,
      "format": "json",
      "method": "user.getTopArtists"
  }
  async with client.session.get("http://ws.audioscrobbler.com/2.0/", params=top_artists_params) as r:
      data = await r.json()
  return data["topartists"]["artist"]