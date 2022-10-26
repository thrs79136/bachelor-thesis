from transformers import pipeline, Pipeline
from src.models.song import Song

global classifier_neg_pos
classifier_neg_pos: Pipeline = None

global classifier_emotions
classifier_emotions: Pipeline = None


def sentiment_analysis_init():
    global classifier_neg_pos, classifier_emotions

    classifier_emotions = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=1)
    classifier_neg_pos = pipeline("sentiment-analysis", top_k=1)


def sentiment_analysis_neg_pos(song: Song):
    global classifier_emotions

    prediction = sentiment_analysis(song, classifier_neg_pos)
    if prediction is not None:
        song.sentiments = prediction[0]


def sentiment_analysis_emotions(song: Song):
    global classifier_emotions

    prediction = sentiment_analysis(song, classifier_emotions)
    if prediction is not None:
        song.emotions = prediction[0]


def sentiment_analysis(song: Song, classifier):
    lyrics = song.get_lyrics()
    if lyrics == 'Instrumental':
        return None

    prediction = classifier(lyrics, return_all_scores=True, truncation=True)
    return prediction
