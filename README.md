# Microauth-Login
### A replacement UNIX login package

Allows you to log into a host by authenticating against a Microauth instance.

#### Installation
<pre>
sudo python setup.py install
</pre>

#### Removal
Extra care has been taken to restore systems to their prior state upon
uninstallation.
<pre>
sudo python setup.py uninstall
</pre>

Put this thing in the base image of containers or VM images and you can
centrally manage access. Like a minimal LDAP for nimble operations.

The /etc/login.conf is also an executable python script that returns a configuration
object, meaning values can be determined by heliocentric planetary positions or 
the Zipf coefficient of a scanned genome for example.
