###########
# IMPORTS #
###########
import csv
import os
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

# Code belongs to:
# Source: https://medium.com/@cbrannen/importing-data-into-firestore-using-python-dce2d6d3cd51

'''
Not currently using Code. Will consider if 
doing Cloud Database instead of RealTime Database.
'''

dir_path = os.path.dirname(os.path.realpath(__file__))
rel_path = '/Datasets/'
file_name = 'Dataset.csv'

cred = credentials.Certificate(dir_path + "/ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()

file_path = dir_path + rel_path + file_name
collection_name = "Opportunities"

def batch_data(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

data = []
headers = []
with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            for header in row:
                headers.append(header)
            line_count += 1
        else:
            obj = {}
            for idx, item in enumerate(row):
                obj[headers[idx]] = item
            data.append(obj)
            line_count += 1
    print(f'Processed {line_count} lines.')

for batched_data in batch_data(data, 499):
    batch = store.batch()
    for data_item in batched_data:
        doc_ref = store.collection(collection_name).document()
        batch.set(doc_ref, data_item)
    batch.commit()

print('Done')