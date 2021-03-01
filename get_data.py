# CC BY 4.0
# © 2021 Daniel Iova

import concurrent.futures as cf
import re
import string
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from unidecode import unidecode

from dict_operations import add_to_global_tree

def get_image_url(soup : BeautifulSoup, murderer : dict):
    '''
    Returns :
        - Url of image, if the filename of the image corresponds to the murderer's name.
        - None, if it doesn't correspond.
    '''
    img_urls = soup.find_all("img")
    for img in img_urls:
        if "../images/" in img["src"]:
            tokens = re.split("/", img["src"], re.UNICODE)
            ratio = fuzz.token_set_ratio(tokens[-2], re.sub(r"\d+", "", tokens[-1]))
            if (ratio > 25):
                img_url = murderer["Base_URL"] + img["src"][3:]
                return img_url
    return "IMG_NOT_FOUND"

def get_page_lang(soup):
    '''
    Returns the page language (e.g. "en" - English, "es" - Spanish)
    '''
    lang = str(soup.find("meta", attrs= {"http-equiv":"Content-Language"}))
    lang = lang[lang.find("content=") + 9 : lang.find("content=") + 11]
    return lang

def process_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace('\t', '')
    text = text.replace('\n', '')
    return text

def get_tables(soup, font_size = 8):
    '''
    Returns the list of <table> tags corresponding to the site's data table and the given font size.
    '''
    return soup.find_all(name = "table", 
                           attrs = {"border" : "0",
                                    "style" : f"font-size: {font_size}pt; color: #000000; border-collapse: collapse", 
                                    "cellpadding":"0" }), font_size
def get_data(murderer):
    '''
    Builds data using the given murderer dictionary.\n
    Returns a dictionary with the computed data.
    '''
    data_dict = {}

    # Get url and html content
    url = murderer["Murderpedia_URL"]
    r = requests.get(url, headers = {"User-Agent": 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
    c = r.content
    soup = BeautifulSoup(c, "html5lib")

    # Return none if the page is not in english
    if get_page_lang(soup) != "en":
        return None

    # Get image url
    data_dict["Image_URL"] = get_image_url(soup, murderer)

    # Find tables that are specific to the data section
    tables, font_size = get_tables(soup)
    if tables == []:
        tables, font_size = get_tables(soup, 10)
    
    for t in tables:
        # Find all <td> tags that are specific to the data table
        tds = t.find_all(name = "td", attrs = {"width":"100%", "style": f"font-size: {font_size}pt; color: #000000"})
        # Build a data list:
        #   - beginning with the string containing "Classification:"
        #   - ending with the string containing "Status:"
        data_list = []
        i = 0
        ok = 0
        classif_index = 0
        for td in tds:
            data_list.append(process_text(td.text))
            if "Classification:" in data_list[i]:
                classif_index = i
            i+= 1
            if "Status:" in td.text:
                ok = 1
                break
        if ok == 1:
            break
    data_list = data_list[classif_index:]
    # Get dictionary from list and update the data_dict with it
    data_dict.update(get_dict_from_data_list(data_list))

    return data_dict

def get_dict_from_data_list(data_list):
    '''
    Computes the data dictionary using the given data_list.\n
    Returns a data dictionary.
    '''
    data_dict = {}
    for item in data_list:
        item = re.sub(r"\:+", ":", item)
        split = re.split(r"\:", item)
        data_dict[unidecode(process_text(split[0]))] = unidecode(process_text(split[1]))
    return data_dict


def process_murderer(gender, letter, murderer, index):
    '''
    Computes the data dictionary for the murderer using the given parameters.\n
    Returns : touple (gender, letter, computed data)
    '''
    data = {}
    data["Name"] = murderer["Name"]
    data["Murderpedia_URL"] = murderer["Murderpedia_URL"]
    data.update(get_data(murderer))
    return gender, letter, data, index


def process_all_murderers(workers):
    '''
    Assigns data scraped from https://murderpedia.org 
    to the global json tree variable global_dataset.\n
    '''
    genders = ["male", "female"]
    alphabet = list(string.ascii_uppercase)

    for gender in genders:
        base = "http://murderpedia.org/" + gender
        for letter in alphabet:
            
            # Build url and get html content
            url = f"{base}.{letter}/index.{letter}.htm"
            r = requests.get(url, headers = {"User-Agent": 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
            c = r.content
            soup = BeautifulSoup(c, "html5lib")

            # Build a list of all correct <tr> rows
            allrows = soup.findAll("tr")
            rows = [row for row in allrows if row.text.strip() != ""][13:]
            
            # Build the entry_thread_list used to facilitate multithreading
            entry_thread_list = []
            index = 0
            for row in rows:
                data = row.findAll("td")
                links  = row.findAll("a")
                if len(data) == 5:
                    dic = {}
                    dic["Name"] = re.sub("&", "and", re.sub(r"\s+", " ", data[1].text.strip().replace("\n","").replace("\t"," ")))
                    if dic["Name"] != "":
                        for x in links:
                            if re.match(r"%s\d*/.*" % letter, x["href"], re.I):
                                entry_thread_list.append([x, dic, gender, letter, index])
                                index += 1
                                break
                    else:
                        print(f"DIDN'T PASS NAME CHECK" + dic["Name"])

            # Execute the calls to the single_entry method using the entry_thread_list
            with cf.ThreadPoolExecutor(max_workers=workers) as executor : 
                executor.map(single_entry, entry_thread_list)

def single_entry(components):
    '''
    Method used in multithreading to make computations for a single entry.\n
    The given components list contains : [link, murderer dictionary, gender, letter, index].\n
    '''
    x, dic, gender, l, index = components
    base_url = "http://murderpedia.org/" + gender + "." + l+"/"
    dic["Murderpedia_URL"] = base_url + x["href"]
    dic["Base_URL"] = base_url
    try:
        add_to_global_tree(*process_murderer(gender, l, dic, index))
        print("DONE", dic["Name"])
    except:
        print("COULDN'T DO", dic["Name"], dic["Murderpedia_URL"])