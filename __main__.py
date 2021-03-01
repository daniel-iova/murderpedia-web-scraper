# CC BY 4.0
# © 2021 Daniel Iova

from get_data import process_all_murderers
from dict_operations import global_dataset, compile_general_model, clean_data, count_murderers
import json

def main():

    ### Define base filenames for the dataset and the general model
    dataset_filename = "dataset.json"
    model_filename = "model.json"
    count_filename = "count.txt"

    max_workers = 8

    ## Process all murderers and save the data to the global_dataset variable
    process_all_murderers(max_workers)

    ### clean the dataset and dump it into a new file
    dataset = clean_data(global_dataset)
    json.dump(dataset, open(f"{dataset_filename}", "w"))

    ### Compile the general model and dump it to file
    compile_general_model(dataset, f"{model_filename}")

    ### Count entries in the final dataset
    count_murderers(f"{dataset_filename}", count_filename)

if __name__ == "__main__":
    main()
