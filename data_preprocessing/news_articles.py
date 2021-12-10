import json
import requests
import logging
# third party imports
from newspaper import Article
import xmltodict


# function to parse web articles
def parse_article(article_url):
    """
    function which extracts information given a web url

    :param article_url: article url
    :return: json record
    """

    # passing the article url
    article = Article(article_url)

    # downloading the data
    article.download()

    # parsing the article
    article.parse()

    # processing natural language processing on article
    article.nlp()

    # creating a json record
    article_record = {
        "article_title": article.title,  # article title
        "article_authors": article.authors,  # article newspaper_authors
        "article_published_date": str(article.publish_date),  # article published data
        "article_text": article.text,  # article web text
        "images_link": article.top_image,  # article image link
        "video_link": article.movies,  # article video link
        "article_summary": article.summary,  # article summary
        "article_keywords": article.keywords,  # keywords associated with articles
        "article_url": article_url  # article url
    }

    # return json record
    return article_record


# function to extract all article web links
def extract_rss_feeds(xml_url, *header_value):
    """
    function to extract all article web links from an xml file
    :param xml_url: xml link
    """
    if len(header_value):
        for value in header_value:
            response = requests.get(xml_url, headers=value)
    else:
        response = requests.get(xml_url)

    # getting the web page data
    # parsing and storing the data in to a dictionary
    dict_data = xmltodict.parse(response.content)

    # getting all the items from rss
    all_parsed_items = dict_data['rss']['channel']['item']

    # list to store all href
    all_href_links = []

    # iterating through all the parsed items
    for index, values in enumerate(all_parsed_items):
        # getting and storing
        link_href = all_parsed_items[index]['link']
        all_href_links.append(link_href)

    all_articles_records = {}

    # iterating all the links
    for href_link in all_href_links:
        try:
            # passing the article link to parsing function
            article_data = parse_article(href_link)

            # storing the results from functions from dictionary
            all_articles_records[href_link] = article_data
        except Exception as e:
            # logging the error
            logging.error('This is an error message')

    return all_articles_records
