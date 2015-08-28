"""
This module acquires configuration data for the login and passwd utils.
"""
import json
import hashlib
from microauth.client import Client

CONFIG_FILE    = "/etc/login.conf"
PASSWD_FILE    = "/etc/passwd"
ORIGINAL_LOGIN = "/bin/login"

config = {
    "server":               "https://localhost:7789/v1/",
    "apikey":               "",
    "use_remote_settings":  0,       # switch to true to attempt to use a config served by the server
    "permit_root_logon":    0,       # don't handle authenticating as the superuser
    "create_accounts":      1,       # create accounts for successful users?
    "defer_to_original":    1,       # should we use the original program if the server is unavailable?
    "allow_groups":         ["shell"],
}

class Script(object):
    """
    Represents the execution environment for a third-party script.
    We send custom values into the environment and work with whatever's left.
    Scripts can also call any methods on objects put in their environment.
    """
    def __init__(self, file=None, env={}):
        self.read_on_exec = True
        self.file = file
        self.env = env
        self.script = ''
        self.code = None
        self.hash = None
        self.cache = {
        }

    def execute(self, env={}):
        if not self.code or self.read_on_exec: self.compile()
        if env: self.env = env
        self.env['cache'] = self.cache
        exec self.code in self.env
        del self.env['__builtins__']
        if 'cache' in self.env.keys():
            self.cache = self.env['cache']
        return (self.env)

    def compile(self, script=''):
        if self.file:
            f = file(self.file, 'r')
            self.script = f.read()
            f.close()
        elif script:
            self.script = script
        if self.script:
            hash = sha1sum(self.script)
            if self.hash != hash:
                self.hash = hash
                self.code = compile(self.script, '<string>', 'exec')
            self.script = ''

    def __getitem__(self, key):
        if key in self.env.keys():
            return (self.env[key])
        else:
            raise (KeyError(key))

	def keys(self):
		return self.env.keys()

def acquire_configuration():

	# CONFIG file should return a dictionary named config
	# it permits you to determine values programatically
	config_program = Script(CONFIG_FILE)
	config_program.execute()
	config = config_program['config']
	
	if 'use_remote_settings' in config and config['use_remote_settings']:
		client = Client(config['key'], config['server'])
		(remote_config, status_code) = client.get("config")
		if status_code == 200:
			for key, value in remote_config.items():
				if key in ['apikey', 'server']:
					continue
				config[key] = value

	return config

def sha1sum(s):
	return hashlib.sha1(s).hexdigest()
