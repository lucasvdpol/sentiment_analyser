from googleapiclient.discovery import build
import isodate
import os

API_KEY = os.environ.get('API_KEY')

def process_video(cur, video_id):
    cur.execute("SELECT 1 FROM dim_video WHERE video_id = %s LIMIT 1;", (video_id,))
    result = cur.fetchone()
    print(f"Video met id {video_id}: {'gevonden' if result else 'niet gevonden'}")
    # Als er een video bestaat met het video_id, dan true
    if result is None:
        fill_dim_video(cur, video_id)
    else:
        return

def fill_dim_video(cur, video_id):
    print(f"dim_video voor video met id {video_id} aanmaken")
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics,recordingDetails",
        id=video_id
    )
    response = request.execute()
    items = response.get("items", [])
    if not items:
        return None

    item = items[0]

    duration_iso = item['contentDetails'].get('duration', 'PT0S')
    duration_sec = int(isodate.parse_duration(duration_iso).total_seconds())

    metadata = {
        "video_id": video_id,
        "title": item['snippet']['title'],
        "published_at": item['snippet'].get('publishedAt'),
        "recording_date": item.get('recordingDetails', {}).get('recordingDate'),
        "duration_sec": duration_sec,
        "resolution": item['contentDetails'].get('definition'),
        "tags": item['snippet'].get('tags', []),
        "language": item['snippet'].get('defaultLanguage')
    }

    cur.execute("""
            INSERT INTO dim_video
            (video_id, title, published_at, recording_date, duration_sec, resolution, tags, language)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (
        video_id,
        metadata["title"],
        metadata["published_at"],
        metadata["recording_date"],
        metadata["duration_sec"],
        metadata["resolution"],
        metadata["tags"],
        metadata["language"]
    ))

    cur.connection.commit()