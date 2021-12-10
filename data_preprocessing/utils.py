import yaml
import pymongo


def check_record_exist(database_credentials, article_url, processed=False):
    with pymongo.MongoClient(database_credentials['connection_string']) as client:
        # get the database
        database = client[database_credentials['db_name']]

        if processed:
            # get collection weekly_demand
            article_collection = database.get_collection('processed_news_article')

            # check for article url
            record = article_collection.find_one({"cleaned_article_url": article_url})
        else:
            # get collection weekly_demand
            article_collection = database.get_collection(database_credentials['collection_name'])

            # check for article url
            record = article_collection.find_one({"article_url": article_url})

    if record:
        return True

    return False
