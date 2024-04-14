import typing as tp
from natasha import Segmenter, NewsEmbedding, NewsNERTagger, Doc
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

    with open(pathlib.Path("data") / 'issuers.json', "r", encoding="utf-8") as f:
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

        results[index] = {}
        for org in orgs:
            if org in issuers:
                results[index][int(issuers[org])] = 0
    answer = []
    for item in results.values():
        answer.append(list(item.items()))
    return answer