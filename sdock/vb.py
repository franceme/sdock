import os, sys, time, subprocess, mystring
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from vbox_extra.gen import VirtualBox

"""
https://xsdata.readthedocs.io/en/latest/
"""

@dataclass
class vb(VirtualBox):
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
    uploadfiles: list = field(default_factory=list)
    vboxmanage: str = "VBoxManage"
    vb_path: str = None
    headless: bool = True

    # cmds_to_exe_with_network:list = field(default_factory=list)
    # cmds_to_exe_without_network:list = field(default_factory=list)

    def on(self, headless: bool = True):
        cmd = "{0} startvm {1}".format(self.vboxmanage, self.vmname)
        if self.headless:
            cmd += " --type headless"

        mystring.string(cmd).exec()

    def vbexe(self, cmd):
        string = "{0} guestcontrol {1} run ".format(self.vboxmanage, self.vmname)

        if self.username:
            string += " --username {0} ".format(self.username)

        string += str(" --exe \"C:\\Windows\\System32\\cmd.exe\" -- cmd.exe/arg0 /C '" + cmd.replace("'", "\'") + "'")
        mystring.string(string).exec()

    def snapshot_take(self, snapshotname):
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} take {2}".format(self.vboxmanage, self.vmname, snapshotname)).exec()

    def snapshot_load(self, snapshotname):
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} restore {2}".format(self.vboxmanage, self.vmname, snapshotname)).exec()

    def snapshot_list(self):
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} list".format(self.vboxmanage, self.vmname)).exec()

    def snapshot_delete(self, snapshotname):
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
        mystring.string("{0} snapshot {1} delete {2}".format(self.vboxmanage, self.vmname, snapshotname)).exec()

    def export_to_ova(self, ovaname):
        # https://www.techrepublic.com/article/how-to-import-and-export-virtualbox-appliances-from-the-command-line/
        # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html
        mystring.string(
            "{0} export {1} --ovf10 --options manifest,iso,nomacs -o {2}".format(self.vboxmanage, self.vmname,
                                                                                 ovaname)).exec()

    def __shared_folder(self, folder):
        mystring.string("{0}  sharedfolder add {1} --name \"{1}_SharedFolder\" --hostpath \"{2}\" --automount".format(
            self.vboxmanage, self.vmname, folder)).exec()

    def add_snapshot_folder(self, snapshot_folder):
        if False:
            import datetime, uuid
            from copy import deepcopy as dc
            from pathlib import Path
            import sdock.vbgen as vb_struct

            # https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-showvminfo.html
            # VBoxManage showvminfo <X> --machinereadable

            machine_info = mystring.string(
                "{0} showvminfo {1} --machinereadable".format(self.vboxmanage, self.vmname), lines=True
            ).exec()
            config_file = None
            for machine_info_line in machine_info:
                machine_info_line = machine_info_line.strip()
                if machine_info_line.startswith("CfgFile"):
                    print(machine_info_line)
                    config_file = machine_info_line.replace("CfgFile=", '').replace('"', '').strip()

            parser = XmlParser()
            og_config = parser.from_path(Path(config_file), vb_struct.VirtualBox)

            # Fix the VMDK Potential
            save_files, vdi_file = [], None
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

            # https://www.tutorialspoint.com/How-to-sort-a-Python-date-string-list
            save_files.sort(key=lambda date: datetime.datetime.strptime(
                '-'.join(date.replace('Snapshots/', '').replace('.sav', '').split("-")[:-1]), "%Y-%m-%dT%H-%M-%S"))

            copy_hardware = dc(og_config.machine.hardware)
            # save_files.reverse()
            ini_snapshot = vb_struct.Snapshot(
                uuid="{" + str(uuid.uuid4()) + "}",
                name="SnapShot := 0",
                # time_stamp=save_file_date,
                # state_file=X,
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
            # ini_snapshot.hardware.storage_controllers.storage_controller = new_storage_controller

            # og_config.machine.current_snapshot = ini_snapshot.uuid
            og_config.machine.snapshot = ini_snapshot

            last_snapshot = ini_snapshot

            for save_file in save_files:
                save_file_date = save_file.replace('.sav', '')
                temp_snapshot = vb_struct.Snapshot(
                    uuid="{" + str(uuid.uuid4()) + "}",
                    name="SnapShot := {0}".format(save_file_date),
                    time_stamp=save_file_date,
                    # state_file=X,
                    hardware=copy_hardware,
                )

                if save_file == save_files[-1]:  # LAST ITERATION
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
                uuid=os.path.basename(vdi_file).replace(".vdi", ""),
                location=vdi_file,
                format="vdi"
            )
            config = SerializerConfig(pretty_print=True)
            serializer = XmlSerializer(config=config)
            og_config_string = serializer.render(og_config)

            for remove, replacewith in [
                ('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ', None),
                (' xsi:type="ns0:Snapshot"', None),
                ('<ns0:', '<'),
                ('</ns0:', '</'),
                ('xmlns:ns0', 'xmlns'),
            ]:
                og_config_string = og_config_string.replace(remove, replacewith or '')

            os.system("cp {0} {0}.OG".format(config_file))
            with open(config_file, "w+") as writer:
                writer.write(og_config_string)

    def import_ova(self, ovafile):
        self.ovafile = ovafile

        mystring.string("{0}  import {1} --vsys 0 --vmname {2} --ostype \"Windows10\" --cpus {3} --memory {4}".format(
            self.vboxmanage, self.ovafile, self.vmname, self.cpu, self.ram)).exec()

    def disable(self):
        if self.disablehosttime:
            mystring.string("{0} setextradata {1} VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1".format(
                self.vboxmanage, self.vmname)).exec()

        if self.biosoffset:
            mystring.string("{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vboxmanage, self.vmname,
                                                                                 self.biosoffset)).exec()

        if self.vmdate:
            ms = round((self.vmdate - datetime.now().date()).total_seconds() * 1000)

            mystring.string(
                "{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vboxmanage, self.vmname, ms)).exec()

        if self.network is None or self.disablenetwork:
            network = "null"
        mystring.string("{0} modifyvm {1} --nic1 {2}".format(self.vboxmanage, self.vmname, network)).exec()

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

            # Disable the Network
            mystring.string("{0} modifyvm {1} --nic1 null".format(self.vboxmanage, self.vmname)).exec()
            for cmd in self.cmds_to_exe_without_network:
                self.vbexe(cmd)

            # Turn on the Network
            mystring.string("{0} modifyvm {1} --nic1 nat".format(self.vboxmanage, self.vmname)).exec()
            self.stop()

        self.disable()

    def run(self, headless: bool = True):
        self.prep()
        self.on(headless)

    def __enter__(self):
        self.run(True)

    def off(self):
        mystring.string("{0} controlvm {1} poweroff".format(self.vboxmanage, self.vmname)).exec()

    def __exit__(self, type, value, traceback):
        self.stop()

    def uploadfile(self, file: str):
        mystring.string(
            "{0} guestcontrol {1} copyto {2} --target-directory=c:/Users/{3}/Desktop/ --user \"{3}\"".format(
                self.vboxmanage, self.vmname, file, self.username)).exec()

    def clean(self, deletefiles: bool = True):
        cmd = "{0} unregistervm {1}".format(self.vboxmanage, self.vmname)

        if deletefiles:
            cmd += " --delete"
            if self.ovafile:
                os.remove(self.ovafile)

        mystring.string(cmd).exec()

    def destroy(self, deletefiles: bool = True):
        self.clean(deletefiles)
