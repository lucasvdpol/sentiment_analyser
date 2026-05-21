from googleapiclient.discovery import build
import isodate
import os

API_KEY = os.environ.get('API_KEY')


def get_metadata(video_id):
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

    metadata = {
        "video_id": video_id,
        "channel_id": item["snippet"]["channelId"],
        "category_id": item["snippet"]["categoryId"],
        "views": int(item['statistics'].get('viewCount', 0)),
        "likes": int(item['statistics'].get('likeCount', 0)),
        "comments": int(item['statistics'].get('commentCount', 0)),
    }

    return metadata

def store_metadata(cur, video_id, metadata):
    cur.execute("""
        INSERT INTO fact_videostatistics
        (video_id, channel_id, category_id, views, likes, comments)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING collected_at;
    """, (
        video_id,
        metadata["channel_id"],
        metadata["category_id"],
        metadata["views"],
        metadata["likes"],
        metadata["comments"],
    ))

    collected_at = cur.fetchone()[0]
    cur.connection.commit()
    return collected_at




