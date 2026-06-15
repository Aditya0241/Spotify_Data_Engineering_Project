import json
import boto3
import pandas as pd
from io import StringIO
from datetime import datetime

def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    
    # Get the file that triggered this Lambda
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    print(f"Processing file: {file_key}")
    
    # Read raw JSON from S3
    obj = s3.get_object(Bucket=source_bucket, Key=file_key)
    data = json.loads(obj['Body'].read())
    
    # ── ARTISTS ──────────────────────────────
    artist_df = pd.DataFrame(data['artists'])
    artist_df = artist_df.drop_duplicates('artist_id')
    print(f"✅ Artists: {len(artist_df)}")
    
    # ── ALBUMS ───────────────────────────────
    album_df = pd.DataFrame(data['albums'])
    album_df = album_df.drop_duplicates('album_id')
    album_df['release_date'] = pd.to_datetime(album_df['release_date'], errors='coerce')
    print(f"✅ Albums: {len(album_df)}")
    
    # ── SONGS ────────────────────────────────
    song_df = pd.DataFrame(data['songs'])
    song_df = song_df.drop_duplicates('song_id')
    song_df['duration_secs'] = (song_df['duration_ms'] / 1000).round(2)
    song_df = song_df.drop(columns=['duration_ms'])
    print(f"✅ Songs: {len(song_df)}")
    
    # ── SAVE TO S3 ───────────────────────────
    dest_bucket = 'spotify-processed-playlist'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def save_to_s3(df, folder):
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        key = f"{folder}/spotify_{folder}_{timestamp}.csv"
        s3.put_object(
            Bucket=dest_bucket,
            Key=key,
            Body=csv_buffer.getvalue()
        )
        print(f"✅ {folder} saved to S3!")
    
    save_to_s3(artist_df, 'artists')
    save_to_s3(album_df, 'albums')
    save_to_s3(song_df, 'songs')
    
    # ── MOVE RAW FILE TO PROCESSED ───────────
    processed_key = file_key.replace('to_process', 'processed')
    s3.copy_object(
        Bucket=source_bucket,
        CopySource={'Bucket': source_bucket, 'Key': file_key},
        Key=processed_key
    )
    s3.delete_object(Bucket=source_bucket, Key=file_key)
    print(f"✅ Raw file moved to processed!")
    
    return {'statusCode': 200, 'body': 'Transformation complete'}