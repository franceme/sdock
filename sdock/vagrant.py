import os, sys, time, subprocess, mystring
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class vagrant(object):
    vagrant_base: str = "talisker/windows10pro",
    disablehosttime: bool = True,
    disablenetwork: bool = True,
    vmdate: str = None,
    cpu: int = 2,
    ram: int = 4096,
    uploadfiles: list = None,
    choco_packages: list = None,
    python_packages: list = None,
    scripts_to_run: str = None,
    vb_path: str = None,
    vb_box_exe: str = "VBoxManage"
    headless: bool = True
    save_files: list = None

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

    def snapshot_take(self, snapshotname):
        vb_name = self.vagrant_name
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} take {2}".format(self.vboxmanage, vb_name, snapshotname)).exec()

    def snapshot_load(self, snapshotname):
        vb_name = self.vagrant_name
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} restore {2}".format(self.vboxmanage, vb_name, snapshotname)).exec()

    def snapshot_list(self):
        vb_name = self.vagrant_name
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} list".format(self.vboxmanage, vb_name)).exec()

    def snapshot_delete(self, snapshotname):
        vb_name = self.vagrant_name
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} delete {2}".format(self.vboxmanage, vb_name, snapshotname)).exec()

    def export_to_ova(self, ovaname):
        vb_name = self.vagrant_name
        # https://www.techrepublic.com/article/how-to-import-and-export-virtualbox-appliances-from-the-command-line/
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html
        mystring.string("{0} export {1} --ovf10 --options manifest,iso,nomacs -o {2}".format(self.vboxmanage, vb_name,
                                                                                             ovaname)).exec()

    # https://jd-bots.com/2021/05/15/how-to-run-powershell-script-on-windows-startup/
    # https://stackoverflow.com/questions/20575257/how-do-i-run-a-powershell-script-when-the-computer-starts
    def create_runner(self):
        with open("on_login.cmd", "w+") as writer:
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
            self.add_file(self.create_runner(),
                          """C:\\\\Users\\\\vagrant\\\\AppData\\\\Roaming\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup""")
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
                """ win10.vm.provision :shell, :inline => "C:\\\\Python38\\\\python -m pip install --upgrade pip {0} " """.format(
                    " ".join(self.python_packages))
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
        mystring.string(""" vagrant up""").exec()

    def resume(self):
        if self.vagrant_name.strip() is not None and self.vagrant_name.strip() != '':
            if self.vmdate:
                diff_days = (self.vmdate - datetime.now().date())
                ms = round(diff_days.total_seconds() * 1000)
                mystring.string(
                    "{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vb_box_exe, self.vagrant_name, ms)).exec()

            cmd = "{0} startvm {1}".format(self.vb_box_exe, self.vagrant_name)
            if self.headless:
                cmd += " --type headless"

            mystring.string(cmd).exec()
        else:
            print("Vagrant VM hasn't been created yet")

    def off(self):
        self.vagrant_name
        mystring.string("{0} controlvm {1} poweroff".format(self.vb_box_exe, self.vagrant_name)).exec()

    def destroy(self, emptyflag=False):
        self.vagrant_name
        mystring.string(""" vagrant destroy -f """).exec()
        for foil in ["Vagrant", "on_start*", "on_login*"]:
            mystring.string("rm {0}".format(foil)).exec()
        mystring.string("yes|rm -r .vagrant/").exec()
        for foil in list(self.uploadfiles):
            if foil not in self.save_files:
                mystring.string("rm {0}".format(foil)).exec()

    def clean(self, emptyflag=False):
        self.destroy(emptyflag)

