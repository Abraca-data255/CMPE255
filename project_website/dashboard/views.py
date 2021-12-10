import logging
import yaml
from django.shortcuts import render, redirect
from .database_records import NewsArticles, ProcessedNewsArticle
from mongoengine import connect, disconnect
import glob
import json
import pymongo


def calculate_number_of_records(database_connection_string,
                                database_name,
                                collection_name):
    try:
        # connect to the database
        client = pymongo.MongoClient(database_connection_string)

        # get the database
        database = client[database_name]

        # get collection name
        weekly_demand_collection = database.get_collection(collection_name)

        # get the total count
        total_count = weekly_demand_collection.find().count()

        # return total count
        return total_count
    except Exception as e:
        return 0


def index(request):
    template = 'index.html'

    # reading config file
    with open("config.yaml", "r") as stream:
        try:
            config_file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

    newyork_records_count = calculate_number_of_records(config_file['newyork_times']['connection_string'],
                                                        config_file['newyork_times']['database_name'],
                                                        config_file['newyork_times']['collection_name'])

    cnbc_records_count = calculate_number_of_records(config_file['cnbc']['connection_string'],
                                                     config_file['cnbc']['database_name'],
                                                     config_file['cnbc']['collection_name'])

    total_records = newyork_records_count + cnbc_records_count

    context = {
        "newyork_times_records": newyork_records_count,
        "cnbc_records": cnbc_records_count,
        "total_records": total_records
    }

    return render(request, template, context)


def search_results(request):
    template = 'results.html'
    query_keywords = request.GET.get('keywords')

    # reading config file
    with open("config.yaml", "r") as stream:
        try:
            config_file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

    database_connection_params = config_file['cnbc_database_details']

    # connect to database connection through mongoengine
    connect(db=database_connection_params['db_name'],
            username=database_connection_params['user_name'],
            password=database_connection_params['password'],
            host=database_connection_params['connection_string'])

    all_articles_cnbc = ProcessedNewsArticle.objects(overall_article_keywords=str(query_keywords))[:50]
    disconnect()

    database_connection_params = config_file['newyork_times_database_details']
    # connect to database connection through mongoengine
    connect(db=database_connection_params['db_name'],
            username=database_connection_params['user_name'],
            password=database_connection_params['password'],
            host=database_connection_params['connection_string'])

    all_articles_newyork = ProcessedNewsArticle.objects(overall_article_keywords=str(query_keywords))[:50]
    disconnect()

    context = {'all_articles_cnbc': all_articles_cnbc,
               'cnbc_count': len(all_articles_cnbc),
               'all_articles_nytimes': all_articles_newyork,
               'nytimes_count': len(all_articles_newyork)}

    return render(request, template, context)
