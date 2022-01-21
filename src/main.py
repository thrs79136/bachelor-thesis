import settings
from src.helper import spotify_api
from src.helper.mcgill_billboard_helper import get_mcgill_song_ids, get_song_by_mcgill_id
from src.helper.csv_helper import save_song, get_songs, write_header
from src.models.song import Song
import time

settings.init_logger()
spotify_api.init()

mcgill_ids = get_mcgill_song_ids()

write_header('songs.csv')


len = len(mcgill_ids)

# 0% progress
settings.printProgressBar(0, len, prefix='Progress:', suffix='Complete', length=50)
for i, item in enumerate(mcgill_ids):
    # Do stuff...
    song = get_song_by_mcgill_id(item)
    save_song('songs.csv', song)
    # Update Progress Bar
    settings.printProgressBar(i + 1, len, prefix = 'Progress:', suffix = 'Complete', length = 50)



# 25tZHMv3ctlzqDaHAeuU9c
