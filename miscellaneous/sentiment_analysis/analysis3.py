# processing_functions.py

import pandas as pd
import requests
API_URL = ...
headers = ...


def query(payload):
    response = None
    while not response or response.get('error'):
        response = requests.post(API_URL, headers=headers, json=payload).json()
        print(response if response.get('error') else 'Success!')
    return response


def get_sentiments(course, text):
    response = query({
        "inputs": text,
        "parameters": {"candidate_labels": [course + ' positive', course + ' negative', course + ' neutral']},
    })
    result = {}
    for i in range(3):
        result[response['labels'][i]] = response['scores'][i]
    # courses = row['courses']
    # if len(courses) > 5:
    #     return []
    # result = query({
    #     "inputs": row['text'],
    #     "parameters": {"candidate_labels": [course + ' positive' for course in courses] + [course + ' negative' for course in courses]},
    # })
    # scores = [str(score) for score in result['scores']]
    # return str(','.join(scores))
    print(response)
    return result


def process_chunk(chunk):
    # chunk['courses'] = chunk['courses'].apply(lambda x: x.split(','))
    # chunk['sentiments'] = chunk.apply(get_sentiments, axis=1)
    df_list = []
    for index, row in chunk.iterrows():
        courses = row['courses'].split(',')
        for course in courses:
            scores = get_sentiments(course, row['text'])
            df_list.append({
                'year': row['created_utc'],
                'text': row['text'],
                'course': course,
                'positive_sentiment': scores[course + ' positive'],
                'negative_sentiment': scores[course + ' negative']
            })
    return pd.DataFrame(df_list)
