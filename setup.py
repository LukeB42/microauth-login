#!/usr/bin/env python
import sys

def main():
	if len(sys.argv) < 2:
		print "Optional arguments are: install, uninstall, sdist, bdist"
		raise SystemExit

	# print banner

def install():
	# install deps and module

	# move original passwd

	# copy passwd.py as setuid

	# move original login program

	# move login.py to /bin/microauth_login
	# symlink /bin/login 

	pass

def uninstall():
	# remove module and scripts

	# move original passwd

	# move original login program

	pass

if __name__ == "__main__":
	main()
