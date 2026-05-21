import psycopg2
import os
import time
from datetime import datetime
from metadata import *
from dim_video import *
from dim_channel import *
from dim_category import *
from engagement import *
from transcript import process_transcript
from classifier import *
from sqlalchemy import create_engine
from dim_time import *

import whisper

video_dir = "/app/youtube"

def main():
    conn = psycopg2.connect(
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        host=os.getenv('DB_HOST'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

    #Verbinding maken
    cur = conn.cursor()

    model = whisper.load_model("tiny")
    engine = create_engine("postgresql+psycopg2://s1156206:s1156206@95.217.3.61/indatad_s1156206")

    print(datetime.now())

    # Controleren
    for video_id in os.listdir(video_dir):
        print('Metadata ophalen van video met video_id ' + video_id , flush=True)
        print(datetime.now())
        # Metadata ophalen van een video
        video_metadata = get_metadata(video_id)
        if video_metadata is None:
            continue
        collected_at = store_metadata(cur, video_id, video_metadata)
        #Dim_time
        process_time(cur, collected_at)
        #Dim_video
        process_video(cur, video_id)
        #Dim_category
        process_category(cur, video_metadata['category_id'])
        #Dim_channel
        process_channel(cur, video_metadata["channel_id"])
        #Transcript
        process_transcript(video_id, video_dir, cur, model)


        conn.commit()

    print(datetime.now())
    print('Doorgaan naar engagement ', flush=True)
    print(datetime.now())
    get_engagement(engine)
    print('Doorgaan met sentiment', flush=True)
    print(datetime.now())
    classify(engine)
    print(datetime.now())

    conn.commit()

    # #Wijzigingen opslaan en verbinding verbreken
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
