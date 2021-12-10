# importing libraries
import re
import nltk
from nltk.corpus import stopwords
from contractions import CONTRACTION_MAP
import spacy
import unidecode

# loading en_core_web_md model
# other model details can be found at here - https://spacy.io/models/en
nlp = spacy.load('en_core_web_lg')


# data preprocessing steps functions

# function to remove html tags
def remove_html_tags(text):
    """
    function to remove html tags

    :param text: given text
    :return: filtered text with removed html components
    """
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)


# function to remove accented characters from text
def remove_accented_chars(text):
    """
    function to remove accented characters from text, e.g. café

    :param text: given text
    :return: filtered text with accented text
    """
    text = unidecode.unidecode(text)
    return text


# function to expand the contractions from the text
def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    """
    function to expand the contractions from the text

    :param text: given text
    :param contraction_mapping: given contraction mapping
    :return: expanded contractions
    """
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


# function for named entity recognition
def named_entity_recognition(text):
    """
    function for named entity recognition

    :param text: given text
    :return: dict with named entity entries
    """
    complete_text = nlp(text)
    results = {}
    for ent in complete_text.ents:
        if ent.label_ not in results:
            results[ent.label_] = []
        results[ent.label_].append(ent.text)

    return results


# function to remove stop words from the given text
def remove_stopwords(text):
    """
    function to remove stop words from the given text

    :param text: given text
    :return: filtered text with stop words
    """
    stop_words = set(stopwords.words('english'))
    return " ".join([word for word in str(text).split() if word not in stop_words])


# function to remove special characters from the given text
def remove_special_characters(text, remove_digits=False):
    """
    function to remove special characters from the given text

    :param text: given text
    :param remove_digits: boolean parameter for removing digits
    :return: filtered text
    """
    pattern = r'[^a-zA-z0-9.\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


# function for stemming the text
def stemming_text(text):
    """
    function for stemming the text

    :param text: given text
    :return: transformed text
    """
    stemmer = nltk.porter.PorterStemmer()
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text


# function for lemmatize text
def lemmatize_text(text):
    """
    function for lemmatize text

    :param text: given text
    :return: transformed text
    """
    lemmatizer = nltk.stem.WordNetLemmatizer()
    text = nlp(text)
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])


# function to remove url from given text
def remove_urls(text):
    """
    function to remove url from given text

    :param text: given text
    :return: filtered text
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)


# function for converting the text to lower case
def lower_text(text):
    """
    function for converting the text to lower case

    :param text: given text
    :return: transformed text
    """
    return text.lower()


# function for extracting the url from text
def extract_urls(text):
    """
    function for extracting the url from text

    :param text: given text
    :return: transformed text
    """
    url_list = re.findall(r'(https?://\S+)', text)
    return url_list


# function for extracting the person names from text
def find_persons(text):
    """
    function for extracting the person names from text

    :param text: given text
    :return: transformed text
    """
    doc2 = nlp(text)
    # Identify the persons
    persons = [ent.text for ent in doc2.ents if ent.label_ == 'PERSON']
    return persons
