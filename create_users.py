import sys
import csv
import subprocess
import re

gunames = []

#helper function for bash commands
def sh(script):
	out = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = out.communicate()
	if stderr:
		print("\n\n---ERROR---\n" + stderr + "\n-----------\n\n")
	return stdout.decode('utf-8')


# makes sure the correct data is inserted in each column
# isNumeric is a boolean value defining whether or not the data SHOULD be numeric or not
# returns an error message if data is incorrect
def check_data(data, isNumeric):
	# does the data exist?
	if not data:
		return False
	# is the data the right format?
	if data[0].isdigit() != isNumeric:
		return False
	return True


# checks for all currently created groups
# if group doesn't exist, creates group
def check_for_group(groupname):
	if groupname not in sh(['cut', '-d:', '-f1', '/etc/group']):
		print("CREATING GROUP " + groupname)
		sh(['groupadd', groupname])

# concatenates username, ensures uniqueness of username
def create_username(firstname, lastname, eid):
	nt = firstname[0].lower() + lastname.lower()
	n = re.sub(r'[^a-z]?',"",nt)
	i = 0
	while n in gunames:
		n += eid[i]
		i += 1
	gunames.append(n)
	return n


# attempts to create and add user
# username is first inital and last name [+ #'s if necessary]
# passwd must be changed by user at login
# home dir is /home/department/username
def try_add(firstname, lastname, username, homedir, group, passwd):
	name = firstname + " " + lastname
	try:
		sh(['useradd', '-g', group, '-m', '-d', homedir, '-p', passwd, '-c', name, username])
		sh(['passwd', '-e', username])
		return True
	except:
		return False



# populate gunames with current users on system
gunames = (sh(['cut', '-d:', '-f1', '/etc/passwd']))[:-2].split("\\n")
# open file, parse info, add users
try:
	f = str(sys.argv[1]) 
except:
	print("Usage: python create_users.py user_info_file.csv")
	exit(1)

with open(f) as userinfo:
	cr = csv.DictReader(userinfo);
	for u in cr:
		print("\n\n")
		# check the firstname, lastname, groupname, department name, employee ID
		if not check_data(u['FirstName'], False):
			print("ERROR CREATING USER FROM DATA:\n\tEmployee ID: ", u['EmployeeID'])
			continue
		if not check_data(u['LastName'], False):	
			print("ERROR CREATING USER FROM DATA:\n\tEmployee ID: ", u['EmployeeID'])
			continue
		if not check_data(u['Group'], False):
			print("ERROR CREATING USER FROM DATA:\n\tEmployee ID: ", u['EmployeeID'])
			continue
		if not check_data(u['Department'], False):
			print("ERROR CREATING USER FROM DATA:\n\tEmployee ID: ", u['EmployeeID'])
			continue
		if not check_data(u['EmployeeID'], True): 
			print("ERROR CREATING USER FROM DATA:\n\tEmployee ID: ", u['EmployeeID'])
			continue
		
		# create a unique username
		uname = create_username(u['FirstName'], u['LastName'], u['EmployeeID'])
		print("ADDING USER " + uname)

		# create group if necessary
		check_for_group(u['Group'])
		print("GROUP " + u['Group'] + " OK")

		# try to create the user
		hdir = "/home/" + u['Department'].lower() + "/"
		print("HOME DIRECTORY FOR " + uname + " IS " + hdir + uname)
		if not try_add(u['FirstName'], u['LastName'], uname, hdir, u['Group'], uname[::-1]):
			print("ERROR CREATING USER FROM DATA:\n\tEmployee ID:  ", u['EmployeeID'])
			continue
