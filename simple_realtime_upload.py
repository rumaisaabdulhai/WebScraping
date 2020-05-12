from firebase import firebase
import json
import os

'''
Simple Upload to Real-Time Firebase (No Authentication Yet)
'''

# Helpful Documentation:
# https://ozgur.github.io/python-firebase/

# Does not account for duplicates yet.
opp_app = firebase.FirebaseApplication('https://findmyopportunities-31222.firebaseio.com/', None)
f = open(os.path.dirname(os.path.realpath(__file__)) + '/Datasets/Opportunities.json',)

for opportunity in json.load(f):
    result = opp_app.post('/Opportunities', opportunity)