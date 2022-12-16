import requests
import pandas as pd
from bs4 import BeautifulSoup
from googletrans import Translator
import json
import time

translator= Translator()
file_path = "./data/"

brand = []
perfume = []
new_notes = []

search_brand_list = []
search_perfume_list = []

def json_file_read(file_name):
    file = f"{file_name}.json"
    with open(file_path+file, 'r') as file:
        json_db = json.load(file)
        df = pd.DataFrame(json_db, columns = ['fields']) # json 데이터로 pandas 생성
        df = pd.DataFrame(list(df['fields'].map(lambda x : {d:x[d] for d in x}))) # 안에 있는 fields로 pandas 생성
    return df


def json_file_create(file_name, data):
    file = f"{file_name}.json"
    with open(file_path+file, 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


def append_brand_data(data):
    for pk, brand_id in enumerate(data) :
        req = requests.get(f'https://basenotes.com/brands/{brand_id}')
        soup = BeautifulSoup(req.text, 'html.parser')
        body = soup.select_one(".p-body-main .bn")
        if(body.select_one("h1")):
            brand_name = body.select_one("h1").text
            thumbnail = body.select_one(".bnheroimage")
            brand_thumbnail = "https://basenotes.com"+thumbnail.get("src") if thumbnail else None

            brand_desc = ""
            brand_desc_ko = ""
            descs_list = body.select(".bncol-9 > div > p, .bncol-9 > div > div[data-xf-p='1']")
            for desc in descs_list:
                if not desc.text:
                    continue
                brand_desc += f'{desc.text}\n'
                brand_desc_trans_ko = translator.translate(desc.text, src="en", dest='ko').text  # 영어 -> 한국어 번역
                brand_desc_ko +=  f'{brand_desc_trans_ko}\n'
            
            link = body.select_one(".bncol-9 ul>li>a")
            brand_link = link.get("href") if link else None

            new_brand = {
                "model": "perfume.brand", 
                "pk": pk+1,
                "fields": {
                    "origin_id": brand_id,
                    "image": brand_thumbnail,
                    "title": brand_name,
                    "website": brand_link,
                    "brand_desc":brand_desc,
                    "brand_desc_ko":brand_desc_ko,
                }
            }
            print(new_brand)
            brand.append(new_brand)
    json_file_create("brand",brand)            


def get_brand_perfume_list(data):
    # 해당 브랜드의 item 목록 가져오기
    for pk, brand_id in enumerate(data) :
        page = 1
        while(True):
            req = requests.get(f'https://basenotes.com/fragrances/page-{page}?brand={brand_id}')
            soup = BeautifulSoup(req.text, 'html.parser')
            body = soup.select_one(".p-body-main .bn")
            brand_item_cards = body.select(".bncardlist .bncards .bncard")
            for pk, item_card in enumerate(brand_item_cards):
                perfume_id = item_card.select_one("a").get("href").split(".")[1]
                search_perfume_list.append(perfume_id)

            btn_next = body.select_one(".block-outer-main .pageNav a.pageNav-jump--next")
            if btn_next:
                page+=1 
            else: 
                break


def append_new_note(df_notes, note_name,note_origin_id=0):
    note_name_ko = translator.translate(note_name, src="en", dest='ko').text if note_name else "" # 영어 -> 한국어 번역
    new_note_data = {
        "name": note_name,
        "kor_name": note_name_ko,
        "image": "",
        "note_category": None
    }
    new_note = {
        "model": "custom_perfume.note",
        "pk": df_notes.shape[0]+1,
        "fields" : new_note_data
    }
    new_notes.append(new_note)
    # note pandas에도 추가
    df_notes.loc[df_notes.shape[0]] = list(new_note_data.values())
    return df_notes.shape[0]


def append_perfume_data(data): 
    df_notes = json_file_read("notes")
    for pk, perfume_id in enumerate(data) :
        req = requests.get(f'https://basenotes.com/fragrances/{perfume_id}')
        soup = BeautifulSoup(req.text, 'html.parser')
        body = soup.select_one(".p-body-main")
        if(body.select_one("h1>span[itemprop='Name']")):
            
            perfume_name = body.select_one("h1>span[itemprop='Name']").text

            thumbnail = body.select_one(".bnheroimageouter>img")
            perfume_thumbnail = "https://basenotes.com"+thumbnail.get("src")

            brand = body.select_one("span[itemprop='brand']>a")
            if brand:
                brand_origin_id = brand.get("href").split(".")[1]
                if(brand_origin_id in search_brand_list):
                    perfume_brand_name = search_brand_list.index(brand_origin_id)+1
                else:
                    print("--- brand 추가---------",search_brand_list)
                    perfume_brand_name = len(search_brand_list)+1
                    search_brand_list.append(brand_origin_id)
            else:
                None
                

            gender = body.select_one("h1>span:nth-child(2)>i")
            perfume_gender = gender.get("class")[0][-1:] if gender else "S" # 향수 주사용 성별 : (F)Female/(M)Male/(S)uniSex
            
            launch_date = body.select_one("h1>span:nth-child(3)>span")
            perfume_launch_date = launch_date.text.split(" ")[-1][1:-1]+"-01-01" if launch_date.text.split(" ")[-1][1:-1] else None 
            
            pirce = body.select_one(".bnminicontainer .bncard.card4 .ebayimage>div")
            perfume_price_unit = pirce.text.replace("\t","").replace("\n","").split(" ")[0] if pirce else "USD"
            perfume_price = float(pirce.text.replace("\t","").replace("\n","").split(" ")[-1]) if pirce else 0

            perfume_desc = body.select_one("p[itemprop='description']").text.replace("\t","").replace("\n","")
            perfume_desc_ko = translator.translate(perfume_desc, src="en", dest='ko').text if perfume_desc else ""
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
                    if not (note_name and note_origin_id):
                        continue
                    elif(not df_notes.loc[df_notes['name'] == note_name].empty):
                        note_id = df_notes.loc[df_notes['name'] == note_name].index.to_list()[0]+1
                    else:
                        note_id = append_new_note(df_notes, note_name,note_origin_id) # 기존 향 DB에 없으면 향 데이터 추가

                    notes_data[note_type].append(note_id)

            # 크롤링향 향 데이터  
            new_perfume = {
                "model": "perfume.perfume",
                "pk": pk+1,
                "fields" : {
                    "origin_id": perfume_id,
                    "image": perfume_thumbnail,
                    "title": perfume_name,
                    "brand": perfume_brand_name,
                    "gender" : perfume_gender,
                    "price" : perfume_price,
                    "price_unit" : perfume_price_unit,
                    "launch_date" : perfume_launch_date,
                    "desc":perfume_desc,
                    "desc_ko":perfume_desc_ko,
                    "top_notes" : notes_data['Top'],
                    "heart_notes" : notes_data['Heart'],
                    "base_notes" : notes_data['Base'],
                    "none_notes" : notes_data['None'],
                }
            }
            print(new_perfume)
            perfume.append(new_perfume)
        
        if (pk+1)%50 == 0 :
            json_file_create("perfume",perfume)
            json_file_create("new_notes",new_notes)
            time.sleep(10)
    
    json_file_create("perfume",perfume)
    json_file_create("new_notes",new_notes)


# 인기 브랜드 추출
def main():
    
    req = requests.get(f'https://basenotes.com/brands/')
    soup = BeautifulSoup(req.text, 'html.parser')
    body = soup.select_one(".p-body-main .bn")
    brand_cards = body.select(".bncard")
    for brand_card in brand_cards:
        link = brand_card.select_one("a").get("href").split(".")[1]
        search_brand_list.append(link)
        
    print(search_brand_list) # ['26185169', '105818', '105811', '105810', '105808', '105807', '105805', '105804', '105803', '105802', '105801', '105799', '100006', '100035', '100132', '100141', '100167', '100181', '100202', '100220', '100260', '100267', '100348', '100352', '100361', '100385', '100394', '100402', '100661', '100690', '100826', '100862', '100884', '101834', '102221', '103019', '100075', '100091', '100612', '100695', '100742', '101815', '102445', '103669', '104040', '104259', '104437', '104825', '102952', '102954', '102951', '103303', '102953', '102924', '102956', '102983', '102949', '102955', '103302', '103304']

    # 해당 브랜드의 향수제품 목록 추출
    get_brand_perfume_list(search_brand_list)
    print(search_brand_list)

    # perfume 상세 데이터 추출
    append_perfume_data(search_perfume_list)
    # brand 상세 데이터 추출
    append_brand_data(search_brand_list)

main()