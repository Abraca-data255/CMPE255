import data_preprocessing
from database_records import ProcessedNewsArticle
from rule_based_sentimental_analysis import text_blob_sentiment, vader_sentiment
import pymongo
from mongoengine import connect, disconnect
import yaml
from utils import check_record_exist


def process_database_records(database_connection_params):
    """
    function to process database records

    :param database_connection_params: database connection strings
    """

    # make the client connection through pymongo
    client = pymongo.MongoClient(database_connection_params['connection_string'])

    # connect to database connection through mongoengine
    connect(db=database_connection_params['db_name'],
            username=database_connection_params['user_name'],
            password=database_connection_params['password'],
            host=database_connection_params['connection_string'])

    # get the database
    database = client[database_connection_params['db_name']]

    # get collection weekly_demand
    article_collection = database.get_collection(database_connection_params['collection_name'])

    # go through all the documents
    for document in article_collection.find():
        try:
            print(document['article_url'])
            if not check_record_exist(database_connection_params,
                                      document['article_url'],
                                      processed=True):
                # get the article text
                article_text = document['article_text']

                # data pre-processing block
                article_text = data_preprocessing.remove_html_tags(article_text)
                article_text = data_preprocessing.lower_text(article_text)
                article_text = data_preprocessing.remove_urls(article_text)
                article_text = data_preprocessing.remove_accented_chars(article_text)
                article_text = data_preprocessing.expand_contractions(article_text)
                article_text = data_preprocessing.remove_special_characters(article_text)
                article_text = data_preprocessing.remove_stopwords(article_text)
                article_text = data_preprocessing.stemming_text(article_text)

                # making document for processed news article
                current_article = ProcessedNewsArticle()
                current_article.cleaned_source_name = document['source_name']
                current_article.cleaned_article_title = document['article_title']

                original_article_authors = ",".join(document['article_authors'])
                current_article.cleaned_article_authors = data_preprocessing.find_persons(original_article_authors)

                current_article.cleaned_article_published_date = document['article_published_date']
                current_article.cleaned_images_link = document['images_link']
                current_article.cleaned_video_link = document['video_link']
                current_article.cleaned_article_summary = document['article_summary']
                current_article.cleaned_article_url = document['article_url']

                # named entity recognition
                current_article.cleaned_article_text = article_text
                ner_results = data_preprocessing.named_entity_recognition(document['article_text'])
                current_article.cleaned_recognized_entity = ner_results

                current_article.cleaned_article_keywords = document['article_keywords']

                # rule based sentiment analysis
                current_article.text_blob_sentiment = text_blob_sentiment(article_text)
                current_article.vader_sentiment = vader_sentiment(article_text)

                current_article.save()

        except Exception as e:
            print(e)

    # disconnect with the database
    disconnect()


if __name__ == '__main__':
    with open('config.yaml') as f:
        config_dict = yaml.safe_load(f)

    process_database_records(config_dict['newyork_times_database_details'])
    # process_database_records(config_dict['cnbc_database_details'])


