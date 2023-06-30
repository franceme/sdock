import os, sys, requests, time, subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

def cmd(cmd,display=True, lines=False):
	output_contents = ""
	if display:
		print(cmd)
	process = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,bufsize=1,encoding='utf-8', universal_newlines=True, close_fds=True)
	while True:
		out = process.stdout.readline()
		if out == '' and process.poll() != None:
			break
		if out != '':
			if display:
				sys.stdout.write(out)
			output_contents += out
			sys.stdout.flush()
	if not lines:
		return output_contents
	return [x for x in output_contents.split('\n') if x.strip() != '']

def wget(url, verify=True):
	to = url.split('/')[-1].replace('%20','_')
	if not os.path.exists(to):
		resp = requests.get(url, allow_redirects=True,verify=verify)
		open(to,'wb').write(resp.content)
	return to

def extract_file_from_zip(local_zipfile, extractedfile):
	import zipfile

	if not os.path.exists(extractedfile):
		cur_folder = os.path.abspath(os.curdir)
		with zipfile.ZipFile(local_zipfile,"r") as zip_ref:
			zip_ref.extractall(cur_folder)
		os.remove(local_zipfile)

	return extractedfile if os.path.exists(extractedfile) else None

def extract_ova_from_zip(local_zipfile):
	if False:
		import zipfile

		ovafile = os.path.basename(local_zipfile).replace('.zip','.ova')
		if not os.path.exists(ovafile):
			cur_folder = os.path.abspath(os.curdir)
			with zipfile.ZipFile(local_zipfile,"r") as zip_ref:
				zip_ref.extractall(cur_folder)
			os.remove(local_zipfile)

		return ovafile if os.path.exists(ovafile) else None
	else:
		return extract_file_from_zip(local_zipfile, os.path.basename(local_zipfile).replace('.zip','.ova'))

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

def getPort(ports=[], prefix="-p",dup=True):
	if ports is None or ports == []:
		return ''
	if not isinstance(ports, list):
		ports = [ports]
	if prefix is None:
		prefix = ''
	if dup:
		return ' '.join([
			f"{prefix} {port if checkPort(port) else open_port()}:{port}" for port in ports
		])
	else: #Created a flag to support the direct usage of the port instead of linking it to the original port
		return ' '.join([
			f"{prefix} {port if checkPort(port) else open_port()}" for port in ports
		])

def exe(string):
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
	save_host_dir: bool = False

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

		my_save_host_dir = ''
		if self.save_host_dir:
			if 'HOSTDIR' in os.environ:
				past_dir,current_dir = os.environ['HOSTDIR'], os.path.abspath(os.curdir).replace('/sync/','')
				my_save_host_dir = '--env="HOSTDIR={0}/{1}"'.format(past_dir,current_dir)
			else:
				my_save_host_dir = '--env="HOSTDIR={0}"'.format(dir)

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
			my_save_host_dir,
			self.image,
			cmd
		]) + str(self.clean()+";" if self.postClean else "")

	def __str__(self):
		return self.string()

@dataclass
class vb:
	"""Class for keeping track of an item in inventory."""
	vmname: str = "takenname"
	username: str = None
	ovafile: str = None
	disablehosttime: bool = True
	disablenetwork: bool = True
	biosoffset: str = None
	vmdate: str = None
	network: bool = False
	cpu: int = 2
	ram: int = 4096
	sharedfolder: str = None
	uploadfiles:list = field(default_factory=list)
	vboxmanage: str = "VBoxManage"
	vb_path: str = None
	headless: bool = True
	#cmds_to_exe_with_network:list = field(default_factory=list)
	#cmds_to_exe_without_network:list = field(default_factory=list)

	def on(self,headless:bool=True):
		cmd = "{0} startvm {1}".format(self.vboxmanage,self.vmname)
		if self.headless:
			cmd += " --type headless"

		exe(cmd)

	def vbexe(self, cmd):
		string = "{0} guestcontrol {1} run ".format(self.vboxmanage, self.vmname)
		
		if self.username:
			string += " --username {0} ".format(self.username)

		string += str(" --exe \"C:\\Windows\\System32\\cmd.exe\" -- cmd.exe/arg0 /C '" + cmd.replace("'","\'") + "'")
		exe(string)

	def snapshot_take(self,snapshotname):
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		exe("{0} snapshot {1} take {2}".format(self.vboxmanage,self.vmname, snapshotname))

	def snapshot_load(self,snapshotname):
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		exe("{0} snapshot {1} restore {2}".format(self.vboxmanage,self.vmname, snapshotname))

	def snapshot_list(self):
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		exe("{0} snapshot {1} list".format(self.vboxmanage,self.vmname))

	def snapshot_delete(self,snapshotname):
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		exe("{0} snapshot {1} delete {2}".format(self.vboxmanage,self.vmname, snapshotname))

	def export_to_ova(self,ovaname):
		#https://www.techrepublic.com/article/how-to-import-and-export-virtualbox-appliances-from-the-command-line/
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html
		exe("{0} export {1} --ovf10 --options manifest,iso,nomacs -o {2}".format(self.vboxmanage,self.vmname, ovaname))

	def __shared_folder(self, folder):
		exe("{0}  sharedfolder add {1} --name \"{1}_SharedFolder\" --hostpath \"{2}\" --automount".format(self.vboxmanage, self.vmname, folder))

	def add_snapshot_folder(self, snapshot_folder):
		if False:
			import datetime, uuid
			from copy import deepcopy as dc
			from pathlib import Path
			import sdock.vbgen as vb_struct

			#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-showvminfo.html
			#VBoxManage showvminfo <X> --machinereadable

			machine_info = cmd(
				"{0} showvminfo {1} --machinereadable".format(self.vboxmanage, self.vmname), lines=True
			)
			config_file = None
			for machine_info_line in machine_info:
				machine_info_line = machine_info_line.strip()
				if machine_info_line.startswith("CfgFile"):
					print(machine_info_line)
					config_file = machine_info_line.replace("CfgFile=",'').replace('"','').strip()

			parser = XmlParser()
			og_config = parser.from_path(Path(config_file), vb_struct.VirtualBox)
			
			#Fix the VMDK Potential
			save_files,vdi_file = [],None
			vmdk_files = []
			for filename in os.scandir(snapshot_folder):
				if os.path.isfile(filename.path):
					if filename.name.endswith('.sav'):
						save_files += [filename.path]
					if filename.name.endswith('.vdi'):
						vdi_file = filename.path
					if filename.name.endswith('.vmdk'):
						vmdk_files += [filename.path]
				print(filename.name)
			print(vdi_file)

			"""
			VDI located in StorageControllers-attachedDevice-Image (uuid):> {06509f60-d51f-4ce4-97ed-f83cff79d93e}
			Also located in Machine -> MediaRegistry -> HardDisks -> HardDisk
			"""

			#https://www.tutorialspoint.com/How-to-sort-a-Python-date-string-list
			save_files.sort(key=lambda date: datetime.datetime.strptime('-'.join(date.replace('Snapshots/','').replace('.sav','').split("-")[:-1]), "%Y-%m-%dT%H-%M-%S"))

			copy_hardware=dc(og_config.machine.hardware)
			#save_files.reverse()
			ini_snapshot = vb_struct.Snapshot(
					uuid = "{"+str(uuid.uuid4())+"}",
					name = "SnapShot := 0",
					#time_stamp=save_file_date,
					#state_file=X,
					hardware=copy_hardware,
				)

			new_storage_controller = vb_struct.StorageController(
				name="SATA",
				type="AHCI",
				port_count=1,
				use_host_iocache=False,
				bootable=True,
				ide0_master_emulation_port=0,
				ide0_slave_emulation_port=1,
				ide1_master_emulation_port=2,
				ide1_slave_emulation_port=3,
				# attached_device=""
			)
			new_storage_controller.attached_device.append(vb_struct.AttachedDevice(
				type="HardDisk",
				hotpluggable=False,
				port=0,
				device=0,
				image=vb_struct.Image(
					uuid=os.path.basename(vdi_file).replace(".vdi", "")
				)
			))
			#ini_snapshot.hardware.storage_controllers.storage_controller = new_storage_controller

			#og_config.machine.current_snapshot = ini_snapshot.uuid
			og_config.machine.snapshot = ini_snapshot

			last_snapshot = ini_snapshot


			for save_file in save_files:
				save_file_date = save_file.replace('.sav','')
				temp_snapshot = vb_struct.Snapshot(
					uuid = "{"+str(uuid.uuid4())+"}",
					name = "SnapShot := {0}".format(save_file_date),
					time_stamp=save_file_date,
					#state_file=X,
					hardware=copy_hardware,
				)

				if save_file == save_files[-1]: #LAST ITERATION
					og_config.machine.current_snapshot = temp_snapshot.uuid

					new_storage_controller = vb_struct.StorageController(
						name="SATA",
						type="AHCI",
						port_count=1,
						use_host_iocache=False,
						bootable=True,
						ide0_master_emulation_port=0,
						ide0_slave_emulation_port=1,
						ide1_master_emulation_port=2,
						ide1_slave_emulation_port=3,
						#attached_device=""
					)
					new_storage_controller.attached_device.append(vb_struct.AttachedDevice(
						type="HardDisk",
						hotpluggable=False,
						port=0,
						device=0,
						image=vb_struct.Image(
							uuid=os.path.basename(vdi_file).replace(".vdi","")
						)
					))

					temp_snapshot.hardware.storage_controllers.storage_controller = new_storage_controller
					og_config.machine.current_snapshot = temp_snapshot.uuid
					last_snapshot.snapshots = vb_struct.Snapshots(
						snapshot=[temp_snapshot]
					)

					last_snapshot = temp_snapshot
				else:
					last_snapshot.snapshots = vb_struct.Snapshots(
						[temp_snapshot]
					)
					last_snapshot = temp_snapshot

			og_config.machine.media_registry.hard_disks.hard_disk.hard_disk = vb_struct.HardDisk(
				uuid=os.path.basename(vdi_file).replace(".vdi",""),
				location=vdi_file,
				format="vdi"
			)
			config = SerializerConfig(pretty_print=True)
			serializer = XmlSerializer(config=config)
			og_config_string = serializer.render(og_config)

			for remove,replacewith in [
				('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ',None),
				(' xsi:type="ns0:Snapshot"',None),
				('<ns0:','<'),
				('</ns0:','</'),
				('xmlns:ns0','xmlns'),
			]:
				og_config_string = og_config_string.replace(remove,replacewith or '')


			os.system("cp {0} {0}.OG".format(config_file))
			with open(config_file,"w+") as writer:
				writer.write(og_config_string)

	def import_ova(self, ovafile):
		self.ovafile = ovafile

		exe("{0}  import {1} --vsys 0 --vmname {2} --ostype \"Windows10\" --cpus {3} --memory {4}".format(self.vboxmanage, self.ovafile, self.vmname, self.cpu, self.ram))

	def disable(self):
		if self.disablehosttime:
			exe("{0} setextradata {1} VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1".format(self.vboxmanage, self.vmname))

		if self.biosoffset:
			exe("{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vboxmanage, self.vmname, self.biosoffset))

		if self.vmdate:
			ms = round((self.vmdate - datetime.now().date()).total_seconds()*1000)

			exe("{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vboxmanage, self.vmname, ms))

		if self.network is None or self.disablenetwork:
			network = "null"
		exe("{0} modifyvm {1} --nic1 {2}".format(self.vboxmanage, self.vmname, network))

	def prep(self):
		if self.ovafile:
			self.import_ova(self.ovafile)

		self.disable()
		if self.sharedfolder:
			self.__shared_folder(self.sharedfolder)
		
		for file in list(self.uploadfiles):
			self.uploadfile(file)

		if False:			
			self.start()
			for cmd in self.cmds_to_exe_with_network:
				self.vbexe(cmd)

			#Disable the Network
			exe("{0} modifyvm {1} --nic1 null".format(self.vboxmanage, self.vmname))
			for cmd in self.cmds_to_exe_without_network:
				self.vbexe(cmd)

			#Turn on the Network
			exe("{0} modifyvm {1} --nic1 nat".format(self.vboxmanage, self.vmname))
			self.stop()
		
		self.disable()

	def run(self, headless:bool = True):
		self.prep()
		self.on(headless)
	
	def __enter__(self):
		self.run(True)
	
	def off(self):
		exe("{0} controlvm {1} poweroff".format(self.vboxmanage, self.vmname))

	def __exit__(self, type, value, traceback):
		self.stop()
	
	def uploadfile(self, file:str):
		exe("{0} guestcontrol {1} copyto {2} --target-directory=c:/Users/{3}/Desktop/ --user \"{3}\"".format(self.vboxmanage, self.vmname, file, self.username))
	
	def clean(self, deletefiles:bool=True):
		cmd = "{0} unregistervm {1}".format(self.vboxmanage, self.vmname)

		if deletefiles:
			cmd += " --delete"
			if self.ovafile:
				os.remove(self.ovafile)

		exe(cmd)
	
	def destroy(self, deletefiles:bool=True):
		self.clean(deletefiles)

@dataclass
class vagrant(object):
	vagrant_base:str = "talisker/windows10pro",
	disablehosttime: bool = True,
	disablenetwork: bool = True,
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
	save_files:list = None

	def __post_init__(self):
		if self.uploadfiles is None or type(self.uploadfiles) is tuple:
			self.uploadfiles = []

		if self.choco_packages is None or type(self.choco_packages) is tuple:
			self.choco_packages = []

		if self.python_packages is None or type(self.python_packages) is tuple:
			self.python_packages = []

		if self.scripts_to_run is None or type(self.scripts_to_run) is tuple:
			self.scripts_to_run = []

		if self.save_files is None or type(self.save_files) is tuple:
			self.save_files = []
		
		if self.vmdate is None or type(self.vmdate) is tuple:
			self.vmdate = None

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

	def snapshot_take(self,snapshotname):
		vb_name = self.vagrant_name
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		exe("{0} snapshot {1} take {2}".format(self.vboxmanage,vb_name, snapshotname))

	def snapshot_load(self,snapshotname):
		vb_name = self.vagrant_name
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		exe("{0} snapshot {1} restore {2}".format(self.vboxmanage,vb_name, snapshotname))

	def snapshot_list(self):
		vb_name = self.vagrant_name
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		exe("{0} snapshot {1} list".format(self.vboxmanage,vb_name))

	def snapshot_delete(self,snapshotname):
		vb_name = self.vagrant_name
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		exe("{0} snapshot {1} delete {2}".format(self.vboxmanage,vb_name, snapshotname))

	def export_to_ova(self,ovaname):
		vb_name = self.vagrant_name
		#https://www.techrepublic.com/article/how-to-import-and-export-virtualbox-appliances-from-the-command-line/
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html
		exe("{0} export {1} --ovf10 --options manifest,iso,nomacs -o {2}".format(self.vboxmanage,vb_name, ovaname))

	#https://jd-bots.com/2021/05/15/how-to-run-powershell-script-on-windows-startup/
	#https://stackoverflow.com/questions/20575257/how-do-i-run-a-powershell-script-when-the-computer-starts
	def create_runner(self):
		with open("on_login.cmd","w+") as writer:
			writer.write("""powershell -windowstyle hidden C:\\\\Users\\\\vagrant\\\\Desktop\\\\on_start.ps1""")
		return "on_login.cmd"

	def write_startup_file(self):
		contents = []
		if self.vmdate:
			diff_days = (self.vmdate - datetime.now().date()).days
			contents += [
				"Set-Date -Date (Get-Date).AddDays({0})".format(diff_days)
			]

		if self.disablenetwork:
			contents += [
				"""Disable-NetAdapter -Name "*" -Confirm:$false """
			]

		with open("on_start.ps1", "w+") as writer:
			writer.write("""
{0}
""".format(
	"\n".join(contents)
))
		return "on_start.ps1"

	def add_file(self, foil, directory="C:\\\\Users\\\\vagrant\\\\Desktop"):
		return """ win10.vm.provision "file", source: "{0}", destination: "{1}\\\\{0}" """.format(foil, directory)


	def prep(self):
		self.uploadfiles = list(self.uploadfiles)	
		self.uploadfiles += [self.write_startup_file()]
		uploading_file_strings = []
		for foil in self.uploadfiles:
			uploading_file_strings += [self.add_file(foil)]

		uploading_file_strings += [
			self.add_file(self.create_runner(),"""C:\\\\Users\\\\vagrant\\\\AppData\\\\Roaming\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup""")
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
					""" win10.vm.provision :shell, :inline => "C:\\\\Python38\\\\python -m pip install --upgrade pip {0} " """.format(" ".join(self.python_packages))
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

	def resume(self):
		if self.vagrant_name.strip() is not None and self.vagrant_name.strip() != '':
			if self.vmdate:
				diff_days = (self.vmdate - datetime.now().date())
				ms = round(diff_days.total_seconds()*1000)
				exe("{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vb_box_exe, self.vagrant_name, ms))

			cmd = "{0} startvm {1}".format(self.vb_box_exe,self.vagrant_name)
			if self.headless:
				cmd += " --type headless"

			exe(cmd)
		else:
			print("Vagrant VM hasn't been created yet")

	def off(self):
		self.vagrant_name
		exe("{0} controlvm {1} poweroff".format(self.vb_box_exe, self.vagrant_name))
	
	def destroy(self,emptyflag=False):
		self.vagrant_name
		exe(""" vagrant destroy -f """)
		for foil in ["Vagrant", "on_start*", "on_login*"]:
			exe("rm {0}".format(foil))
		exe("yes|rm -r .vagrant/")
		for foil in list(self.uploadfiles):
			if foil not in self.save_files:
				exe("rm {0}".format(foil))

	def clean(self,emptyflag=False):
		self.destroy(emptyflag)


def install_docker():
	#https://docs.docker.com/engine/install/ubuntu/
	for string in [
		"sudo apt-get update",
		"sudo apt-get install ca-certificates curl gnupg",
		"sudo install -m 0755 -d /etc/apt/keyrings",
		"curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
		"sudo chmod a+r /etc/apt/keyrings/docker.gpg",
		"""echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
		""",
		"sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
		"sudo apt-get update",
		"sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
	]:
		try:
			cmd(string)
		except: pass
