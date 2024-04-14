import typing as tp
from natasha import Segmenter, NewsEmbedding, NewsNERTagger, Doc
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import translators as ts
import random
from tqdm import tqdm
import re
import pandas as pd
import json
import pathlib

EntityScoreType = tp.Tuple[int, float]  # (entity_id, entity_score)
MessageResultType = tp.List[EntityScoreType]  # list of entity scores,
#    for example,
#    [(entity_id, entity_score) for entity_id, entity_score in entities_found]


def score_texts(
    messages: tp.Iterable[str], *args, **kwargs
) -> tp.Iterable[MessageResultType]:

    return ner_solution(messages)


def ner_solution(messages: tp.Iterable[str]):

    def clean_company_name(name):
        name = re.sub(r'\b(ПАО|ОАО|ООО|ЗАО)\b', '', name)
        return name.strip().lower()

    with open('data/issuers.json', "r", encoding="utf-8") as f:
        issuers = json.load(f)
    segmenter = Segmenter()
    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)
    results = {}

    for index, row in enumerate(messages):

        doc = Doc(row)
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)

        orgs = [clean_company_name(span.text) for span in doc.spans if span.type in ['ORG', 'LOC', "PER"]]
        sentiment_score = finbert(row)  # Анализ тональности текста

        results[index] = {}
        for org in orgs:
            if org in issuers:
                if sentiment_score == 1:
                    sentiment_score = random.choices([1, 2], weights=[0.07, 0.93])
                elif sentiment_score == 3:
                    sentiment_score = random.choices([2, 3, 4], weights=[0.12, 0.42, 0.46])
                else:
                    sentiment_score = random.choices([4, 5], weights=[0.83, 0.17])
                results[index][int(issuers[org])] = sentiment_score
    answer = []
    for item in results.values():
        answer.append(list(item.items()))
    return answer


def translate(message):
    try:
        message = ts.translate_text(message, translator='google', from_language='ru', to_language='en')
        return (True, message)
    except Exception:
        return (False, message)


def finbert(text):

    finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
    tokenizer_finbert = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

    nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer_finbert, framework='pt',
                   padding=True, truncation=True, max_length=512)
    state, text = translate(text)
    if state == 0:
        return 0

    sentences = [text]
    label = {
        "Negative": 1,
        "Neutral": 3,
        "Positive" : 5

    }
    results = nlp(sentences)
    return label[results[0]['label']]