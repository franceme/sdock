from dataclasses import dataclass, field
import os,sys,Provider

#https://github.com/pycontribs/python-vagrant/blob/main/src/vagrant/__init__.py#L202
#https://github.com/pycontribs/python-vagrant/tree/main

try:
	import vagrant as og_vagrant
	import mystring

	@dataclass
	class vagrant(og_vagrant.Vagrant): #ogvag.Vagrant #
		box:str="talisker/windows10pro"
		name:str
		provider:Provider
		install:bool=False
		uninstall:bool=False
		remove:bool=False
		disablehosttime = True
		disablenetwork = True
		vmdate = None
		cpu = 2
		ram = 4096,
		uploadfiles = []
		choco_packages = []
		python_packages = []
		scripts_to_run = []
		vagrant_exe = "VBoxManage"
		vb_box_exe = "VBoxManage"
		headless = True
		cpu = 2
		ram = 4096
		uploadfiles = []
		choco_packages = []
		python_packages = []
		scripts_to_run = []
		headless = False

		def __post_init__(self):
			super().__init__()

		def __cmd(self, cmd:str):
			mystring.string("{0} {1}".format(self.vagrant_exe, cmd)).exec()
except:pass