##################################################################################################
#Prototype
#A Meraki API Call to populate and maintain network objects using a JSON dictionary as source
#
#Requirments:
#Python3 and the requests library
#to install requests:
#pip3 install requests
#
#Usage:
#python3 main.py -k <apikey> -o <orgname>
#
#Future:
#Error handling on data iteration
#move record creation to a function
#check if exists and update instead of add
#build in creating and assigning to group objects
###################################################################################################



import requests
import json, sys, getopt


def getorgId(arg_orgname):
    org_response = requests.request("GET", f'{m_baseUrl}/organizations/', headers=m_headers)
    org = org_response.json()
    for row in org:
        if row['name'] == arg_orgname:
            orgid = row['id']
            print("Org" + " " + row['name'] + " " + "found.")
        else:
            print("Exception: This Org does not match:" + ' ' + row['name'] + ' ' + 'Is not the orginization specified!')

    return orgid


def main(argv):
    global arg_apikey
    global m_baseUrl
    global m_headers
    global arg_orgname

    arg_apikey = None
    arg_orgname = None

    try:
        opts, args = getopt.getopt(argv, 'k:o:')
    except getopt.GetoptError:
        sys.exit(0)

    for opt, arg in opts:
        if opt == '-k':
            arg_apikey = arg
        elif opt == '-o':
            arg_orgname = arg

    if arg_apikey is None or arg_orgname is None:
        print('Please specify the required values!')
        sys.exit(0)

    # set needed vlaues from env_vars
    m_headers = {'X-Cisco-Meraki-API-Key': arg_apikey}
    m_baseUrl = 'https://api.meraki.com/api/v1'

    orgid = getorgId(arg_orgname)

    f = open('policyobj.json',)
    objects = json.load(f)

    for i in objects['policy_objects']:
        payload = {
            "name": i['name'],
            "category": i['category'],
            "type": i['type'],
            "cidr": i['cidr']
        }
        print(payload)
        print ('Adding' + ' ' + i['name'])
        create_obj = requests.request("post", f'{m_baseUrl}/organizations/{orgid}/policyObjects', headers=m_headers, data=payload)
        print(create_obj)
        if create_obj.status_code == 201:
            print('Object Added!')
        else:
            print('Something weht wrong adding' + ' ' + i['name'])

    print('Policy Objects added! Have a great day!')

if __name__ == '__main__':
    main(sys.argv[1:])


