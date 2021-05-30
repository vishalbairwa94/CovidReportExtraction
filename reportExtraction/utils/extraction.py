from autocorrect import Speller
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import re

stop = stopwords.words('english')
import datetime
from datetime import datetime, timezone
from dateutil.parser import parse
from date_extractor import extract_dates

spell = Speller(lang='en')


def name_extraction(text_list):
    # input will be list of text splitted i.e whole report splitted into sentences.
    # each index of list is one sentence

    name_phrases = ['name', 'patient name', 'patient']
    text_with_name = []
    for each in text_list:
        for i in name_phrases:
            if i in each.lower():
                text_with_name.append(each)
    result = " ".join(text_with_name)

    st = StanfordNERTagger(
        '/Users/vishalbairwa/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz',
        '/Users/vishalbairwa/stanford-ner-2020-11-17/stanford-ner.jar',
        encoding='utf-8')
    tokenized_text = word_tokenize(result)
    classified_text = st.tag(tokenized_text)
    person_names = []
    for i in classified_text:
        if i[1] == 'PERSON' and i[0].isupper():
            person_names.append(i[0])
    name = " ".join(person_names)
    return name


def report_result(text_list):
    # input will be list of text splitted i.e whole report splitted into sentences.
    # each index of list is one sentence

    result_phrases = ['result',
                      'interpretation',
                      'examination',
                      'investigation',
                      'observation']
    text_with_result_report = []
    for each in text_list:
        for i in result_phrases:
            if i in each.lower():
                text_with_result_report.append(each)

    result = None
    for i in text_with_result_report:
        if 'positive' in spell(i.lower()) or 'detected' in spell(i.lower()):
            result = 'POSITIVE'
        if 'negative' in spell(i.lower()):
            result = 'NEGATIVE'
    return result


# def fetch_date(text_list):
#     # input will be list of text splitted i.e whole report splitted into sentences.
#     # each index of list is one sentence
#     ps = PorterStemmer()
#
#     text_with_collect_phrases = []
#     for j in range(0, len(text_list) - 1):
#         for each in [ps.stem(x) for x in text_list[j].split(" ")]:
#             if 'collect' in spell(each) or 'coll' in spell(each):
#                 text_with_collect_phrases.append(text_list[j])
#
#     collect_phrases_list_cleaned = []
#     for i in text_with_collect_phrases:
#         tokens = i.split(" ")
#         cleaned_tokens = []
#         cleaned_sentence = None
#         for j in tokens:
#             if len(j) != 1:
#                 cleaned_tokens.append(j)
#         cleaned_sentence = " ".join(cleaned_tokens)
#         collect_phrases_list_cleaned.append(cleaned_sentence)
#
#     date_formats = ['%m/%d/%Y', '%m/%d/%y', '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y', '%m-%d-%Y',
#                     '%m-%d-%y', '%Y-%m-%d', '%f/%e/%Y', '%f/%e/%y', '%e/%f/%Y', '%e/%f/%y', '%f-%e-%Y',
#                     '%f-%e-%y', '%e-%f-%Y', '%e-%f-%y', '%b %e, %Y', '%B %e, %Y', '%b %d, %Y',
#                     '%B %d, %Y', '%Y-%m-%d %H:%M:%S', '%m-%b-%Y', '%m-%B-%Y', '%m/%b/%Y', '%m/%B/%Y', '%d/%B/%Y']
#     date = None
#     for sents in collect_phrases_list_cleaned:
#         tokens = sents.split(" ")
#         for token in tokens:
#             for formats in date_formats:
#                 try:
#                     if('-' in token[0] or '.' in token[0] or '—' in token[0]):
#                         token = token[1:]
#                     if('-' in token[-1] or '.' in token[-1] or '—' in token[-1]):
#                         token = token[:-1]
#                     form = datetime.strptime(token, formats)
#                     date = token
#                 except:
#                     pass
#
#     return date


def validation(days):
    hours = days * 24

    validation = None

    if hours > 72:
        validation = "NOT VALIDATED"
    else:
        validation = "VALIDATED"

    return validation

def date_Parsing(text_list):
    cleaned_text = []
    for each in text_list:
        if len(each) > 4:
            cleaned_text.append(each)
    cleaned_text = cleaned_text[0:int(len(cleaned_text))]

    date = []
    for i in cleaned_text:
        date.append(extract_dates(i))

    cleaned_dates = []
    for each in date:
        if(len(each) != 0):
            find_year = each[0]
            if(find_year.year == 2021 or find_year.year == 2020):
                cleaned_dates.append(each)

    final = []
    for i in cleaned_dates:
        if(len(i) == 1):
            final.append(i[0])
        if(len(i) > 1):
            for each in i:
                find_year = each
                if(find_year.year == 2021):
                    final.append(each)
    min_date = min(final)
    now = datetime.now(timezone.utc)

    diff = (now -min_date).days
    return diff

