#!/usr/bin/python
import socket
import re
import subprocess
import os

remoteip = "8.8.8.8"
hostname = "www.yahoo.com"
connection = True

os.system('clear')
print('-' * 25)
print "***Beginning Test***\n1\n2\n3\n4\n5\n"

try:
	ipr = subprocess.check_output('ip route | grep default', shell=True)
except:
	connection = False	

# get default gateway
if(connection):
	searchobj = re.search(r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})', ipr)
	gateway = searchobj.group()
	print("Your default gateway is " + gateway + "\n")

	# ping the gateway
	if(os.system('ping -c 1 ' + gateway + ' > /dev/null 2>/dev/null')):
		print "Gateway Connection FAILED\n"
	else:
		print "Gateway Connection SUCCEEDED\n"
else:
	print "No gateway to test\n"

# ping the remote address
if(os.system('ping -c 1 ' + remoteip + ' > /dev/null 2>/dev/null')):
	print "Remote Connection FAILED\n"
else:
	print "Remote Connection SUCCEEDED\n" 

# ping the url to test DNS
if(os.system('ping -c 1 ' + hostname + ' > /dev/null 2>/dev/null')):
	print "DNS Resolution FAILED\n"
else:
	print "DNS Resolution SUCCEEDED\n" 

print "***End Test***"
print('-' * 25)