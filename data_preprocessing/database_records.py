from mongoengine import Document, StringField, \
    URLField, ListField, DictField


# News Article Document Class
class NewsArticles(Document):
    source_name = StringField(required=True)
    article_title = StringField(required=True)
    article_authors = ListField()
    article_published_date = StringField()
    article_text = StringField(required=True)
    images_link = StringField()
    video_link = ListField()
    article_summary = StringField(required=True)
    article_keywords = ListField()
    article_url = URLField(required=True)
    meta = {'allow_inheritance': True}


# Processed News Article Document Class
class ProcessedNewsArticle(Document):
    cleaned_source_name = StringField(required=True)
    cleaned_article_title = StringField(required=True)
    cleaned_article_authors = ListField()
    cleaned_article_published_date = StringField()
    cleaned_article_text = StringField(required=True)
    cleaned_images_link = StringField()
    cleaned_video_link = ListField()
    cleaned_article_summary = StringField(required=True)
    cleaned_article_keywords = ListField()
    cleaned_article_url = URLField(required=True)
    cleaned_recognized_entity = DictField()
    text_blob_sentiment = DictField()
    vader_sentiment = DictField()
    flair_sentiment = DictField()
    transformers_sentiment = DictField()
    overall_sentiment = StringField()
    overall_article_keywords = ListField()
    overall_article_keywords_dict = DictField()
    meta = {'allow_inheritance': True}

