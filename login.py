#!/usr/bin/env python
"""
This program defines a drop-in replacement for the UNIX login package
 for use with container systems to authenticate to a single microauth
instance.

Luke Brooks 2015
"""
import pty
import socket
import getpass
import logging
from microauth.client import Client
from microauth_login.defaults import config
CONFIG_FILE = "/etc/login.conf"

def prompt_for_login():
	username       = ""
	password       = ""
	reading_stdin  = 1

	while reading_stdin:
		try:
			username = raw_input("%s login: " % socket.gethostname())
			if not username: continue
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

	try:
		(resp, status) = uAuth.post('users/%s/login' % username, {"password":password})
	except:
		# Defer to the original login program is configured to do so

		print "Authentication server currently unavailable."
		return None

	if status == 200: return True
	return False

def log_attempt(success, username):
	pass

def acquire_configuration(config):
	# 1) Read the local configuration at CONFIG_FILE.
	# 2) if use_remote_settings enabled, consult the authentication server.
	config['apikey'] = ""
	return config

if __name__ == "__main__":
	success = None
	while success == None:
		config = acquire_configuration(config)
		(username, password) = prompt_for_login()
		success = authenticate(username, password)
	log_attempt(success, username)
	print username
	print password
