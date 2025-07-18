import pymongo
import pandas as pd


mongo_client = pymongo.MongoClient(
    "mongodb://admin:admin@localhost:27017/reddit?authSource=admin"
)
db = mongo_client.reddit
posts = db.posts


def dump_csv():
    """
    Dump the posts collection to a CSV file.
    """
    cursor = posts.find()
    data = list(cursor)
    print(f"Number of posts: {len(data)}")

    df = pd.DataFrame(data)
    df = df.drop(columns=["_id", "text"])

    df.to_csv('posts.csv', index=False)


if __name__ == "__main__":
    dump_csv()