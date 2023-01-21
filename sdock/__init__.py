import os, sys, requests, time
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

def wget(url, verify=True):
	to = url.split('/')[-1].replace('%20','_')
	if not os.path.exists(to):
		resp = requests.get(url, allow_redirects=True,verify=verify)
		open(to,'wb').write(resp.content)
	return to

def open_port():
	"""
	https://gist.github.com/jdavis/4040223
	"""

	import socket

	sock = socket.socket()
	sock.bind(('', 0))
	x, port = sock.getsockname()
	sock.close()

	return port

def checkPort(port):
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = bool(sock.connect_ex(('127.0.0.1', int(port))))
	sock.close()
	return result

def getPort(ports=[], prefix="-p"):
	if ports is None or ports == []:
		return ''
	return ' '.join([
		f"{prefix} {port if checkPort(port) else open_port()}:{port}" for port in ports
	])

def exe(string):
	global exe_logs
	with open("logs.txt","a+") as writer:
		writer.write("{0}\n".format(string))
	print(string)
	os.system(string)

@dataclass
class dock:
	"""Class for keeping track of an item in inventory."""
	docker: str = "docker"
	image: str = "frantzme/pythondev:lite"
	ports: list = field(default_factory=list)
	cmd: str = None
	nocmd: bool = False
	nonet: bool = False
	dind: bool = False
	shared: bool = False
	detach: bool = False
	sudo: bool = False
	remove: bool = True
	mountto: str = "/sync"
	mountfrom: str = None
	name: str = "current_running"
	login: bool = False
	loggout: bool = False
	logg: bool = False
	macaddress: str = None
	postClean: bool = False
	preClean: bool = False
	extra: str = None

	def clean(self):
		return "; ".join([
			"{} kill $({} ps -a -q)".format(self.docker, self.docker),
			"{} kill $({} ps -q)".format(self.docker, self.docker),
			"{} rm $({} ps -a -q)".format(self.docker, self.docker),
			"{} rmi $({} images -q)".format(self.docker, self.docker),
			"{} volume rm $({} volume ls -q)".format(self.docker, self.docker),
			"{} image prune -f".format(self.docker),
			"{} container prune -f".format(self.docker),
			"{} builder prune -f -a".format(self.docker)
		])

	def string(self):
		if self.dind or self.shared:
			import platform
			if False and platform.system().lower() == "darwin":  # Mac
				dockerInDocker = "--privileged=true -v /private/var/run/docker.sock:/var/run/docker.sock"
			else:  # if platform.system().lower() == "linux":
				dockerInDocker = "--privileged=true -v /var/run/docker.sock:/var/run/docker.sock"
		else:
			dockerInDocker = ""

		if self.shared:
			exchanged = "-e EXCHANGE_PATH=" + os.path.abspath(os.curdir)
		else:
			exchanged = ""

		dir = '%cd%' if sys.platform in ['win32', 'cygwin'] else '`pwd`'
		use_dir = "$EXCHANGE_PATH" if self.shared else (self.mountfrom if self.mountfrom else dir)

		if self.nocmd:
			cmd = ''
		else:
			cmd = self.cmd or '/bin/bash'

		network = ""
		if self.nonet:
			network = "--network none" #https://docs.docker.com/network/none/

		return str(self.clean()+";" if self.preClean else "") + "{0} run ".format(self.docker) + " ".join([
			dockerInDocker,
			'--rm' if self.remove else '',
			'-d' if self.detach else '-it',
			'-v "{0}:{1}"'.format(use_dir, self.mountto),
			exchanged,
			network,
			getPort(self.ports),
			'--mac-address ' + str(self.macaddress) if self.macaddress else '',
			self.extra if self.extra else '',
			self.image,
			cmd
		]) + str(self.clean()+";" if self.postClean else "")

	def __str__(self):
		return self.string()

@dataclass
class vagrant(vb):
	"""
	box = sdock.vagrant(
		vagrant_base="talisker/windows10pro",
		vmdate = datetime.date(2022, 12, 25),
		uploadfiles = [sdock.wget(x,False) for x in [
			'https://cdn.sw.altova.com/v2023sp1/en/MissionKitEnt2023sp1.exe',
			'https://cdn.sw.altova.com/v2023sp1/en/MissionKitEnt2023sp1.zip',
			'https://staruml.io/download/releases-v5/StarUML%20Setup%205.0.2.exe',
			'https://sparxsystems.com/bin/easetup_x64.msi',
			'https://cytranet.dl.sourceforge.net/project/dia-installer/diashapes/0.3.0/diashapes-setup-0.3.0.exe'
		]],
		choco_packages = ["jdk8"],
		python_packages = ["hugg"],
		vb_path="/Users/maister/VirtualBox VMs/",
		headless=False
	)
	"""
	vagrant_base:str = "talisker/windows10pro",
	disablehosttime: bool = True,
	vmdate: str = None,
	cpu: int = 2,
	ram: int = 4096,
	uploadfiles: list = None,
	choco_packages:list =  None,
	python_packages:list =  None,
	scripts_to_run:str =  None,
	vb_path: str = None,
	vb_box_exe: str = "VBoxManage"
	headless: bool = True

	def __post_init__(self):

		if self.uploadfiles is None or type(self.uploadfiles) is tuple:
			self.uploadfiles = []

		if self.choco_packages is None or type(self.choco_packages) is tuple:
			self.choco_packages = []

		if self.python_packages is None or type(self.python_packages) is tuple:
			self.python_packages = []

		if self.scripts_to_run is None or type(self.scripts_to_run) is tuple:
			self.scripts_to_run = []


	@property
	def vagrant_name(self):
		if not self.vb_path:
			return

		vag_name = None

		folder_name = os.path.basename(os.path.abspath(os.curdir))
		for item in os.listdir(self.vb_path):
			if not os.path.isfile(item) and folder_name in item:
				vag_name = item.split('/')[-1].strip()

		return vag_name

	def prep(self):
		if self.vmdate:
			diff_days = (self.vmdate - datetime.now().date()).days
			self.scripts_to_run += [
				"Set-Date -Date (Get-Date).AddDays({0})".format(diff_days)
			]

		
		uploading_file_strings = []
		for foil in self.uploadfiles:
			uploading_file_strings += [
				""" win10.vm.provision "file", source: "{0}", destination: "C:\\\\Users\\\\vagrant\\\\Desktop\\\\{0}" """.format(foil)
			]
		
		scripts = []
		for script in self.scripts_to_run:
			if script:
				scripts += [
					"""win10.vm.provision "shell", inline: <<-SHELL
{0}
SHELL""".format(script)
				]
		
		if self.python_packages != []:
			self.choco_packages += [
				"python38"
			]

		if self.choco_packages:
			choco_script = """win10.vm.provision "shell", inline: <<-SHELL
[Net.ServicePointManager]::SecurityProtocol = "tls12, tls11, tls"
iex (wget 'https://chocolatey.org/install.ps1' -UseBasicParsing)
"""

			for choco_package in set(self.choco_packages):
				choco_script += """choco install -y {0} \n""".format(choco_package)	
			
			choco_script += """
SHELL"""

			scripts += [choco_script]

		if self.python_packages != []:
			scripts += [
				""" win10.vm.provision :shell, :inline => "python -m pip install --upgrade pip {0} " """.format(" ".join(self.python_packages))
			]

		virtualbox_scripts = [
			"vb.gui = {0}".format("false" if self.headless else "true")
		]

		if self.disablehosttime:
			virtualbox_scripts += [
				"""vb.customize [ "guestproperty", "set", :id, "/VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled", 1 ] """
			]

		if len(virtualbox_scripts) > 0:
			virtualbox_scripting = """
config.vm.provider 'virtualbox' do |vb|
{0}
end
""".format("\n".join(virtualbox_scripts))

		contents = """# -*- mode: ruby -*- 
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
	config.vm.define "win10" do |win10| 
    	win10.vm.box = "{0}"
		{1}
		{2}
		{3}
	end
end
""".format(
	self.vagrant_base,
	"\n".join(uploading_file_strings),
	"\n".join(scripts),
	virtualbox_scripting
)
		with open("Vagrantfile", "w+") as vagrantfile:
			vagrantfile.write(contents)

	def on(self):
		exe(""" vagrant up""")

	def off(self):
		self.vagrant_name
		exe("{0} controlvm {1} poweroff".format(self.vb_box_exe, self.vagrant_name))
	
	def destroy(self):
		self.vagrant_name
		exe(""" vagrant destroy -f """)
		exe("rm Vagrantfile")
		exe("yes|rm -r .vagrant/")
		for foil in self.uploadfiles:
			exe("rm {0}".format(foil))