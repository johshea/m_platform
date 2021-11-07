#this script is a prototype, and very specific. As always it should be executed on aproduction env only after thourough testing.
#This script functions as a way to validate an org or networks current firmware state.
#the dashboard
##########################################################
# Prep your environment
#Environment with Python3 installed
#pip3 install requests
#
##########################################################
#
# -k <your api key> [MANDATORY]
# -o <your org name> [MANDATORY]
# -n <specific network name> [optional (not case sensitive)]
#
# usage python3 main.py -k <api key> -o <specific org name> -n <network name>
######################################################################################################



import requests
import datetime
import sys, getopt, csv

def rem_whitespace(string):
    return string.split()


def get_networks(orgid):
    # create iterable list of all networks and then create filtered categories
    net_response = requests.request("GET", f'{m_baseUrl}/organizations/{orgid}/networks/', headers=m_headers)
    if 'json' in net_response.headers.get('Content-Type'):
        # print(networks)
        return net_response.json()
    else:
        print('Response content is not in JSON format.')
        sys.exit(0)


def create_df(networkid, networkname):
    device_req = requests.get(f'{m_baseUrl}/networks/{networkid}/devices', headers=m_headers)
    try:
        if 'json' in device_req.headers.get('Content-Type'):
            devices = device_req.json()

            #create an empty list to store dictionary objects
            device_data = []

            # populate the data storage object
            for device in devices:
               device_data_df = {'Name': networkname, 'model': device['model'], 'Serial': device['serial'], 'MAC': device['mac'], 'Firmware': device['firmware']}
               device_data.append(device_data_df)

               #print(device_data_df) #test dataset

            #Create and write the CSV file
            if len(device_data) > 0:
                keys = device_data[0].keys()
                filename = networkname + '_devices-' + str(time) + '.csv'
                inpath = Path.cwd() / filename
                print(inpath)
                with inpath.open(mode='w+', newline='') as output_file:
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(device_data)

        return ("Firmware Report For" + " " + networkname + " " + "Created")

    except:
        return("A null or blank value was found in one of the collected fields for" + " " + networkname )

def main(argv):
    global arg_apikey
    global m_baseUrl
    global orgid
    global m_headers
    global m_baseUrl
    global time

    arg_apikey = None
    arg_orgname = None
    arg_netname = None

    try:
        opts, args = getopt.getopt(argv, 'k:o:n:')
    except getopt.GetoptError:
        sys.exit(0)

    for opt, arg in opts:
        if opt == '-k':
            arg_apikey = arg
        elif opt == '-o':
            arg_orgname = arg
        elif opt == '-n':
            arg_netname = arg


    #print(arg_apikey) #test point for correct apikey
    #print(arg_orgname) #test point for correct orgname
    #print(arg_netname) #test print for correct network name


    if arg_apikey is None or arg_orgname is None:
        print('Please specify the required values!')
        sys.exit(0)


    # set needed vlaues from env_vars
    m_headers = {'X-Cisco-Meraki-API-Key': arg_apikey}
    m_baseUrl = 'https://api.meraki.com/api/v1'

    d = datetime.datetime.now()
    time = d.date()

    # get orgid for specified org name
    org_response = requests.request("GET", f'{m_baseUrl}/organizations/', headers=m_headers)
    org = org_response.json()
    for row in org:
        if row['name'] == arg_orgname:
            orgid = row['id']
            #print(orgid)
            print("Org" + " " + row['name'] + " " + "found.")
        else:
            print("Exception: This Org does not match:" + ' ' + row['name'] + ' ' + 'Is not the orginization specified!')

    # create iterable list of all networks and then create filtered categories
    networks = get_networks(orgid)


    if arg_netname != None:
        network_found = False
        for i in range(len(networks)):
            if networks[i]['name'].lower() == arg_netname.lower():
                print("Creating Report for Meraki Network" + " " + networks[i]['id'])
                state = create_df(networks[i]['id'], networks[i]['name'])
                print(state)
                network_found = True

        if not network_found:
            print(arg_netname + " " + "Could not be found!")
            sys.exit(0)

    elif arg_netname == None:
        for i in range(len(networks)):
            if networks[i]['productTypes'] != ['systemsManager']:
                print("Creating Report for Meraki Network" + " " + networks[i]['id'])
                create_df(networks[i]['id'], networks[i]['name'])
                state = create_df(networks[i]['id'], networks[i]['name'])
                print(state)


    print("I am Done. Have a nice day!")
if __name__ == '__main__':
    main(sys.argv[1:])