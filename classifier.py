import pandas as pd
import pickle
import re
from sqlalchemy import create_engine, text


def classify(engine):
    #Vectorizer inladen
    with open('vectorizer.pkl', 'rb') as f:
        cv = pickle.load(f)

    #Model inladen
    with open('model.pkl', 'rb') as f:
        clf = pickle.load(f)

    #Functie om alle hoofdletters en leestekens weg te halen
    def preprocess_text(text):
        if text is None or text.strip() == "":
            return ""
        text = text.lower()  # lowercase
        text = re.sub(r'[^\w\s]', '', text)  # punctuation verwijderen
        return text

    #Data ophalen
    df_video = pd.read_sql("SELECT * FROM dim_video;", engine)

    #Transcripties met functie bewerken
    df_video['clean_transcript'] = df_video['transcript'].apply(preprocess_text)

    #Vectorizer toepassen
    X_transcripts = cv.transform(df_video['clean_transcript'].values)
    #Omzetten naar normale numpy array?
    X_dense = X_transcripts.toarray()

   #Kijken waar geen vectoren zijn in een rij. Dit betekent dat er geen enkel herkenbaar woord is -> transcript is null
    empty_mask = X_dense.sum(axis=1) == 0

    #Voor alle videos waar geen vector is, dus transcript is null -> sentiment_binary = -1
    df_video.loc[empty_mask, 'sentiment_binary'] = -1
    #~empty mask is het tegenovergestelde van empty_mask, dus hier zitten wel vectoren en een transcirpt in
    #Voorspellen -> krijgt 0 of 1
    df_video.loc[~empty_mask, 'sentiment_binary'] = clf.predict(X_dense[~empty_mask])

    #Getallen omzetten in iets logisch
    labels_naar_sentiment = {-1: 'Unknown', 0: 'Negative', 1: 'Positive'}
    df_video['Sentiment'] = df_video['sentiment_binary'].map(labels_naar_sentiment)

    #Waarden updaten in database
    with engine.begin() as connection:
        for idx, row in df_video.iterrows():
            connection.execute(
                text("""
                                UPDATE dim_video
                                SET sentiment = :sentiment
                                WHERE video_id = :video_id
                            """),
                {"sentiment": row["Sentiment"], "video_id": row["video_id"]}
            )


    print("Videos gelabeled met sentiment")

