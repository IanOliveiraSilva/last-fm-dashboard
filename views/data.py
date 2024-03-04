import requests
from dotenv import load_dotenv
import os

class DataFetcher:
    def __init__(self, user, period):
        self.user = user
        self.period = period
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.api_url = os.getenv("API_URL")

    def get_json_data(self, method):
        url = f"{self.api_url}?method={method}&user={self.user}&api_key={self.api_key}&period={self.period}&limit=5&format=json"
        response = requests.get(url)
        return response.json()

    def get_user_info(self):
        url = f"{self.api_url}?method=user.getinfo&user={self.user}&api_key={self.api_key}&format=json"
        response = requests.get(url)
        return response.json()
    
    def get_recent_track(self):
        url = f"{self.api_url}?method=user.getrecenttracks&user={self.user}&api_key={self.api_key}&limit=5&format=json"
        response = requests.get(url)
        return response.json()

    def get_similar_artist(self, artist):
        url = f"{self.api_url}?method=artist.getsimilar&artist={artist}&api_key={self.api_key}&limit=5&format=json"
        response = requests.get(url)
        return response.json()
    
    def get_similar_track(self, artist, track):
        url = f"{self.api_url}?method=track.getsimilar&artist={artist}&track={track}&api_key={self.api_key}&limit=5&format=json"
        response = requests.get(url)
        return response.json()
    
    def get_track_info(self, artist, track):
        url = f"{self.api_url}?method=track.getInfo&api_key={self.api_key}&artist={artist}&track={track}&format=json"
        response = requests.get(url)
        return response.json()
    
    def get_artist_info(self, artist): 
        url = f"{self.api_url}?method=artist.getinfo&artist={artist}&api_key={self.api_key}&limit=5&format=json"
        response = requests.get(url)
        return response.json()
    
    
    