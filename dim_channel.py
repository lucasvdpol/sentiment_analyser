from googleapiclient.discovery import build
import os

API_KEY = os.environ.get('API_KEY')


def process_channel(cur, channel_id):
    print(f"Dim_channel aanmaken voor channel met id {channel_id}")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()
    items = response.get("items", [])

    if not items:
        print(f"Geen kanaal gevonden voor id: {channel_id}")
        return None

    item = items[0]
    channel_info = {
        "channel_id": channel_id,
        "name": item['snippet']['title'],
        "description": item['snippet'].get('description'),
        "subscribers": int(item['statistics'].get('subscriberCount', 0)),
        "video_count": int(item['statistics'].get('videoCount', 0)),
        "views": int(item['statistics'].get('viewCount', 0))
    }

    cur.execute("""
                    INSERT INTO dim_channel
                    (channel_id, name, description, subscribers, video_count, views)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (channel_id) DO UPDATE
                    SET subscribers = EXCLUDED.subscribers,
                    video_count = EXCLUDED.video_count,
                    views = EXCLUDED.views;
                """, (
        channel_info["channel_id"],
        channel_info["name"],
        channel_info["description"],
        channel_info["subscribers"],
        channel_info["video_count"],
        channel_info["views"]

    ))

    cur.connection.commit()
