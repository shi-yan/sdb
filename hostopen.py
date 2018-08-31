import gdb
import re
import subprocess

username = 'shiy' # your host machine's username
hostip = '10.0.0.1' # your host machine's ip
editor = 'subl' # your text editor
password = 'xxxx' # host machine password
sshpass = 'sshpass' # path for sshpass

class HostOpen (gdb.Command):
	def __init__ (self):
		super (HostOpen, self).__init__ ("ho", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True)

	def invoke (self, arg, from_tty):
		print ("HostOpen")
		frame = gdb.execute("info f " + arg, to_string=True)
		pattern = re.compile("\((/.+:[0-9]+)\);", re.MULTILINE)
		match = pattern.findall(frame)
		print("match!", match[0])
		filename = match[0]
		subprocess.call(sshpass + " -p "+password+" ssh "+username+"@"+hostip+" \"DISPLAY=:0 nohup "+editor+" "+filename+"\"", shell=True)

HostOpen ()


