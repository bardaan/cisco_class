#!/usr/bin/env python

import sys
import getpass
import requests
import os
import json

def create_ospf_config():
	true = 1    																	
	while true:
		try:
			true = 0
			inp = raw_input('Enter File Name to get the details from: ')
			user_file = open(inp).read()
			ospf_dict = json.loads(user_file)
			device = ospf_dict['device_list']['device']
			for each in device:
				url='http://' + device[each]['mgmt_ip'] + '/ins'
				switchuser='admin'
				switchpassword='cisco'
				myheaders={'content-type':'application/json'}
				payload1={
				  	"ins_api": {
					    "version": "1.0",
					    "type": "cli_conf",
					    "chunk": "0",
					    "sid": "1",
					    "input": "config t ;feature ospf ;router ospf " + device[each]['ospf_process_id'] + " ;router-id " + device[each]['ospf_router_id'] + " ;exit ;",
					    "output_format": "json"
					}
				}
								
				requests.post(url,data=json.dumps(payload1), headers=myheaders,auth=(switchuser,switchpassword)).json()
				
				for key in device[each]['intf_details']:
					intf = device[each]['intf_details'][key]
					if intf['name'].__contains__('Eth')  or intf['name'].__contains__('eth') or intf['name'].__contains__('ETH'):
						switchport = 'no switchport ;'
					else:
						switchport = ''
					payload2={
					  	"ins_api": {
						    "version": "1.0",
						    "type": "cli_conf",
						    "chunk": "0",
						    "sid": "1",
						    "input": "interface " + intf['name'] + " ;no shut ;" + switchport + "description " + intf['description'] + " ;ip address " + intf['ip_prefix'] + " ;ip router ospf " + device[each]['ospf_process_id'] + " area " + intf['ospf_area'] + " ;exit ;",
						    "output_format": "json"
						}
					}
					
					requests.post(url,data=json.dumps(payload2), headers=myheaders,auth=(switchuser,switchpassword)).json()
				print ('\n\n\n')
		except IOError:
			print ("\nPlease enter a valid file name.\n")
			print ("You may also press CTRL+C to exit.\n")
			true = 1
		except KeyboardInterrupt:
			sys.exit()


def user_input():

	true = 1  												 	##Keeps track of the while loop
	retry = 0   													##Keeps track of invalid input entered by the user

	while true:
		os.system('clear')
		true = 0
		print ('	1. Enter filename where the details have been populated')
		print ('	2. See sample file with details for manually populating/creating the details prior to above option')
		print ('	3. About This Program')
		print ('	4. Exit')
		
		if retry > 5:
				print ('\n\n\nPlease Select a Valid Option???\n\n\n')

		try:
			inp = int(raw_input('\n\n\n			Select Option:  '))
		except ValueError:
			retry += 1
			true = 1
			continue
			
		os.system('clear')
		if inp not in range(1,5):
			true = 1
			retry += 1
		elif inp == 4:
			sys.exit()
		elif inp == 1:
			create_ospf_config()
			print ('Your Configuration has been pushed into the device(s) successfully!!!') 
		elif inp == 2:
			sample_file = open("sample.json").read()
			print (sample_file)
			print ('\n\n\nPress any key to go back to previous menu') 
			raw_input()
			os.system('clear')
			true = 1
		elif inp == 3:
			print ('This program configures the interfaces and runs OSPF in your network.')
			print ('You may populate a json file with the details and provide the filename. Everything will be configured accordingly.')
			print ('You can check the sample json file for creating the details manually in the main menu')
			print ('\n\n\nPress any key to go back\n\n\n')
			raw_input()
			os.system('clear')
			true = 1


user_input()
