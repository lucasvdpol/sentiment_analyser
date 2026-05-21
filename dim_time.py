def process_time(cur, collected_at):
    cur.execute("SELECT 1 FROM dim_time WHERE timestamp = %s LIMIT 1;", (collected_at,))
    result = cur.fetchone()
    print(f"Tijd met id {collected_at}: {'gevonden' if result else 'niet gevonden'}")
    # Als er een video bestaat met het video_id, dan true
    if(result is None):
        fill_dim_tijd(cur, collected_at)
    else:
        return


def fill_dim_tijd(cur, collected_at):
    print('Nieuwe dim_tijd aanmaken')
    dim_tijd = {
        "timestamp": collected_at,
        "year": collected_at.year,
        "month": collected_at.month,
        "day": collected_at.day,
        "hour": collected_at.hour,
        "minute": collected_at.minute,
        "second": collected_at.second,
        "day_of_week": collected_at.weekday(),  # maandag=0, zondag=6
        "quarter": (collected_at.month - 1) // 3 + 1
    }

    cur.execute("""
        INSERT INTO dim_time
        (timestamp, year, month, day, hour, minute, second, day_of_week, quarter)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        dim_tijd["timestamp"],
        dim_tijd["year"],
        dim_tijd["month"],
        dim_tijd["day"],
        dim_tijd["hour"],
        dim_tijd["minute"],
        dim_tijd["second"],
        dim_tijd["day_of_week"],
        dim_tijd["quarter"]
    ))

    cur.connection.commit()