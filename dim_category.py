from googleapiclient.discovery import build
import os

API_KEY = os.environ.get('API_KEY')

def process_category(cur, category_id):
    cur.execute("SELECT 1 FROM dim_category WHERE category_id = %s LIMIT 1;", (category_id,))
    result = cur.fetchone()
    print(f"Category met id {category_id}: {'gevonden' if result else 'niet gevonden'}")
    if result is None:
        fill_dim_category(cur, category_id)
    else:
        return

def fill_dim_category(cur, category_id):
    print(f"dim_category voor video met id {category_id} aanmaken")
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.videoCategories().list(
        part="snippet",
        id = category_id,
    )
    response = request.execute()
    items = response.get("items", [])
    if not items:
        return None

    item = items[0]

    categories = {
        "category_id": item["id"],
        "category_name": item['snippet']['title'],
    }

    cur.execute("""
                INSERT INTO dim_category
                (category_id, category_name)
                VALUES (%s, %s);
            """, (
        categories["category_id"],
        categories["category_name"],
    ))

    cur.connection.commit()