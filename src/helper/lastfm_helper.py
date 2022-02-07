import requests
import logging

import json

API_KEY = '3238395ba98fc958e6e371d9c453eb7a'
CLIENT_SECRET = '898ab4eaac6dd541ea73f61813efd3e0'
USER_AGENT = 'https://github.com/thrs79136/bachelor-thesis'

logger = logging.getLogger(__name__)

class LastFmHelper:

    @staticmethod
    def lastfm_get(payload):
        # define headers and URL
        headers = {'user-agent': USER_AGENT}
        url = 'https://ws.audioscrobbler.com/2.0/'

        # Add API key and format to the payload
        payload['api_key'] = API_KEY
        payload['format'] = 'json'

        response = requests.get(url, headers=headers, params=payload)
        return response


    @staticmethod
    def get_track_tags(song_name: str, artist: str) -> list:
        response = LastFmHelper.lastfm_get({
            'method': 'track.getInfo',
            'track': song_name,
            'artist': artist,
            'autocorrect': 1
        })
        if 'error' in response.json():
            logger.warning(f'Song \'{artist} - {song_name}\' could not be found on LastFM')
            return None

        # LastFmHelper.jprint(response.json())
        tags = response.json()['track']['toptags']['tag']
        result = list(map(lambda tag: tag['name'].lower(), tags))
        return result


    @staticmethod
    def jprint(obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

