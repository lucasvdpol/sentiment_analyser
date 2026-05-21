import os
import yt_dlp
import whisper
from sqlalchemy import create_engine

def extract_transcript(video_path, model):
    if not os.path.isfile(video_path):
        return None

    print(f"Transcriberen: {video_path}")
    result = model.transcribe(video_path, language="en")
    return result.get("text", "")


def save_transcript_to_db(cur, video_id, transcript):
    cur.execute("""
        UPDATE dim_video
        SET transcript = %s
        WHERE video_id = %s;
    """, (transcript, video_id))
    cur.connection.commit()
    print(f"Transcript opgeslagen voor video {video_id}")


def process_transcript(video_id, video_dir, cur, model):
    cur.execute("SELECT transcript FROM dim_video WHERE video_id = %s LIMIT 1;", (video_id,))
    result = cur.fetchone()
    if result and result[0]:
        print(f"Transcript al aanwezig voor {video_id}, overslaan.")
        return

    # Video pad verkrijgen
    video_path = os.path.join(video_dir, video_id)
    # Transcript extraheren
    transcript = extract_transcript(video_path, model)
    if transcript:
        save_transcript_to_db(cur, video_id, transcript)
    else:
        print(f"Transcript extractie mislukt voor {video_id}")
