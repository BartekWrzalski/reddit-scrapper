from prometheus_client import Counter, Histogram, Summary


DOWNLOAD_COUNTER = Counter(
    "reddit_downloads", 
    "Number of succesfull downloads"
)

LANGUAGE_COUNTER = Counter(
    "language_detection", 
    "Number of detected languages", 
    ["language"]
)

FETCHING_TIME = Histogram(
    "reddit_fetching_time",
    "Time taken to fetch submissions from Reddit",
)
LANGUAGE_DETECTING_TIME = Histogram(
    "reddit_language_detecting_time",
    "Time taken to detect language of a submission",
)
VECTORIZE_TIME = Histogram(
    "reddit_vectorize_time",
    "Time taken to vectorize a submission"
)

SCORE_HISTOGRAM = Histogram(
    "reddit_score",
    "Reddit score distribution",
    buckets=[500, 1000, 1500, 2000, 3000, 5000, 7500, 10000, 15000, 20000],
)

COMMENT_HISTOGRAM = Histogram(
    "reddit_comments",
    "Reddit comments distribution",
    buckets=[10, 20, 30, 50, 100, 200, 500, 1000],
)
