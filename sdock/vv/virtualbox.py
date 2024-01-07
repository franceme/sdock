import datetime
import os,sys,Provider


class app(Provider):
	def __init__(self, set_to_datetime_value:datetime.datetime=None, set_disable_timesync:bool=False, set_disable_network:bool=False):
		super().__init__()
		self.name = None
		self.set_to_datetime_value=set_to_datetime_value
		self.set_disable_timesync=set_disable_timesync
		self.set_disable_network=set_disable_network

	def __cmd(self, cmd:str):
		os.system("VBoxManage {0}".format(cmd))

	def install(self):
		return

	def uninstall(self):
		return

	def vagrant_string(self):
		return """
win10.vm.provider :virtualbox do |vb|
	vb.name = "{0}"
	vb.gui = true
end
""".format(self.name)

	def prep(self):
		with self.inverse():
			if self.set_to_datetime_value is not None:
				self.set_date(self.set_to_datetime_value)

			if self.set_disable_timesync:
				self.disable_timesync()

			if self.set_disable_network:
				self.disable_network()


	def on(self):
		self.__cmd("startvm {0}".format(self.name))

	def off(self):
		#self.__cmd("controlvm {0} acpipowerbutton".format(self.name))
		self.__cmd("controlvm {0} poweroff".format(self.name))

	def delete(self):
		self.__cmd("unregistervm --delete {0}".format(self.name))

	def disable_timesync(self):
		self.__cmd("setextradata {0} VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1".format(self.name))

	def set_date(self, datetime_value:datetime.datetime=None):
		datetime_value = datetime_value or self.set_to_datetime_value
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