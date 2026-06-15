import json
import boto3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime


def lambda_handler(event, context):
    secret_client = boto3.client('secretsmanager')
    secret = secret_client.get_secret_value(SecretId = 'spotify/api-credentials')
    creds = json.loads(secret['SecretString'])


    sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(
        client_id = creds['SPOTIFY_CLIENT_ID'],
        client_secret = creds['SPOTIFY_CLIENT_SECRET']
        ))
    
    artists = ["Taylor Swift", "Drake", "Coldplay", "The Weeknd"]

    artist_list = []
    for artist_name in artists:
        data = sp.search(q=artist_name, type='artist', limit=None)
        artist = data['artists']['items'][0]
        artist_data = {
            'artist_id': artist['id'],
            'artist_name': artist['name'],
            'spotify_url': artist['external_urls']['spotify'],
            'artist_image_url': artist['images'][0]['url'] if artist['images'] else None,
            'uri': artist['uri']
        }
        artist_list.append(artist_data)
        print(f"✅ {artist['name']} — ID: {artist['id']}")
    print(f"\nTotal artists fetched: {len(artist_list)}")

    album_list = []
    for artist in artist_list:
        results = sp.artist_albums(artist['artist_id'], album_type='album', limit=None)
        
        for album in results['items']:
            album_data = {
                'album_id': album['id'],
                'album_name': album['name'],
                'album_type': album['album_type'],
                'total_tracks': album['total_tracks'],
                'release_date': album['release_date'],
                'spotify_url': album['external_urls']['spotify'],
                'album_image_url': album['images'][0]['url'] if album['images'] else None,
                'artist_id': artist['artist_id'],
                'artist_name': artist['artist_name']
            }
            album_list.append(album_data)
            print(f"✅ {artist['artist_name']} — {len(results['items'])} albums fetched!")
    print(f"\nTotal albums fetched: {len(album_list)}")


    song_list = []
    for album in album_list:
        data = sp.album_tracks(album['album_id'], limit=50)
        for track in data['items']:
            song_data = {
                'song_id': track['id'],
                'song_name': track['name'],
                'duration_ms': track['duration_ms'],
                'track_number': track['track_number'],
                'disc_number': track['disc_number'],
                'explicit': track['explicit'],
                'spotify_url': track['external_urls']['spotify'],
                'uri': track['uri'],
                'album_id': album['album_id'],
                'album_name': album['album_name'],
                'artist_id': album['artist_id'],
                'artist_name': album['artist_name']
            }
            song_list.append(song_data)
            print(f"✅ {album['album_name']} — {len(results['items'])} songs fetched!")
    print(f"\nTotal songs fetched: {len(song_list)}")

    raw_data = {
        'artists': artist_list,
        'albums': album_list,
        'songs': song_list,
        'extracted_at': str(datetime.now())
    }

    client = boto3.client('s3')
    filename = "raw_data/to_process/spotify_raw_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".json"
    client.put_object(
        Body = json.dumps(raw_data),
        Bucket = 'spotify-raw-playlist',
        Key = filename
    )

    print(f"✅ Data saved to S3!")
    print(f"Artists: {len(artist_list)}, Albums: {len(album_list)}, Songs: {len(song_list)}")
    return {'statusCode': 200, 'body': 'Extraction complete'}
