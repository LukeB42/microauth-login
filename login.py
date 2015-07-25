#!/usr/bin/env python
"""
This program defines a drop-in replacement for the UNIX login package,
for systems to authenticate to a single microauth instance.

Luke Brooks 2015
"""
import os
import pwd
import pty
import socket
import _curses
import getpass
import logging
import subprocess
from microauth.client import Client
from microauth_login.config import acquire_configuration
CONFIG_FILE = "/etc/login.conf"
PASSWD_FILE = "/etc/passwd"

DEBUG = True
def log(message):
	if DEBUG:
		import pprint
		p = pprint.PrettyPrinter()
		p = p.pprint
		if type(message) in [list, dict]:
			print "DEBUG: "
			p(message)
		else:
			print "DEBUG: " + str(message)

def read_passwd():
	result = {}
	fd     = open(PASSWD_FILE)
	file   = fd.read()
	fd.close()
	for line in file.split('\n'):
		if not line: continue
		line = line.split(':',1)
		result[ line[0] ] = line[1].split(':')
	return result

def prompt_for_login():
	username       = ""
	password       = ""
	reading_stdin  = 1

	while reading_stdin:
		try:
			username = raw_input("%s login: " % socket.gethostname())
			if not username: continue
			if DEBUG and username == "EXIT":
				raise SystemExit
			password = getpass.getpass()
			if username and password:
				reading_stdin = 0
		except EOFError:
			print "^D"
		except KeyboardInterrupt:
			print

	return (username, password)

def authenticate(username, password):
	uAuth = Client(config['apikey'], config['server'], verify=False)

	# Check user groups with server.
	try:
		(resp, status) = uAuth.get('users/%s' % username)
	except:
		if "defer_to_original" in config and config["defer_to_original"]:
			run_default_login_program()

		print "Authentication server currently unavailable."
		return

	if status != 200:
		log("%s user %s" % (str(status), username))
		return

	# Allow/deny based on allow_groups and deny_groups lists.
	# Obtain users groups/roles.
	user_groups = []
	if "roles" in resp:
		user_groups = resp['roles']
	elif "groups" in resp:
		user_groups = resp['groups']

	priority = None
	if "priority" in config:
		priority = config['priority']

	allowed = False
	if "allow_groups" in config:
		for group in config['allow_groups']:
			if group in user_groups:
				log("%s found in allow group." % username)
				allowed = True
	else:
		log("No allow groups configured.")
		return

	denied = False
	if "deny_groups" in config:
		for group in config['deny_groups']:
			if group in user_groups:
				log("%s found in deny group." % username)
				denied = True
	else:
		log("No deny groups configured.")

	if priority and allowed and denied:
		log('Priority "%s"' % priority)
		if priority == "deny":
			return
	elif denied == True or allowed == False:
		log("Denied:  " + str(denied))
		log("Allowed: " + str(allowed))
		return

	# Perform the actual authentication.
	# It is in this section that you would want to upload data from
	# hardware peripherals to make use of key-based authentication.
	try:
		(resp, status) = uAuth.post('users/%s/login' % username, {"password":password})
	except:
		# Defer to the original login program is configured to do so
		if "defer_to_original" in config and config["defer_to_original"]:
			run_default_login_program()

		print "Authentication server currently unavailable."
		return

	if status == 200:
		return(1)
	return

def log_attempt(success, username):
	pass


def create_account(username):
	log("Creating account for %s." % username)

def check_user_exists(username):
	try:
		pwd.getpwnam(username)
	except KeyError:
		if 'create_accounts' in config and config['create_accounts']:
			create_account(username)

def run_default_login_program():
	pass	

def spawn_shell(username):
	"""
	Detach from the controlling terminal, change UID to that of username
	and spawn a shell in their home directory.
	"""

	passwd_file = read_passwd()

	if not username in passwd_file:
		log("Account not found.")
		return False
	user     = passwd_file[username]
	uid      = user[1]
	gid      = user[2]
	home_dir = user[4]
	shell    = user[5]

	log("Defining environment.")
	os.environ["HOME"]  = home_dir
	os.environ["USER"]  = username
	os.environ["SHELL"] = shell

	screen = _curses.initscr()
	terminal_width  = screen.getmaxyx()[1]
	_curses.endwin()
	
	os.environ['COLUMNS'] = str(terminal_width)

	if not "TERM" in os.environ:
		os.environ["TERM"]  = "dumb"


	log("Changing UID")
	os.setgid(int(gid))
	os.setuid(int(uid))

	log("Moving into %s" % home_dir)
	os.chdir(home_dir)

	log("Detaching from TTY")

	log("Spawning shell.")
	pty.spawn(shell)
	if os.path.isfile("/usr/bin/clear"):
		os.system('clear')
	return True

if __name__ == "__main__":
	if os.getuid():
		print "login: Cannot possibly work without effective root"
		raise SystemExit

	# The main loops that first keep asking for input on stdin and
	# then check if the users shell can be spawned in their home directory.

	user_home_dir_exists = False
	while user_home_dir_exists == False:

		success = None
		while success == None:
			# Overlay some sensible defaults with whatever's in CONFIG_FILE
			# and possibly poll our remote microauth instance for settings.
			config               = acquire_configuration(CONFIG_FILE)
			# Read STDIN in an infinite loop. Ignore all signals.
			(username, password) = prompt_for_login()
			# Send the data over to microauth.
			success              = authenticate(username, password)

		# Write to utmp and syslog so the incident is available to lastlog et al.
		log_attempt(success, username)
		# Verify the account exists locally. Possibly create it if configured to.
		user_home_dir_exists = check_user_exists(username)

	spawn_shell(username)
