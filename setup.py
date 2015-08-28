#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import os
import sys
import shutil
from setuptools import setup, find_packages

banner = """
██████╗ ███████╗██╗   ██╗██████╗ ███████╗██████╗ ███╗   ██╗███████╗████████╗██╗ ██████╗███████╗   
██╔══██╗██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝██║██╔════╝██╔════╝   
██████╔╝███████╗ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██╔██╗ ██║█████╗     ██║   ██║██║     ███████╗   
██╔═══╝ ╚════██║  ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║╚██╗██║██╔══╝     ██║   ██║██║     ╚════██║   
██║     ███████║   ██║   ██████╔╝███████╗██║  ██║██║ ╚████║███████╗   ██║   ██║╚██████╗███████║██╗
╚═╝     ╚══════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝╚══════╝╚═╝
"""

def main():
	if len(sys.argv) < 2:
		print "Optional arguments are: install, uninstall, sdist, bdist"
		raise SystemExit

	if sys.argv[1] == "install":
		install()

	if sys.argv[1] == "uninstall":
		uninstall()

def install():
	print banner
	# install deps and module
	data_files = ()
	setup(name='microauth_login',
		version="0.0.3",
		description='A drop-in replacement for the *nix login package.',
		author='Luke Brooks',
		author_email='luke@psybernetics.org',
		url='http://psybernetics.org.uk/microauth',
		download_url = 'https://github.com/LukeB42/microauth-login/tarball/0.0.3',
		data_files = data_files,
		packages=['microauth_login'],
		include_package_data=True,
		install_requires=[
			"setproctitle",
			"microauth",
		],
		keywords=["authentication", "login", "microservices"]
	)

	print "Installing login.conf to /etc/login.conf"
	shutil.copyfile("login.conf","/etc/login.conf")

	# move original passwd

	# copy passwd.py as setuid

	# move original login program
	print "Moving /bin/login to /bin/original_login"
	shutil.move("/bin/login", "/bin/original_login")

	# move login.py to /bin/microauth_login
	print "Moving login.py to /bin/microauth_login"
	shutil.copyfile("login.py","/bin/microauth_login")

	# symlink /bin/login 
	print "Symlinking /bin/microauth_login to /bin/login"
	os.symlink("/bin/microauth_login", "/bin/login")

	# chmod /bin/login
	print "Making /bin/login executable."
	os.chmod("/bin/login", 0755)

	print "Remember to add an API key to /etc/login.conf at the minimum."


def uninstall():
	if not os.path.islink("/bin/login"):
		print "The program at /bin/login doesn't appear to be a link to Microauth-Login."
		raise SystemExit

	# remove module and config
	if os.path.exists("/etc/login.conf"):
		print "Removing /etc/login.conf"
		os.unlink("/etc/login.conf")

	# move original passwd
	
	# move original login program

	print "Removing symlink to microauth-login."
	os.remove("/bin/login")

	print "Moving original login back into place."
	shutil.move("/bin/original_login", "/bin/login")

if __name__ == "__main__":
	main()
