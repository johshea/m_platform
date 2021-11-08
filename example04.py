# import the YMAL data
import yaml

# open and read the file
with open("ysample.yaml")as f:
   ysample = f.read()
# print the yaml data
print(ysample)
# convert to a python dictionary
ydict = yaml.safe_load(ysample)
# create a variable from the data
yvar = ydict['device-1']['ip_address']
print(yvar)
# Edit the data
ydict['device-1']['device_name'] = 'lab mx'
#revert back to a json string
print(yaml.dump(ydict))
