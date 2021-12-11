# FETCHING DATA FROM DB
from mongoengine import connect, disconnect
# from database_records import NewsArticle

# GOOGLE RESULT OF AUTHOR
import googlesearch

# TWITTER API
import tweepy

# READING ENV FILE
from dotenv import load_dotenv
import os


# GETTING KEYS FROM ENV FILE
load_dotenv()
auth = tweepy.OAuthHandler(
    os.getenv("TWITTER_CONSUMER_API_KEY"), os.getenv("TWITTER_CONSUMER_SECRET_API_KEY")
)
auth.set_access_token(
    os.getenv("TWITTER_ACCESS_TOKEN_KEY"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
)

api = tweepy.API(auth)


def get_authors():
    # CONNECT TO MONGO DB
    connect(
        db="cnbc",
        username="dataminingadmin",
        password="fall2021project",
        host="mongodb+srv://dataminingadmin:fall2021project@cluster1.ngjps.mongodb.net/cnbc",
    )

    # COLLECT ALL AUTHOR NAMES FROM THE DATABASE
    authors = set()

    for article in NewsArticle.objects():
        for author in article.article_authors:
            authors.add(author)

    disconnect()

    return authors


def google_search_author(authors):
    # FETCH FOLLOWER COUNT OF AUTHOR
    for author in authors:

        # GOOGLE SEARCH NAME OF AUTHOR AND ADD TWTIITER TO GET TWITTER USERNAME
        for res in googlesearch.search(
            author.replace(" ", "+") + "+twitter", num_results=10, lang="en"
        ):

            # USE TWITTER API TO GET FOLLOWER COUNT OF AUTHOR
            if "//twitter.com" in res:
                twitter_id = res[res.find(".com/") + 5 : res.find("?")]
                print(author, twitter_id)
                print(api.get_user(screen_name=twitter_id).followers_count)
                break


# GETTING BEARER TOEKN FROM ENV FILE
load_dotenv()
Client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))


def twitter_api(tweeter_account_id):
    # GET ALL USERNAMES OF AUTHORS WHO CNBC FOLLOWS (CNBC_ID = 20402945)

    f = open("nytimes_authors.csv", "a")
    f.write("name, username, id, followings\n")
    cnbc_following = Client.get_users_following(
        id=tweeter_account_id, max_results=1000
    ).data

    for username in cnbc_following:
        x = api.get_user(screen_name = username.username)
        f.write(username.name + ", " + username.username + ", " + str(username.id) + ", " + str(x.followers_count) + "\n")
    f.close()
    # for username in cnbc_following[:2]:
    #     print(Client.get_user(username=username, user_fields=["public_metrics", "url"]))

    # # GET ALL USERNAMES OF AUTHORS WHO NYTIMES FOLLOWS
    # nytimes_following = Client.get_users_followers(id=tweeter_account_id, max_results=2).data
    # print(nytimes_following[0])

twitter_api(807095)


# CNBC -> 
    # cnbc details => https://api.twitter.com/2/users/by/username/cnbc?user.fields=public_metrics
    # FOLLOWINGS => https://api.twitter.com/2/users/20402945/following?max_results=1000

# NYTIMES -> 
    # nytimes details => https://api.twitter.com/2/users/by/username/nytimes?user.fields=public_metrics
    # FOLLOWINGS => https://api.twitter.com/2/users/807095/following?max_results=1000
