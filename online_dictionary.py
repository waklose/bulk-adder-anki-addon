import requests
from bs4 import BeautifulSoup
import json

def contains_kanji(word):
    for char in word:
        if ord(char) >= 19968 and ord(char) <= 40879:
            return True
    return False
    

def search_word(word):
    if not contains_kanji(word):
        print("No kanji found in the word")
        return None
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

    return json.dumps(list_of_kanji_dict, ensure_ascii=False)


#print(search_word("漢字"))