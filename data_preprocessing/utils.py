import yaml
import pymongo


def check_record_exist(database_credentials, article_url, processed=False):
    """
     function to check if a record exists in a database or not

    :param database_credentials: database credentials
    :param article_url: article url
    :param processed: boolean value to process or not
    :return: boolean value
    """
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
