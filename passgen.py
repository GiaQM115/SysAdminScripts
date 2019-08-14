import random

specialchars = ['!','@','#','$','%','^','&','(',')','~','+','=','_','-','?','/',':',';','.',',','{','}','[',']']

# function to change the character in string p at index n to a random digit
def change_char(n, p):
	newch = random.randint(0,9)
	if n == 0:
		p = str(newch) + p[1:]
	if n == length-1:
		p = p[0:n] + str(newch)
	else:
		p = p[0:n] + str(newch) + p[n+1:]
	return p

# function to change the character in string p at index n to a random capital letter
def capital_char(n, p):
	newch = random.randint(65,90)
	if n == 0:
		p = chr(newch) + p[1:]
	if n == length-1:
		p = p[0:n] + chr(newch)
	else:
		p = p[0:n] + chr(newch) + p[n+1:]
	return p
# function to change the character in string p at index n to a random special character
def special(n, p):
	newch = random.randint(0,len(specialchars))
	newch = specialchars[newch]
	if n == 0:
		p = newch + p[1:]
	if n == length-1:
		p = p[0:n] + newch
	else:
		p = p[0:n] + newch + p[n+1:]
	return p

# main function: utilized random integers and the above functions to make a random password
def create_passwd():
	changed = list()
	passwd = ""
	# make sure at least 1 character remains a lowercase letter
	changed.append(random.randint(0,length-1))

	# create a string of all lowercase letters with correct length
	for i in range(0,length):
		ch = random.randint(97,121)
		passwd = passwd + chr(ch)

	# change 1-3 characters into numbers
	# the section before the forloop ensures at least 1 character is changed to a number
	index = random.randint(0,length-1)
	while index in changed:
		index = random.randint(0,length-1)
	changed.append(index)
	passwd = change_char(index, passwd)
	for i in range(0,2):
		# some probability to keep it fresh (;
		r = random.randint(1,100)
		if(r % 2 == 0 or r % 3 == 0):
			# find an index we are allowed to change
			while index in changed:
				index = random.randint(0,length-1)
			# change the character
			passwd = change_char(index, passwd)
	# capitalize insert 2-4 characters
	# make sure at least 2 get changed and make sure they stay capitalized
	for i in range(0,2):
		index = random.randint(0,length-1)
		while index in changed:
			index = random.randint(0,length-1)
		changed.append(index)
		passwd = capital_char(index, passwd)
	for i in range(0,2):
		# some probability to keep it fresh (;
		r = random.randint(1,100)
		if(r % 5 == 0 or r % 2 == 0):
			# find an index we are allowed to change
			while index in changed:
				index = random.randint(0,length-1)
			# change the character
			passwd = capital_char(index, passwd)	
	# insert 1 or 2 special characters
	index = random.randint(0,length-1)
	while index in changed:
		index = random.randint(0,length-1)
	changed.append(index)
	passwd = special(index, passwd)
	for i in range(0,2):
		# some probability to keep it fresh (;
		r = random.randint(1,100)
		if(r % 3 == 0):
			# find an index we are allowed to change
			while index in changed:
				index = random.randint(0,length-1)
			# change the character
			passwd = special(index, passwd)
	print("PASSWORD: " + passwd + "\nIf this is acceptable, type 'exit'\nFor a new " + str(length) + " character password, hit enter\nFor a new password of a different length, type exit and restart the utility")


# allow the user to choose a password length
# if the users input is not 8 or 12, prompt again for a valid length
length = int(input("8 or 12 character password? "))
while length != 8 and length != 12:
	length = int(input(str(length) +" is an invalid size\n8 or 12 characters? "))
# try to make a password
create_passwd()
# if the user is happy with the password, exit
# else, make a new one
while input().lower() != 'exit':
	create_passwd()
exit()
