from datetime import datetime
from dataclasses import dataclass, field
import os,sys
from . import Provider

#https://github.com/pycontribs/python-vagrant/blob/main/src/vagrant/__init__.py#L202
#https://github.com/pycontribs/python-vagrant/tree/main

try:
	import vagrant as og_vagrant
	import mystring

	@dataclass
	class app(og_vagrant.Vagrant): #ogvag.Vagrant #
		"""Help Info
# The contents of the Makefile that made it work
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

# How this works with the file
#!/usr/bin/env python3
import os,sys
from importlib.metadata import version
from datetime import datetime

try:
	if version('sdock') < '0.1.73':
		raise Exception("Upgrade the version")
except:
	os.system("{0} -m pip install --upgrade sdock".format(sys.executable))
from sdock.vv import *

#Choco Packages: https://community.chocolatey.org/packages

box_name = "tempbox"
box = vagrant.app(
	box="talisker/windows10pro",
	name=box_name,
	provider=virtualbox.app(),
	disablehosttime = True,
	disablenetwork = True,
	vmdate = datetime(year=2023, month=1, day=10, hour=3, minute=0, second=0),
	python_packages = ["hugg"],
)

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Vagrant Runner for {0}".format(box_name))
	parser.add_argument("--start", help="Start the box",action='store_true',default=False)
	parser.add_argument("--stop", help="Stop the box",action='store_true',default=False)
	parser.add_argument("--clean", help="Clean the box",action='store_true',default=False)
	#parser.add_argument("--save", help="Save the progress with the box",action='store_true',default=False)
	#parser.add_argument("--load", help="Load the progress with the box",action='store_true',default=False)
	args,unknown = parser.parse_known_args()
	return args

args = getArgs()
if args.start:
	box.on()
elif args.stop:
	box.off()
elif args.clean:
	box.clean()
		"""
		name:str
		provider:Provider
		box:str="talisker/windows10pro"
		install:bool=False
		uninstall:bool=False
		remove:bool=False
		disablehosttime:bool = True
		disablenetwork:bool = True
		vmdate:datetime.datetime = None
		cpu:int = 2
		ram:int = 4096
		uploadfiles:str = []
		choco_packages:str = []
		python_packages:str = []
		scripts_to_run:str = []
		vagrant_exe:str = "vagrant"
		vb_box_exe:str = "VBoxManage"
		headless:bool = False
		hidden_status:str=og_vagrant.Status(
			name="N/A", state="uninstantiated", provider="N/A"
		)
		save_files:str = []
		_date_diff:str = None

		def __post_init__(self):
			if self.provider is None or self.provider.raw_name != "virtualbox":
				raise Exception("Vagrant only supports virtualbox at this time")

			if self.provider:
				self.provider.name = self.name
				self.provider.set_exe(self.exe)

			self.hidden_status=self.set_status("uninstantiated")
			super().__init__()

		def exe(self, cmd:str):
			mystring.string("{0} {1}".format(self.vagrant_exe, cmd)).exec()

		def install(self):
			self.exe("wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg")
			self.exe("""-echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com jammy main" | sudo tee /etc/apt/sources.list.d/hashicorp.list""")
			self.exe("apt update")
			self.exe("apt install vagrant -y")
			if self.provider:
				self.provider.install()

		def uninstall(self):
			self.exe("yes|rm -rf /opt/vagrant")
			self.exe("yes|rm -f /usr/bin/vagrant")
			if self.provider:
				self.provider.uninstall()

		def snapshot_take(self, snapshotname):
			# https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
			self.exe("{0} snapshot {1} take {2}".format(self.vb_box_exe, self.name, snapshotname))

		def snapshot_load(self, snapshotname):
			# https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
			self.exe("{0} snapshot {1} restore {2}".format(self.vb_box_exe, self.name, snapshotname))

		def snapshot_list(self):
			# https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
			self.exe("{0} snapshot {1} list".format(self.vb_box_exe, self.name))

		def snapshot_delete(self, snapshotname):
			# https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
			self.exe("{0} snapshot {1} delete {2}".format(self.vb_box_exe, self.name, snapshotname))

		def export_to_ova(self, ovaname):
			# https://www.techrepublic.com/article/how-to-import-and-export-virtualbox-appliances-from-the-command-line/
			# https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html
			self.exe("{0} snapshot {1} export {2} --ovf10 --options manifest,iso,nomacs -o {3}".format(self.vb_box_exe, self.name,ovaname))

		def create_runner(self):
			foil = "on_login.cmd"
			# https://jd-bots.com/2021/05/15/how-to-run-powershell-script-on-windows-startup/
			# https://stackoverflow.com/questions/20575257/how-do-i-run-a-powershell-script-when-the-computer-starts
			with open(foil, "w+") as writer:
				writer.write("""powershell -windowstyle hidden C:\\\\Users\\\\vagrant\\\\Desktop\\\\on_start.ps1""")
			self.uploadfiles += [foil]
			return foil

		def shell_wrap(self, *contents):
			if len(contents) == 1:
				return """win10.vm.provision :shell, :inline => "{0}" """.format(contents[0])
			else:
				return """win10.vm.provision "shell", inline: <<-SHELL\n{0}\nSHELL""".format("\n".join(contents))

		def choco_packages(self):
			return shell_wrap(
				"""[Net.ServicePointManager]::SecurityProtocol = "tls12, tls11, tls" """,
				"""iex (wget 'https://chocolatey.org/install.ps1' -UseBasicParsing)""",
				*[
					"choco install -y {0}".format(x) for x in self.choco_packages
				]
			)

		@property
		def diff(self):
			if self._date_diff is None:
				self._date_diff = (self.vmdate - datetime.now().date())
			return self._date_diff

		@property
		def diff_days():
			return self.diff.days

		@property
		def diff_ms():
			return round(self.diff.total_seconds() * 1000)

		def add_file_to_box(self, foil, directory="C:\\\\Users\\\\vagrant\\\\Desktop"):
			return """ win10.vm.provision "file", source: "{0}", destination: "{1}\\\\{0}" """.format(foil, directory)

		def on_start_file(self, contents=[]):
			foil = "on_start.ps1"
			"""Potential Contents
Set-Date -Date (Get-Date).AddDays()
Disable-NetAdapter -Name "*" -Confirm:$false 
			"""
			with open(foil, "w+") as writer:
				writer.write("""
{0}
""".format("\n".join(contents)))
			self.uploadfiles += [foil]
			return foil

		def write_vagrant_file(self):
			foil = "Vagrantfile"

			shell_scripts = []
			if len(self.python_packages) > 0:
				self.choco_packages += ["python3.8"]
				shell_scripts += [
					shell_wrap("C:\\\\Python38\\\\python -m pip install --upgrade pip {0} ".format(" ".join(self.python_packages)))
				]

			with open(foil, "w+") as writer:
				writer.write("""# -*- mode: ruby -*- 
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
	config.vm.box = "{name}"
	config.vm.define "win10" do |win10| 
		win10.vm.box = "{box}"
{choco_script}
{shell_scripts}
	end
end
""".format(
	name=self.name,
	box=self.box,
	shell_scripts="\n		".join(shell_scripts)),
	choco_script=self.choco_packages()
)
			return foil

		def status():
			if self.hidden_status is None:
				return super.status()
			return self.hidden_status
		
		def set_status(state=None):
			if state is None:
				self.hidden_status = None
			else:
				self.hidden_status = og_vagrant.Status(name=self.name, state=state, provider=self.provider.raw_name)

		def clean(self):
			self.destroy()

		def off(self):
			self.halt(force=True)

		def on(self):
			self.set_status("started-enstantiating")
			if not os.path.exists("Vagrantfile"):
				self.write_vagrant_file()
			self.set_status()

			self.up()
			last_status = self.status()

			self.set_status("provider-manipulation")
			with self.provider.inverse():
				self.set_status("provider-manipulation-started")

				if self.vmdate is not None:
					self.provider.set_date(self.vmdate)
					self.set_status("vm-date-set")

				if self.disablehosttime:
					self.provider.disable_timesync()
					self.set_status("time-sync-disabled")

				if self.disablenetwork:
					self.provider.disable_network()
					self.set_status("network-disabled")

			self.set_status("provider-manipulation-completed")
			self.set_status(None)
	
		def __enter__(self):
			return self

		def __exit__(self, a=None, b=None, c=None):
			for foil in list(self.uploadfiles):
				os.remove(foil)
			self.clean()
			os.remove("Vagrantfile")
			self.exe("yes|rm -r .vagrant/")


except Exception as e:
	print("Exception: {0}".format(e))
	pass