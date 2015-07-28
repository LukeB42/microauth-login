#!/usr/bin/env python
import sys

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

	print banner


def install():
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
