import os
import json
import pandas as pd
import numpy as np
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

file_path = "./data/"

def make_notes_db():
    with open(file_path+'notes.json', encoding='utf-8', mode='r') as f:
        notes_json = json.load(f)
    with open(file_path+'new_notes.json', encoding='utf-8', mode='r') as f:
        notes_json += json.load(f)
    df = pd.DataFrame(notes_json, columns = ['fields'])
    notes_data = pd.DataFrame(list(df['fields'].map(lambda x : {d:x[d] for d in x}))) # 안에 있는 fields로 pandas 생성
    return notes_data

def make_perfumes_db():
    notes_data = make_notes_db()
    with open(file_path+'perfume.json', encoding='utf-8', mode='r') as f:
        perfumes_json = json.load(f)
    df = pd.DataFrame(perfumes_json, columns = ['fields']) # json 데이터로 pandas 생성
    perfumes_data = pd.DataFrame(list(df['fields'].map(lambda x : {d:x[d] for d in x}))) # 안에 있는 fields로 pandas 생성
    #top/heart/base/none을 쳐서 notes로 지정
    perfumes_data['all_notes'] = perfumes_data.apply(lambda x: ' '.join(str(n) for n in (x.top_notes + x.heart_notes + x.base_notes + x.none_notes)), axis='columns')
    perfumes_data['notes'] = perfumes_data.apply(lambda x: ' '.join(notes_data[['name']].loc[n-1].values[0] for n in (x.top_notes + x.heart_notes + x.base_notes + x.none_notes)), axis='columns')
    
    csv_path = file_path+'perfume_notes_data.csv'
    perfumes_data.to_csv(csv_path, index=False)
    return perfumes_data

def read_perfumes_db():
    perfumes_data_path = file_path+'perfume_notes_data.csv'
    if(os.path.isfile(perfumes_data_path)):
        perfumes = pd.read_csv(perfumes_data_path).fillna("")
    else:
        perfumes = make_perfumes_db()
    return perfumes

def tf_idf(df):
    
    tfidf_vector = TfidfVectorizer(analyzer='word',ngram_range=(1,3), min_df=0) # 자연어 벡터화
    tf_vector_notes = tfidf_vector.fit_transform(df['notes']) # 데이터 학습 및 변환
    tfidf_vector_voca = sorted(tfidf_vector.vocabulary_.items()) # 벡터라이저가 학습한 단어사전을 정렬 및 출력
    content_base_similarity = cosine_similarity(tf_vector_notes, tf_vector_notes) # 코사인 유사도
    content_base_similarity = pd.DataFrame(content_base_similarity, index=df.index, columns=df.index)

    csv_path = file_path+'perfume_notes_distance_data.csv'
    content_base_similarity.to_csv(csv_path, index=False)

    return content_base_similarity

def recommend_perfume_list(df,target_perfume_id,limit):
    sim_data_path = file_path+'perfume_notes_distance_data.csv'
    if(os.path.isfile(sim_data_path)):
        similarity_notes = pd.read_csv(sim_data_path)
    else:
        similarity_notes = tf_idf(df)

    target_perfume_index = list(map(lambda x:str(x-1),target_perfume_id)) # pandas column 선택을 위한 숫자배열 문자열배열로 변경 & index와 perfume id만큼 차이
    target_similarity_notes = similarity_notes[target_perfume_index].sum(axis='columns').to_numpy() # 기준아이템이 전체 아이템에 대한 코사인 유사도 합계
    recommand_index = target_similarity_notes.argsort()[::-1][:limit+len(target_perfume_id)] # 코사인 유사도 내림차순으로 정렬된 행렬의 limit 갯수만큼 인덱스 반환
    # result = df.iloc[recommand_index]
    recommand_id = [i+1 for i in recommand_index if i+1 not in target_perfume_id][0:limit]  # 본인 제외 & index와 perfume id만큼 차이
    return recommand_id


def recommend(target_perfume_id=[1],limit=24):
    perfumes = read_perfumes_db()
    result =  recommend_perfume_list(perfumes,target_perfume_id=target_perfume_id,limit=limit)
    return result