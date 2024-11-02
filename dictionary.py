import requests
from bs4 import BeautifulSoup
import json

from . import config

def contains_kanji(word):
    for char in word:
        if ord(char) >= 19968 and ord(char) <= 40879:
            return True
    return False

def kanji_in_word(word):
    kanji_list = []
    for char in word:
        if ord(char) >= 19968 and ord(char) <= 40879:
            kanji_list.append(char)
    return kanji_list
    
def search_word(word, online = False):
    if not contains_kanji(word):
        return None
    
    if online:
        url = f"https://jisho.org/search/{word}%20%23kanji"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        search_results = soup.find_all("div", class_="kanji details")

        list_of_kanji_dict = []
        for elem in search_results:
            kanji_dict = {}
            first_row = elem.find("div", class_="row") 
            kanji_dict["kanji"] = first_row.find("h1", class_="character").text.strip()

            first_row_details = first_row.find("div", class_="row kanji-details--section")

            kanji_dict["meaning"] = first_row_details.find("div", class_="kanji-details__main-meanings").text.strip()
            try:
                kanji_dict["kunyomi"] = first_row_details.find("dl", class_="dictionary_entry kun_yomi").find("a").text.strip()
            except:
                kanji_dict["kunyomi"] = ""
            try:
                kanji_dict["onyomi"] = first_row_details.find("dl", class_="dictionary_entry on_yomi").find("a").text.strip()
            except:
                kanji_dict["onyomi"] = ""
            try:
                kanji_dict["jlpt"] = first_row_details.find("div", class_="kanji_stats").find("div", class_="jlpt").find("strong").text.strip()
            except:
                kanji_dict["jlpt"] = ""
            list_of_kanji_dict.append(kanji_dict)
    else:
        list_of_kanji_dict = []
        for kanji in kanji_in_word(word):
            kanji_dict = {}
            kanji_dict["kanji"] = kanji

            try:
                kanji_dict["meaning"] = ", ".join(config.full_kanji_dictionary[kanji][4])
            except:
                print(kanji.encode('utf-8'))
                continue
            kanji_dict["kunyomi"] = config.full_kanji_dictionary[kanji][2].replace(" ", "、")
            kanji_dict["onyomi"] = config.full_kanji_dictionary[kanji][1].replace(" ", "、")
            try:
                kanji_dict["jlpt"] = config.full_kanji_dictionary[kanji][5]["jlpt"]
            except:
                kanji_dict["jlpt"] = ""

            list_of_kanji_dict.append(kanji_dict)
        

    return json.dumps(list_of_kanji_dict, ensure_ascii=False)


print(search_word("漢字"))