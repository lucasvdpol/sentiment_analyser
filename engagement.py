import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy import text

def get_engagement(engine):
    #Data ophalen
    df_fact = pd.read_sql("SELECT * FROM fact_videostatistics;", engine)

    #Check of het is gelukt met de tabel ophalen
    if df_fact.empty:
        print("Geen data beschikbaar om engagement te berekenen.")
        return

    #Likes per view en comments per view uiterekenen
    df_fact['likes_per_view'] = df_fact.apply(
        lambda x: x['likes'] / x['views'] if x['views'] and x['views'] > 0 else 0,
        axis=1
    )
    df_fact['comments_per_view'] = df_fact.apply(
        lambda x: x['comments'] / x['views'] if x['views'] and x['views'] > 0 else 0,
        axis=1
    )
    #Fout ik had eigenlijk de laatste moeten ophalen
    engagement = df_fact.groupby('video_id').agg({
        'views': 'mean',
        'likes': 'mean',
        'comments': 'mean',
        'likes_per_view': 'mean',
        'comments_per_view': 'mean'
    }).reset_index()

    engagement = engagement.rename(columns={
        'views': 'view_count',
        'likes': 'like_count',
        'comments': 'comment_count'
    })

    features = ['view_count', 'like_count', 'comment_count', 'likes_per_view', 'comments_per_view']
    engagement = engagement.dropna(subset=features)


    #Feature scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(engagement[features])

    X_scaled_df = pd.DataFrame(X_scaled, columns=features)
    X_scaled_df['video_id'] = engagement['video_id']

    #k-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    X_scaled_df['Cluster'] = kmeans.fit_predict(X_scaled_df[features])

    #Engagement per cluster berekenen
    cluster_means = engagement.groupby(X_scaled_df['Cluster'])[['likes_per_view', 'comments_per_view']].mean()

    #Clusters sorteren op like-ratio (laag -> hoog)
    #Cluster getal is altijd random, dus vandaar even kijken welk getal welk label krijgt
    #Fout ik had ook de comments per view moeten meenemen
    sorted_clusters = cluster_means['likes_per_view'].sort_values().index.tolist()

    labels = ['Low Engagement', 'Medium Engagement', 'High Engagement']
    cluster_to_label = {sorted_clusters[i]: labels[i] for i in range(len(sorted_clusters))}

    #Labels toevoegen
    X_scaled_df['Engagement Cluster'] = X_scaled_df['Cluster'].map(cluster_to_label)

    #Opslaan
    with engine.begin() as connection:
        for idx, row in X_scaled_df.iterrows():
            connection.execute(
                text("UPDATE dim_video SET engagement = :engagement WHERE video_id = :video_id"),
                {'engagement': row['Engagement Cluster'], 'video_id': row['video_id']}
            )

    print("Video's gelabeled met engagement")
