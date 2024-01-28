import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text="""Diwali, also referred to as Deepavali, is one of the most prominent festivals of the Hindu community. This festival of lights holds a sacred place in the hearts of millions around the globe. With its origins deeply rooted in the rich tapestry of Indian culture, this enchanting celebration marks the triumph of light over darkness, knowledge over ignorance, and joy over despair. In this article, we will learn all about Diwali, its history and significance, when is Diwali 2023, the timing of Lakshmi Puja, how to celebrate etc.According to the ancient calendar, Diwali is observed on Amavasya (or new moon) — the 15th day — of the month of Kartik, every year. In 2023, Diwali will be celebrated on 12th November (Sunday). Diwali is observed as a Gazetted Holiday throughout the nation. According to the Hindu calendar, this year Diwali will be celebrated after 20 days of the Dussehra 2023 festival."""

def summarizer(rawdocs):
    stopwords= list(STOP_WORDS)
    # print(stopwords)
    nlp=spacy.load('en_core_web_sm')
    doc =nlp(rawdocs)
    # print(doc)
    tokens= [token.text for token in doc]
    # print(tokens)
    word_freq ={}
    for word in doc: 
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1

    # print(word_freq)

    max_freq = max(word_freq.values())
    # print(max_freq)        

    for word in word_freq.keys():
        word_freq[word] =word_freq[word]/max_freq
    # print(word_freq)        #normalized frequency

    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]= word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    # print(sent_scores)

    # SUMMARY
    select_len = int(len(sent_tokens) * 0.3)
    # print(select_len)

    summary = nlargest(select_len, sent_scores, key= sent_scores.get)
    # print(summary)

    final_summary =[word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("Lenght of original text",len(text.split(' ')))
    # print("Lenght of summary text",len(summary.split(' ')))

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))