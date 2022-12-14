import requests
import pandas as pd  
from bs4 import BeautifulSoup
import json

perfume = []
new_notes = []

# start = 26120000
end = 26192510
start = end - 3000

file_path = "./static/json/"

with open(file_path+"notes.json", 'r') as file:
    notes_db = json.load(file)
    df_notes = pd.DataFrame(notes_db, columns = ['fields']) # json 데이터로 pandas 생성
    df_notes = pd.DataFrame(list(df_notes['fields'].map(lambda x : {d:x[d] for d in x}))) # 안에 있는 fields로 pandas 생성

def append_new_note(note_name,note_origin_id=0):
    new_note_data = {
        "name": note_name,
        "kor_name": "",            
        "image": "",
        "note_category": None
    }
    new_note = {"model": "custom_perfume.note"}
    new_note["fields"] = new_note_data
    new_notes.append(new_note)

    # note pandas에도 추가
    df_notes.loc[df_notes.shape[0]] = list(new_note_data.values())
    return df_notes.shape[0]

for num in range(start, end):
    req = requests.get(f'https://basenotes.com/fragrances/{num}')
    soup = BeautifulSoup(req.text, 'html.parser')
    body = soup.select_one(".p-body-main")
    if(body.select_one("h1>span[itemprop='Name']")):
        # 향수 정보 크롤링
        perfume_name = body.select_one("h1>span[itemprop='Name']").text
        brand = body.select_one("span[itemprop='brand']>a")
        gender = body.select_one("h1>span:nth-child(2)>i")
        launch_date = body.select_one("h1>span:nth-child(3)>span")
        thumbnail = body.select_one(".bnheroimageouter>img")
        pirce = body.select_one(".bnminicontainer .bncard.card4 .ebayimage>div")
        
        perfume_brand_name = brand.text if brand else None
        perfume_gender = gender.get("class")[0][-1:] if gender else "S" # 향수 주사용 성별 : (F)Female/(M)Male/(S)uniSex
        perfume_launch_date = launch_date.text.split(" ")[-1][1:-1]+"-01-01" if launch_date.text.split(" ")[-1][1:-1] else None 
        perfume_thumbnail = "https://basenotes.com"+thumbnail.get("src") if thumbnail else None
        perfume_price = float(pirce.text.replace("USD","").replace("\t","").replace("\n","")) if pirce else 0

        # 향 정보 크롤링
        notes_data = {'Top':[],'Heart':[],'Base':[],'None':[]}
        fragrancenotes = soup.select("ol.fragrancenotes>li")
        for fragrancenote in fragrancenotes:
            note_type =  fragrancenote.select_one("h3").text.replace("\t","").replace("\n","").split(" ")[0] if fragrancenote.select_one("h3") else "None" # 사용된 향의 포지션 :  Top / Heart / Base / None
            notes = fragrancenote.select("li")
            for note in notes:
                if note.select_one("a"):
                    note_name = note.select_one("a").text
                    note_origin_id = note.select_one("a").get("href").split('/')[-1]
                else:
                    note_name = note.text.replace("\t","").replace("\n","")
                    note_origin_id = 0

                # 향DB에 있는 향만 향수 notes필드에 추가
                if(not df_notes.loc[df_notes['name'] == note_name].empty):
                    note_id = df_notes.loc[df_notes['name'] == note_name].index.to_list()[0] +1
                else:
                    note_id = append_new_note(note_name,note_origin_id) # 기존 향 DB에 없으면 향 데이터 추가

                notes_data[note_type].append(note_id)
        # 크롤링향 향 데이터  
        result = {
            "origin_id": num,
            "image": perfume_thumbnail,
            "title": perfume_name,
            "brand": perfume_brand_name,
            "gender" : perfume_gender,
            "price" : perfume_price,
            "launch_date" : perfume_launch_date,
            "top_notes" : notes_data['Top'],
            "heart_notes" : notes_data['Heart'],
            "base_notes" : notes_data['Base'],
            "none_notes" : notes_data['None'],
        }
        new_data = {"model": "perfume.perfume"}
        new_data["fields"] = result
        print(new_data)
        perfume.append(new_data)

# 크롤링한 향수 데이터 json 파일에 저장.
perfume_file = f"perfume.json"
with open(file_path+perfume_file, 'w', encoding="utf-8") as outfile:
    json.dump(perfume, outfile, ensure_ascii=False, indent=4)

# 크롤링한 추가 향 데이터 json 파일에 저장.
notes_file = f"new_notes.json"
with open(file_path+notes_file, 'w', encoding="utf-8") as outfile:
    json.dump(new_notes, outfile, ensure_ascii=False, indent=4)