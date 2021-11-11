#DISCLAIMER: Please note: This script is meant for demo purposes only. All tools/
# #scripts in this repo are released for use "AS IS" without any warranties of any kind,
# #including, but not limited to their installation, use, or performance. Any use of
#these scripts and tools is at your own risk. There is no guarantee that they have
# #been through thorough testing in a comparable environment and we are not responsible
# #for any damage or data loss incurred with their use. You are responsible for
# #reviewing and testing any scripts you run thoroughly before use in any non-testing
# #environment.

# usage python3 main.py -k <api key> -o <specific org name> -f filetype


import meraki
import sys, csv, json
from pathlib import Path
import datetime
import time



def main(argv):

    def get_org(arg_orgname):
        org_response = dashboard.organizations.getOrganizations()
        for org in org_response:
            if org['name'].lower() == arg_orgname.lower():
                orgid = org['id']
                # print(orgid)
                print("Org" + " " + orgid + " " + "found.")
                return(orgid)

            else:
                print("No Org found")
                sys.exit(0)

    def get_networks(orgid):
        networks = dashboard.organizations.getOrganizationNetworks(orgid, total_pages='all')
        return(networks)

    #Function for creating output as CSV
    def output_csv(data, flag, filename, net_name):
        # Create and write the CSV file (Windows, linux, macos)
        if len(data) > 0:
            keys = data[0].keys()
            Path(flag).mkdir(parents=True, exist_ok=True)
            inpath = Path.cwd() / flag / filename
            # print(inpath)
            with inpath.open(mode='w+', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
        return ('success')

    #Function for creating output as json
    def output_json(data, flag, filename, netname):
        if len(data) > 0:
            Path(flag).mkdir(parents=True, exist_ok=True)
            inpath = Path.cwd() / flag / filename
            with inpath.open('w') as jsonFile:
                json.dump(data, jsonFile, indent=4, sort_keys=True)
        return ('success')



    arg_apikey = input("Please enter your Meraki API Key: ")
    if arg_apikey != '':
        API_KEY = arg_apikey
        dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

    arg_orgname = input("Please enter your Organization name: ")
    #resolve the org name to an ID
    if arg_orgname.lower() != '':
        orgid = get_org(arg_orgname)
        networks = get_networks(orgid)

    print("**Report Options**")
    print("client_data")
    print('firmware')
    print('all')
    arg_report = input("Please select a report from the options (default all): ")
    if arg_report == '':
        arg_report = 'all'
    print("**Format**")
    print("json")
    print("csv")
    arg_filetype = input("Please enter a format (default json): ")
    if arg_filetype == '':
        arg_filetype = 'json'



    #set and format the time object
    timenow = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    ####Start Client Data Report ####

    if arg_report.lower() == 'client_data' or arg_report.lower() == 'all':
        # Build the Client Data Report
        # for each network retrieve the client list
        for i in range(0, len(networks)):
            if networks[i]['productTypes'] != ['systemsManager']:
                #print(i) # debug network response

                # Build the Client data into a nested dictionary
                clients = dashboard.networks.getNetworkClients(networks[i]['id'], total_pages='all')
                # print(clients) # debug clients

                try:
                    client_data = []
                    # print(clients)

                    # populate the data storage object
                    for client in clients:
                        # print(client)
                        client_data_df = {'ID': client['id'], 'Description': client['description'],
                                          'MAC': client['mac'],
                                          'User': client['user'], 'IP': client['ip'], 'VLAN': client['vlan'],
                                          'manufacturer': client['manufacturer'],
                                          'OS': client['os']}

                        client_data.append(client_data_df)

                        # Set Variables and send to the CSV report function
                        data = client_data
                        flag = 'client_data'
                        filename = networks[i]['name'] + '_clients-' + str(timenow) + '.' + arg_filetype
                        net_name = networks[i]['name']

                        if arg_filetype == 'csv' and len(client_data) > 0:
                            output = output_csv(data, flag, filename, net_name)
                        elif arg_filetype == 'json':
                            output = output_json(data, flag, filename, net_name)


                    if output == 'success':
                        print("Client Report For" + " " + networks[i]['name'] + " " + "Created in /Client_data")
                    else:
                        print("Client Report For" + " " + networks[i]['name'] + " " + "failed")
                        print("Are there clients in this network?")

                except Exception as e:
                    print(e)



    if arg_report.lower() == 'all':
        time.sleep(10) #pause for writes to complete

    #### Start Firmware Report ####

    if arg_report.lower() == 'firmware' or arg_report.lower() == 'all':
        #Build Firmware Reports
        print("***Creating Firmware Reports***")
        for i in range(len(networks)):
            if networks[i]['productTypes'] != ['systemsManager']:

                try:
                    # create an empty list to store dictionary objects
                    firmware_data = []
                    devices = dashboard.networks.getNetworkDevices(networks[i]['id'])

                    # populate the data storage object
                    for device in devices:
                        firmware_data_df = {'Name': networks[i]['name'], 'model': device['model'], 'Serial': device['serial'],
                                    'MAC': device['mac'], 'Firmware': device['firmware']}

                        firmware_data.append(firmware_data_df)

                        #print(firmware_data_df) #test dataset

                     # Set Variables and send to the CSV report function
                        data = firmware_data
                        flag = 'firmware_data'
                        filename = networks[i]['name'] + '_firmware-' + str(timenow) + '.' + arg_filetype
                        net_name = networks[i]['name']

                        if arg_filetype == 'csv':
                            output = output_csv(data, flag, filename, net_name)
                        elif arg_filetype == 'json':
                            output = output_json(data, flag, filename, net_name)

                    if output == 'success':
                        print("Firmware Report For" + " " + networks[i]['name'] + " " + "Created in /firmware")
                    else:
                        print("Firmware Report For" + " " + networks[i]['name'] + " " + "failed")

                except Exception as e:
                    print(e)

        if arg_report.lower() == 'all':
            time.sleep(10) #pause for writes to complete

    print("All Done. Have a nice day!")

    #### Start Change Report here ####
    #if
        #for

            #try

            #except Exception as e:
                #print(e)


if __name__ == '__main__':
    main(sys.argv[1:])
