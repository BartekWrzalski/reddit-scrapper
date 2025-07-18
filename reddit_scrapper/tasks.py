import praw
from langdetect import detect
import pymongo
import fasttext
import os

from celery import shared_task
from reddit_scrapper.metrics import DOWNLOAD_COUNTER, LANGUAGE_COUNTER, SCORE_HISTOGRAM, COMMENT_HISTOGRAM, FETCHING_TIME, LANGUAGE_DETECTING_TIME, VECTORIZE_TIME

reddit = praw.Reddit(
    client_id= os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
)

fasttext_model = fasttext.load_model("models/cc.en.300.bin")


@shared_task()
@FETCHING_TIME.time()
def fetch():
    subreddit = reddit.subreddit("science")
    submissions = subreddit.top(time_filter="month", limit=500)

    i = 0
    for submission in submissions:
        post = {
            "text": submission.title,
            "score": submission.score,
            "num_comments": submission.num_comments,
        }
        SCORE_HISTOGRAM.observe(submission.score)
        COMMENT_HISTOGRAM.observe(submission.num_comments)

        i += 1
        detect_language.delay(post)
    DOWNLOAD_COUNTER.inc(i)


@shared_task(name="language_detection")
@LANGUAGE_DETECTING_TIME.time()
def detect_language(entry):
    try:
        lang = detect(entry["text"])
        entry["language"] = lang

        LANGUAGE_COUNTER.labels(language=lang).inc()

        if lang == "en":
            vectorize.delay(entry)
    except Exception as e:
        print(f"Error detecting language: {e}")


@shared_task(name="text_vectorization")
@VECTORIZE_TIME.time()
def vectorize(entry):
    try:
        vector = fasttext_model.get_sentence_vector(entry["text"]).tolist()
        entry["vector"] = vector

        save_to_db.delay(entry)
    except Exception as e:
        print(f"Error vectorizing text: {e}")


@shared_task(name="save_to_db")
def save_to_db(entry):
    try:
        mongo_client = pymongo.MongoClient(os.getenv("DATABASE_URL"))
        db = mongo_client.reddit
        posts = db.posts

        posts.insert_one(entry)
    except Exception as e:
        print(f"Error saving to database: {e}")
