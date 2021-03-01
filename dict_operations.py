# CC BY 4.0
# © 2021 Daniel Iova

from collections import defaultdict
import json
import re

def name_to_key(name, index):
    return re.sub(r"[^\w]", "", name) + f"_{index}"


global_dataset = defaultdict(lambda: defaultdict(dict))

def add_to_global_tree(gender, letter, dic, index):
    '''
    Adds an entry to the global_dataset tree using the given parameters.
    '''
    global_dataset[gender][letter][name_to_key(dic["Name"], index)] = dic

def compile_general_model(dataset, model_filename):
    '''
    Receives a dataset and a model filename.\n
    Compiles and dumps to a json file a dictionary with :
        - keys : Keys that appear in the dataset
        - values : Number of occurances for each key\n
    '''
    occurances = {}
    for gender in dataset.keys():
        for letter in dataset[gender].keys():
            for murderer in dataset[gender][letter].keys():
                for key in dataset[gender][letter][murderer].keys():
                    if key not in occurances.keys():
                        occurances[key] = 1
                    else:
                         occurances[key] += 1

    json.dump(dict(sorted(occurances.items(), key= lambda x : x[1], reverse=True)), open(model_filename, "w"))

def clean_data(dataset):
    '''
    Cleans the given dataset of entries that did not have any data scraped from their own page.
    '''
    for g in list(dataset.keys()):
        for l in list(dataset[g].keys()):
            for m in list(dataset[g][l].keys()):
                if len(dataset[g][l][m]) <= 5:
                    del dataset[g][l][m]
    return dataset

def count_children(dic):
    count = 0
    for key in dic.keys():
        count += len(dic[key])
    return count

def count_murderers(dataset_filename, count_filename):
    '''
    Counts the number of entries in the dataset loaded using the given filename.
    '''
    outf = open(count_filename, "w")
    data = json.load(open(dataset_filename))
    male_count, female_count = 0, 0
    if "female" in data.keys():
        female_count = count_children(data["female"])
    if "male" in data.keys():
        male_count = count_children(data["male"])
    print (f"{male_count} Males and {female_count} Females.", file = outf)
    print (f"In total {male_count+female_count} out of 6921 total entries.", file = outf)
    print (f"{6921 - (male_count+female_count)} murderers not scraped.", file = outf)