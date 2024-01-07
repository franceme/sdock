import os,sys,argparse
from datetime import datetime
from abc import ABC, abstractmethod

def datetime_valid(dt_str):
	try:
		datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
	except:
		return False
	return True

def parse():
	parser = argparse.ArgumentParser(description='lls')
	parser.add_argument(
		'-b', '--boxname',
		type=lambda x:(
			isinstance(x,str)
			and
			x.strip() != ''
		),
		help='The Vagrant boxname'
	)
	parser.add_argument(
		'-d', '--date', 
		type=lambda x:(
			isinstance(x,datetime)
			or
			datetime_valid(x)
		),
		help='The date the box should run as'
	)
	parser.add_argument(
		'-p', '--provider',
		type=lambda x:(
			x.lower() == "VBox".lower()
			or
			x.lower() == "VirtualBox".lower()
		),
		help='The provider to be use'
	)
	parser.add_argument(
		'-n', '--network',
		action='store_true',
		default=False,
		help='Whether there should be a network or no'
	)
	parser.add_argument(
		'-i', '--install',
		action='store_true',
		default=False,
		help='Whether to install everything before start'
	)
	parser.add_argument(
		'-u', '--uninstall',
		action='store_true',
		default=False,
		help='Whether to uninstall everything after exit'
	)
	return parser

def cmds(args*):
	if len(args == 1):
		os.system(args[0])
#elif:

class vagrant(object):
	def __init__(self):
		super().__init__()
		self.name = None
		self.provider = None

	def __cmd(self, cmd:str):
		os.system("vagrant {0}".format(cmd))

	def install(self):
		self.__cmd("wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg")
		self.__cmd("""-echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com jammy main" | sudo tee /etc/apt/sources.list.d/hashicorp.list""")
		self.__cmd("apt update")
		self.__cmd("apt install vagrant -y")

	def uninstall(self):
		os.system("yes|rm -rf /opt/vagrant")
		os.system("yes|rm -f /usr/bin/vagrant")

	def set_name(self, string):
		self.name = string

	def set_provider(self, provider:Provider):
		self.provider=provider

	def on(self):
		with open("Vagrantfile", "w+") as writer:
			writer.write("""# -*- mode: ruby -*- 
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "{0}"
  config.vm.define "win10" do |win10| 
	win10.vm.box = "talisker/windows10pro" 
	#win10.vm.provision :shell, :inline => "python -m pip install hugg"
{1}
  end
end
""".format(self.name, self.provider.vagrant_string()))
		self.__cmd("up")

	def off(self):
		#self.__cmd("halt")
		self.__cmd("off")


class Provider(ABC):
	@abstractmethod
	def install(self):
		pass

	@abstractmethod
	def uninstall(self):
		pass

	@abstractmethod
	def set_name(self, string):
		pass

	@abstractmethod
	def set_date(self, string):
		pass

	@abstractmethod
	def disable_network(self):
		pass

	@abstractmethod
	def disable_timesync(self):
		pass

class virtualbox(Provider):
	def __init__(self):
		super().__init__()
		self.name = None

	def __cmd(self, cmd:str):
		os.system("VBoxManage {0}".format(cmd))

	def install(self):
		return

	def uninstall(self):
		return

	def set_name(self, string):
		self.name = string

	def vagrant_string(self):
		return """
win10.vm.provider :virtualbox do |vb|
	vb.name = "{0}"
	vb.gui = true
end
""".format(self.name)

	def on(self):
		self.__cmd("startvm {0}".format(self.name))

	def off(self):
		self.__cmd("controlvm {0} acpipowerbutton".format(self.name))
		self.__cmd("controlvm {0} poweroff".format(self.name))

	def delete(self):
		self.__cmd("unregistervm --delete {0}".format(self.name))

	def disable_timesync(self):
		self.__cmd("setextradata {0} VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1".format(self.name))

	def set_date(self, datetime_value:datetime.datetime):
		self.__cmd("modifyvm {0} --biossystemtimeoffset {1}".format(self.name, 
			str((datetime_value - datetime.datetime.now()).total_seconds())
		))

	def disable_network(self):
		self.__cmd("modifyvm {0} --nic1 null".format(self.name))
		self.__cmd("modifyvm {0} --cableconnected1 off".format(self.name))

def main(args):
	start = None
	"""
name=tempbox
vag=sudo vagrant
vb=sudo VBoxManage
breather=10

default:: cycle

install: #https://developer.hashicorp.com/vagrant/downloads
	#-wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
	#-echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com jammy main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
	-sudo apt update
	-sudo apt install vagrant


uninstall: #https://developer.hashicorp.com/vagrant/docs/installation/uninstallation
	-rm -rf /opt/vagrant
	-rm -f /usr/bin/vagrant

cycle: proc #down up

proc: down
	$(vag) up
	
	$(vb) controlvm $(name) poweroff #acpipowerbutton
	#$(vag) halt
	sleep $(breather)
	
	@make disable

	#$(vag) up
	$(vb) startvm $(name)

disable:
	$(vb) modifyvm $(name) --biossystemtimeoffset -31536000000
	$(vb) setextradata $(name) VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1
	#$(vb) modifyvm $(name) --nic1 null
	$(vb) modifyvm $(name) --cableconnected1 off

rup:
	$(vag) resume 
up:
	$(vag) up

full: up
	$(vag) halt

down:
	-$(vag) destroy -f
cache:
	$(vag) global-status --prune

delete:
	VBoxManage unregistervm --delete "$$name"
	"""


if __init__ == '__main__':
	main(parse())
