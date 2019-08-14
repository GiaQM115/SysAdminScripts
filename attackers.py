import sys
import csv
import re
from geoip import geolite2 as gl

# lists for ip address of failed logins, and corresponding number of failed logins per ip
ips = []
attempts = []

# just checking the usage
if len(sys.argv) != 2:
	print("USAGE: python attackers.py log_file")
	exit(1)

# a filename was provided, try to open the file
# if it doesn't open, return an error message and exit with exit code 1
fp = str(sys.argv[1])
try:
	with open(fp) as f:
		# parse the file line by line
		for line in f:
			# if this line is a failed login attempt
			if "failed password" in line.lower():
				# find the ip address
				ipaddr = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',line).group()
				# if this address has been found already, increment the attempts value at the same location
				if ipaddr in ips:
					i = ips.index(ipaddr)
					attempts[i] += 1
				else:
					# append the ip to the ips list, append 1 to the same location in attempts
					ips.append(ipaddr)
					attempts.append(1)
	f.close()
except Exception as e:
	print("cannot open log file: " + fp)
	exit(1)

# use a DictWriter to allow us to add column headers
writer = csv.DictWriter(open('attackers.csv','w'), ['Attempts','IP Address'])
writer.writerow({'Attempts':'Attempts','IP Address':'IP Address'})
for i in range(0,len(ips)):
	# only look at attempts higher than 10
	if attempts[i] > 10:
		# write to the file
		writer.writerow({'Attempts': str(attempts[i]), 'IP Address': str(ips[i])})
# we done, yo
