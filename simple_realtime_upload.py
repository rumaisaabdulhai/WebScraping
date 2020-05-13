###########
# IMPORTS #
###########
from firebase import firebase
import json
import os

'''
Simple Upload to Real-Time Firebase (Currently Using)

Note: Does not account for duplicates yet.
'''

# Helpful Documentation:
# https://ozgur.github.io/python-firebase/

opp_app = firebase.FirebaseApplication('https://findmyopportunities-31222.firebaseio.com/', None)
f = open(os.path.dirname(os.path.realpath(__file__)) + '/Datasets/Opportunities_Small.json',)

# Publish Opportunities to Firebase
for opportunity in json.load(f):
    result = opp_app.post('/Opportunities', opportunity)