from config import get_db

# Dashboard DB 
db_dashboard = get_db("Dashboard")

artists_collection = db_dashboard['ArtistMeta']
songs_collection = db_dashboard['SongMeta']
records_collection = db_dashboard['Records']


# MelonChart DB 
db_melon_chart = get_db("MelonChart")

ranked_songs_collection = db_melon_chart['RankedSongs']

# SongData DB 
db_song_data = get_db('SongDataDB')

def get_collection_by_release(release):
    year, month, _ = release.split('-') 
    return db_song_data[f'{year}-{int(month)}']