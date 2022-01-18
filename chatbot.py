#
# Copyright 201-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import pandas as pd

from bm25 import BM25
import unicodedata
import six
from nltk import word_tokenize

import torch
from transformers import pipeline

THRESHOLD = 0.6
N_CONTEXTS = 5

device = 0 if torch.cuda.is_available() else -1
df = pd.read_csv('data/2022-01-07_7-news.csv')
model_name = "mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
model = pipeline('question-answering', model=model_name, tokenizer=model_name, device=device)

def get_opening_message():
    """The variable starting message."""
    return f"Escriba una pregunta, por favor."

def normalize_terms(terms):
    return [remove_diacritics(term).lower() for term in terms]

def remove_diacritics(text, encoding='utf8'):
    nfkd_form = unicodedata.normalize('NFKD', to_unicode(text, encoding))
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode(encoding)

def to_unicode(text, encoding='utf8'):
    if isinstance(text, six.text_type):
        return text
    return text.decode(encoding)

def do_bm25(query, best_n=3):
    """Return the 'best_n' contexts for the query """

    query = normalize_terms(word_tokenize(query))
    text_lines_total = df.text.values

    text_lines_tokens = []
    for title in text_lines_total:
        title = re.sub(r'\W',' ', title) # matches any non-word character 
        title = re.sub(r'\s+',' ', title) # matches any whitespace character 
        title = title.replace('  ', ' ').replace('   ', ' ')
        tx_line = word_tokenize(title)
        text_lines_tokens.append(tx_line)
    
    news = [normalize_terms(sentence) for sentence in text_lines_tokens]
    bm25 = BM25(news)
    best_indexes = bm25.ranked(query, best_n)

    best_sentences = []
    for idx in best_indexes:
        sentence_found = text_lines_total[idx]
        best_sentences.append(sentence_found)

    return best_sentences


# state 1
def get_question(question):
    """Return the answer with best score"""
    contexts = do_bm25(question, best_n=N_CONTEXTS)
 
    best_score = 0
    for context in contexts:
        QA_input = {'question': question, 'context': context}
        res = model(QA_input)
        if res['score'] > best_score:
            best_score = res['score']
            best_answer = res['answer']
        print( "score: {} -- answer: {}".format(res['score'], res['answer']) )
        if best_score > THRESHOLD:
            break

    return "La respuesta es: {}\nCon una probabilidad de {}%\n\nPuede realizar otra pregunta: ".format(
        best_answer, round(best_score*100), 1), 1


# state 2
def end(any_text):
    return "restarting app...\n\n" + get_opening_message(), 1, {}
