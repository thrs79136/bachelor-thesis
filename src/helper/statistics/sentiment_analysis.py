from transformers import pipeline, Pipeline, AutoTokenizer

from src.models.song import Song

global classifier
classifier: Pipeline = None


def sentiment_analysis_init():
    global classifier

    # classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=1)
    classifier = pipeline("sentiment-analysis", top_k=1)


def start_sentiment_analysis(song: Song):
    global classifier

    print('sentiment analysis for ' + str(song.mcgill_billboard_id))

    lyrics = song.get_lyrics()
    if lyrics == 'Instrumental':
        return

    prediction = classifier(lyrics, return_all_scores=True, truncation=True)
    song.sentiments = prediction[0]



def get_lyrics_emotions(song: Song):
    global classifier



    lyrics = song.get_lyrics()
    if lyrics == 'Instrumental':
        song.emotions = None
        return

    # summarizer = pipeline('summarization', model ='Saravananofficial/Text_Summarizer', framework ='tf')
    # summary = summarizer(lyrics, max_length=130, min_length=60)

    try:
        # tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        # result = tokenizer.encode(lyrics, max_length=512)

        prediction = classifier(lyrics, return_all_scores=True, truncation=True)
        song.emotions = prediction[0]
    except Exception:
        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased", max_length=512)
        result = tokenizer.tokenize(lyrics)
        print((result))
        x = 42

