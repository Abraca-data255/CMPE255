from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newspaper import Article
import nltk

nltk.data.path.append("/tmp")
nltk.download("punkt", download_dir="/tmp")


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
        "article_authors": article.authors,  # article authors
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


def text_blob_sentiment(given_sentence):
    overall_results = TextBlob(given_sentence).sentiment
    results = {
        'sentiment': overall_results.polarity,
        'confidence': overall_results.subjectivity
    }
    return results


def vader_sentiment(given_sentence):
    analyser = SentimentIntensityAnalyzer()
    overall_results = analyser.polarity_scores(given_sentence)
    return overall_results


class TextBlobView(APIView):
    def post(self, request):
        given_text = request.data['text']
        response_from_method = text_blob_sentiment(given_text)
        return Response({"status": "success",
                         "given_text": given_text,
                         "results": response_from_method},
                        status=status.HTTP_200_OK)


class VaderView(APIView):
    def post(self, request):
        given_text = request.data['text']
        response_from_method = vader_sentiment(given_text)
        return Response({"status": "success",
                         "given_text": given_text,
                         "results": response_from_method},
                        status=status.HTTP_200_OK)


class ArticleData(APIView):
    def post(self, request):
        given_url = request.data['url']
        response_from_method = parse_article(given_url)
        return Response({"status": "success",
                         "given_url": given_url,
                         "results": response_from_method},
                        status=status.HTTP_200_OK)
