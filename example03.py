# import the JSON Library
import json

# open and read the file
with open("jsample.json")as f:
    jsample = f.read()

# print the json data
print(jsample)

# convert to a python dictionary
jdict = json.loads(jsample)

# create a variable from the data
jvar = jdict[0]['model']
print (jvar)

# Edit the data
jdict[0]['name'] = 'lab AP'

#revert back to a json string
print(json.dumps(jdict))
