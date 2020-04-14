import csv, json, os

'''
Converts CSV file to json and saves it.
'''

# Variables
dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory path
folder = '/Datasets/' # relative path of desired folder
csv_file = 'Dataset.csv' # csv file name
json_name = 'Opportunities.json' # json file name to create

def csv_to_json(csv_path, json_path):
    '''
    Converts a CSV file to json.
    '''

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(json_path, 'w') as f:
        json.dump(rows, f, indent=2)

def main():
    '''
    Runs the json to csv method.
    '''
    csv_path = dir_path + folder + csv_file
    json_path = dir_path + folder + json_name
    csv_to_json(csv_path, json_path)

if __name__ == '__main__':
    main()