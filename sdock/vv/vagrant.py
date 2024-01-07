import os,sys,argparse

class vagrant(object):
	def __init__(self, box:str, box_name:str, install:bool=False, uninstall:bool=False, remove:bool=False):
		super().__init__()
		self.box = box
		self.name = box_name
		self._provider = None
		self.do_install = install
		self.do_uninstall = uninstall
		self.remove = remove
		self.choco_packages = []

	def __cmd(self, cmd:str):
		os.system("vagrant {0}".format(cmd))

	def add_choco(self, *args):
		for arg in args:
			self.choco_packages += [arg.strip()]

	def install(self):
		self.__cmd("wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg")
		self.__cmd("""-echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com jammy main" | sudo tee /etc/apt/sources.list.d/hashicorp.list""")
		self.__cmd("apt update")
		self.__cmd("apt install vagrant -y")

	def uninstall(self):
		os.system("yes|rm -rf /opt/vagrant")
		os.system("yes|rm -f /usr/bin/vagrant")

	def provider(self, provide:Provider):
		self._provider=provide
		self._provider.name = self.name
		return self._provider

	def on(self):
		with open("Vagrantfile", "w+") as writer:
			writer.write("""# -*- mode: ruby -*- 
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "{0}"
  config.vm.define "win10" do |win10| 
	win10.vm.box = "{1}"
	#win10.vm.provision :shell, :inline => "python -m pip install hugg"
{2}
  end
end
""".format(self.name, self.box, self._provider.vagrant_string()))
		self.__cmd("up")

	def off(self):
		#self.__cmd("halt")
		self.__cmd("off")

	def __enter__(self):
		if self.do_install:
			self.install()
			self._provider.install()
		return self

	def __exit__(self, a=None, b=None, c=None):
		if self.do_uninstall:
			self.uninstall()
			self._provider.uninstall()


if __init__ == '__main__':
	main(parse())
