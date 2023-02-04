"""
This is fully generated through the use of https://codebeautify.org/json-to-python-pojo-generator 
"""

# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome4_from_dict(json.loads(json_string))

from typing import Any, List, Optional, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_stringified_bool(x: str) -> bool:
    if x == "true":
        return True
    if x == "false":
        return False
    assert False


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


class ExtraDataItem:
    name: str
    value: str

    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'ExtraDataItem':
        assert isinstance(obj, dict)
        name = from_str(obj.get("@name"))
        value = from_str(obj.get("@value"))
        return ExtraDataItem(name, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@name"] = from_str(self.name)
        result["@value"] = from_str(self.value)
        return result


class ExtraData:
    extra_data_item: List[ExtraDataItem]

    def __init__(self, extra_data_item: List[ExtraDataItem]) -> None:
        self.extra_data_item = extra_data_item

    @staticmethod
    def from_dict(obj: Any) -> 'ExtraData':
        assert isinstance(obj, dict)
        extra_data_item = from_list(ExtraDataItem.from_dict, obj.get("ExtraDataItem"))
        return ExtraData(extra_data_item)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ExtraDataItem"] = from_list(lambda x: to_class(ExtraDataItem, x), self.extra_data_item)
        return result


class Group:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Group':
        assert isinstance(obj, dict)
        name = from_str(obj.get("@name"))
        return Group(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@name"] = from_str(self.name)
        return result


class Groups:
    group: Group

    def __init__(self, group: Group) -> None:
        self.group = group

    @staticmethod
    def from_dict(obj: Any) -> 'Groups':
        assert isinstance(obj, dict)
        group = Group.from_dict(obj.get("Group"))
        return Groups(group)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Group"] = to_class(Group, self.group)
        return result


class AudioAdapter:
    controller: str
    driver: str
    enabled: bool
    enabled_out: bool

    def __init__(self, controller: str, driver: str, enabled: bool, enabled_out: bool) -> None:
        self.controller = controller
        self.driver = driver
        self.enabled = enabled
        self.enabled_out = enabled_out

    @staticmethod
    def from_dict(obj: Any) -> 'AudioAdapter':
        assert isinstance(obj, dict)
        controller = from_str(obj.get("@controller"))
        driver = from_str(obj.get("@driver"))
        enabled = from_stringified_bool(from_str(obj.get("@enabled")))
        enabled_out = from_stringified_bool(from_str(obj.get("@enabledOut")))
        return AudioAdapter(controller, driver, enabled, enabled_out)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@controller"] = from_str(self.controller)
        result["@driver"] = from_str(self.driver)
        result["@enabled"] = from_str(str(self.enabled).lower())
        result["@enabledOut"] = from_str(str(self.enabled_out).lower())
        return result


class Ioapic:
    enabled: bool

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    @staticmethod
    def from_dict(obj: Any) -> 'Ioapic':
        assert isinstance(obj, dict)
        enabled = from_stringified_bool(from_str(obj.get("@enabled")))
        return Ioapic(enabled)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@enabled"] = from_str(str(self.enabled).lower())
        return result


class TimeOffset:
    value: str

    def __init__(self, value: str) -> None:
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'TimeOffset':
        assert isinstance(obj, dict)
        value = from_str(obj.get("@value"))
        return TimeOffset(value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@value"] = from_str(self.value)
        return result


class BIOS:
    ioapic: Ioapic
    time_offset: TimeOffset
    smbios_uuid_little_endian: Ioapic

    def __init__(self, ioapic: Ioapic, time_offset: TimeOffset, smbios_uuid_little_endian: Ioapic) -> None:
        self.ioapic = ioapic
        self.time_offset = time_offset
        self.smbios_uuid_little_endian = smbios_uuid_little_endian

    @staticmethod
    def from_dict(obj: Any) -> 'BIOS':
        assert isinstance(obj, dict)
        ioapic = Ioapic.from_dict(obj.get("IOAPIC"))
        time_offset = TimeOffset.from_dict(obj.get("TimeOffset"))
        smbios_uuid_little_endian = Ioapic.from_dict(obj.get("SmbiosUuidLittleEndian"))
        return BIOS(ioapic, time_offset, smbios_uuid_little_endian)

    def to_dict(self) -> dict:
        result: dict = {}
        result["IOAPIC"] = to_class(Ioapic, self.ioapic)
        result["TimeOffset"] = to_class(TimeOffset, self.time_offset)
        result["SmbiosUuidLittleEndian"] = to_class(Ioapic, self.smbios_uuid_little_endian)
        return result


class Clipboard:
    mode: str

    def __init__(self, mode: str) -> None:
        self.mode = mode

    @staticmethod
    def from_dict(obj: Any) -> 'Clipboard':
        assert isinstance(obj, dict)
        mode = from_str(obj.get("@mode"))
        return Clipboard(mode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@mode"] = from_str(self.mode)
        return result


class CPU:
    count: int
    pae: Ioapic
    long_mode: Ioapic
    hardware_virt_ex_large_pages: Ioapic

    def __init__(self, count: int, pae: Ioapic, long_mode: Ioapic, hardware_virt_ex_large_pages: Ioapic) -> None:
        self.count = count
        self.pae = pae
        self.long_mode = long_mode
        self.hardware_virt_ex_large_pages = hardware_virt_ex_large_pages

    @staticmethod
    def from_dict(obj: Any) -> 'CPU':
        assert isinstance(obj, dict)
        count = int(from_str(obj.get("@count")))
        pae = Ioapic.from_dict(obj.get("PAE"))
        long_mode = Ioapic.from_dict(obj.get("LongMode"))
        hardware_virt_ex_large_pages = Ioapic.from_dict(obj.get("HardwareVirtExLargePages"))
        return CPU(count, pae, long_mode, hardware_virt_ex_large_pages)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@count"] = from_str(str(self.count))
        result["PAE"] = to_class(Ioapic, self.pae)
        result["LongMode"] = to_class(Ioapic, self.long_mode)
        result["HardwareVirtExLargePages"] = to_class(Ioapic, self.hardware_virt_ex_large_pages)
        return result


class Display:
    controller: str
    vram_size: int

    def __init__(self, controller: str, vram_size: int) -> None:
        self.controller = controller
        self.vram_size = vram_size

    @staticmethod
    def from_dict(obj: Any) -> 'Display':
        assert isinstance(obj, dict)
        controller = from_str(obj.get("@controller"))
        vram_size = int(from_str(obj.get("@VRAMSize")))
        return Display(controller, vram_size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@controller"] = from_str(self.controller)
        result["@VRAMSize"] = from_str(str(self.vram_size))
        return result


class GuestProperty:
    name: str
    value: str
    timestamp: str
    flags: str

    def __init__(self, name: str, value: str, timestamp: str, flags: str) -> None:
        self.name = name
        self.value = value
        self.timestamp = timestamp
        self.flags = flags

    @staticmethod
    def from_dict(obj: Any) -> 'GuestProperty':
        assert isinstance(obj, dict)
        name = from_str(obj.get("@name"))
        value = from_str(obj.get("@value"))
        timestamp = from_str(obj.get("@timestamp"))
        flags = from_str(obj.get("@flags"))
        return GuestProperty(name, value, timestamp, flags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@name"] = from_str(self.name)
        result["@value"] = from_str(self.value)
        result["@timestamp"] = from_str(self.timestamp)
        result["@flags"] = from_str(self.flags)
        return result


class GuestProperties:
    guest_property: List[GuestProperty]

    def __init__(self, guest_property: List[GuestProperty]) -> None:
        self.guest_property = guest_property

    @staticmethod
    def from_dict(obj: Any) -> 'GuestProperties':
        assert isinstance(obj, dict)
        guest_property = from_list(GuestProperty.from_dict, obj.get("GuestProperty"))
        return GuestProperties(guest_property)

    def to_dict(self) -> dict:
        result: dict = {}
        result["GuestProperty"] = from_list(lambda x: to_class(GuestProperty, x), self.guest_property)
        return result


class HID:
    pointing: str

    def __init__(self, pointing: str) -> None:
        self.pointing = pointing

    @staticmethod
    def from_dict(obj: Any) -> 'HID':
        assert isinstance(obj, dict)
        pointing = from_str(obj.get("@Pointing"))
        return HID(pointing)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@Pointing"] = from_str(self.pointing)
        return result


class Memory:
    ram_size: int

    def __init__(self, ram_size: int) -> None:
        self.ram_size = ram_size

    @staticmethod
    def from_dict(obj: Any) -> 'Memory':
        assert isinstance(obj, dict)
        ram_size = int(from_str(obj.get("@RAMSize")))
        return Memory(ram_size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@RAMSize"] = from_str(str(self.ram_size))
        return result


class Nat:
    localhost_reachable: bool

    def __init__(self, localhost_reachable: bool) -> None:
        self.localhost_reachable = localhost_reachable

    @staticmethod
    def from_dict(obj: Any) -> 'Nat':
        assert isinstance(obj, dict)
        localhost_reachable = from_stringified_bool(from_str(obj.get("@localhost-reachable")))
        return Nat(localhost_reachable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@localhost-reachable"] = from_str(str(self.localhost_reachable).lower())
        return result


class DisabledModes:
    nat: Nat
    internal_network: Group
    nat_network: Group

    def __init__(self, nat: Nat, internal_network: Group, nat_network: Group) -> None:
        self.nat = nat
        self.internal_network = internal_network
        self.nat_network = nat_network

    @staticmethod
    def from_dict(obj: Any) -> 'DisabledModes':
        assert isinstance(obj, dict)
        nat = Nat.from_dict(obj.get("NAT"))
        internal_network = Group.from_dict(obj.get("InternalNetwork"))
        nat_network = Group.from_dict(obj.get("NATNetwork"))
        return DisabledModes(nat, internal_network, nat_network)

    def to_dict(self) -> dict:
        result: dict = {}
        result["NAT"] = to_class(Nat, self.nat)
        result["InternalNetwork"] = to_class(Group, self.internal_network)
        result["NATNetwork"] = to_class(Group, self.nat_network)
        return result


class Adapter:
    slot: int
    enabled: bool
    mac_address: str
    cable: bool
    type: str
    disabled_modes: DisabledModes

    def __init__(self, slot: int, enabled: bool, mac_address: str, cable: bool, type: str, disabled_modes: DisabledModes) -> None:
        self.slot = slot
        self.enabled = enabled
        self.mac_address = mac_address
        self.cable = cable
        self.type = type
        self.disabled_modes = disabled_modes

    @staticmethod
    def from_dict(obj: Any) -> 'Adapter':
        assert isinstance(obj, dict)
        slot = int(from_str(obj.get("@slot")))
        enabled = from_stringified_bool(from_str(obj.get("@enabled")))
        mac_address = from_str(obj.get("@MACAddress"))
        cable = from_stringified_bool(from_str(obj.get("@cable")))
        type = from_str(obj.get("@type"))
        disabled_modes = DisabledModes.from_dict(obj.get("DisabledModes"))
        return Adapter(slot, enabled, mac_address, cable, type, disabled_modes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@slot"] = from_str(str(self.slot))
        result["@enabled"] = from_str(str(self.enabled).lower())
        result["@MACAddress"] = from_str(self.mac_address)
        result["@cable"] = from_str(str(self.cable).lower())
        result["@type"] = from_str(self.type)
        result["DisabledModes"] = to_class(DisabledModes, self.disabled_modes)
        return result


class Network:
    adapter: Adapter

    def __init__(self, adapter: Adapter) -> None:
        self.adapter = adapter

    @staticmethod
    def from_dict(obj: Any) -> 'Network':
        assert isinstance(obj, dict)
        adapter = Adapter.from_dict(obj.get("Adapter"))
        return Network(adapter)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Adapter"] = to_class(Adapter, self.adapter)
        return result


class SharedFolder:
    name: str
    host_path: str
    writable: bool
    auto_mount: bool

    def __init__(self, name: str, host_path: str, writable: bool, auto_mount: bool) -> None:
        self.name = name
        self.host_path = host_path
        self.writable = writable
        self.auto_mount = auto_mount

    @staticmethod
    def from_dict(obj: Any) -> 'SharedFolder':
        assert isinstance(obj, dict)
        name = from_str(obj.get("@name"))
        host_path = from_str(obj.get("@hostPath"))
        writable = from_stringified_bool(from_str(obj.get("@writable")))
        auto_mount = from_stringified_bool(from_str(obj.get("@autoMount")))
        return SharedFolder(name, host_path, writable, auto_mount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@name"] = from_str(self.name)
        result["@hostPath"] = from_str(self.host_path)
        result["@writable"] = from_str(str(self.writable).lower())
        result["@autoMount"] = from_str(str(self.auto_mount).lower())
        return result


class SharedFolders:
    shared_folder: List[SharedFolder]

    def __init__(self, shared_folder: List[SharedFolder]) -> None:
        self.shared_folder = shared_folder

    @staticmethod
    def from_dict(obj: Any) -> 'SharedFolders':
        assert isinstance(obj, dict)
        shared_folder = from_list(SharedFolder.from_dict, obj.get("SharedFolder"))
        return SharedFolders(shared_folder)

    def to_dict(self) -> dict:
        result: dict = {}
        result["SharedFolder"] = from_list(lambda x: to_class(SharedFolder, x), self.shared_folder)
        return result


class AttachedDeviceImage:
    uuid: str

    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'AttachedDeviceImage':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        return AttachedDeviceImage(uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        return result


class AttachedDevice:
    type: str
    hotpluggable: bool
    port: int
    device: int
    image: AttachedDeviceImage
    passthrough: Optional[bool]

    def __init__(self, type: str, hotpluggable: bool, port: int, device: int, image: AttachedDeviceImage, passthrough: Optional[bool]) -> None:
        self.type = type
        self.hotpluggable = hotpluggable
        self.port = port
        self.device = device
        self.image = image
        self.passthrough = passthrough

    @staticmethod
    def from_dict(obj: Any) -> 'AttachedDevice':
        assert isinstance(obj, dict)
        type = from_str(obj.get("@type"))
        hotpluggable = from_stringified_bool(from_str(obj.get("@hotpluggable")))
        port = int(from_str(obj.get("@port")))
        device = int(from_str(obj.get("@device")))
        image = AttachedDeviceImage.from_dict(obj.get("Image"))
        passthrough = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("@passthrough"))
        return AttachedDevice(type, hotpluggable, port, device, image, passthrough)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = from_str(self.type)
        result["@hotpluggable"] = from_str(str(self.hotpluggable).lower())
        result["@port"] = from_str(str(self.port))
        result["@device"] = from_str(str(self.device))
        result["Image"] = to_class(AttachedDeviceImage, self.image)
        result["@passthrough"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.passthrough)
        return result


class StorageController:
    name: str
    type: str
    port_count: int
    use_host_io_cache: bool
    bootable: bool
    ide0_master_emulation_port: int
    ide0_slave_emulation_port: int
    ide1_master_emulation_port: int
    ide1_slave_emulation_port: int
    attached_device: List[AttachedDevice]

    def __init__(self, name: str, type: str, port_count: int, use_host_io_cache: bool, bootable: bool, ide0_master_emulation_port: int, ide0_slave_emulation_port: int, ide1_master_emulation_port: int, ide1_slave_emulation_port: int, attached_device: List[AttachedDevice]) -> None:
        self.name = name
        self.type = type
        self.port_count = port_count
        self.use_host_io_cache = use_host_io_cache
        self.bootable = bootable
        self.ide0_master_emulation_port = ide0_master_emulation_port
        self.ide0_slave_emulation_port = ide0_slave_emulation_port
        self.ide1_master_emulation_port = ide1_master_emulation_port
        self.ide1_slave_emulation_port = ide1_slave_emulation_port
        self.attached_device = attached_device

    @staticmethod
    def from_dict(obj: Any) -> 'StorageController':
        assert isinstance(obj, dict)
        name = from_str(obj.get("@name"))
        type = from_str(obj.get("@type"))
        port_count = int(from_str(obj.get("@PortCount")))
        use_host_io_cache = from_stringified_bool(from_str(obj.get("@useHostIOCache")))
        bootable = from_stringified_bool(from_str(obj.get("@Bootable")))
        ide0_master_emulation_port = int(from_str(obj.get("@IDE0MasterEmulationPort")))
        ide0_slave_emulation_port = int(from_str(obj.get("@IDE0SlaveEmulationPort")))
        ide1_master_emulation_port = int(from_str(obj.get("@IDE1MasterEmulationPort")))
        ide1_slave_emulation_port = int(from_str(obj.get("@IDE1SlaveEmulationPort")))
        attached_device = from_list(AttachedDevice.from_dict, obj.get("AttachedDevice"))
        return StorageController(name, type, port_count, use_host_io_cache, bootable, ide0_master_emulation_port, ide0_slave_emulation_port, ide1_master_emulation_port, ide1_slave_emulation_port, attached_device)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@name"] = from_str(self.name)
        result["@type"] = from_str(self.type)
        result["@PortCount"] = from_str(str(self.port_count))
        result["@useHostIOCache"] = from_str(str(self.use_host_io_cache).lower())
        result["@Bootable"] = from_str(str(self.bootable).lower())
        result["@IDE0MasterEmulationPort"] = from_str(str(self.ide0_master_emulation_port))
        result["@IDE0SlaveEmulationPort"] = from_str(str(self.ide0_slave_emulation_port))
        result["@IDE1MasterEmulationPort"] = from_str(str(self.ide1_master_emulation_port))
        result["@IDE1SlaveEmulationPort"] = from_str(str(self.ide1_slave_emulation_port))
        result["AttachedDevice"] = from_list(lambda x: to_class(AttachedDevice, x), self.attached_device)
        return result


class StorageControllers:
    storage_controller: StorageController

    def __init__(self, storage_controller: StorageController) -> None:
        self.storage_controller = storage_controller

    @staticmethod
    def from_dict(obj: Any) -> 'StorageControllers':
        assert isinstance(obj, dict)
        storage_controller = StorageController.from_dict(obj.get("StorageController"))
        return StorageControllers(storage_controller)

    def to_dict(self) -> dict:
        result: dict = {}
        result["StorageController"] = to_class(StorageController, self.storage_controller)
        return result


class Controller:
    name: str
    type: str

    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Controller':
        assert isinstance(obj, dict)
        name = from_str(obj.get("@name"))
        type = from_str(obj.get("@type"))
        return Controller(name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@name"] = from_str(self.name)
        result["@type"] = from_str(self.type)
        return result


class Controllers:
    controller: Controller

    def __init__(self, controller: Controller) -> None:
        self.controller = controller

    @staticmethod
    def from_dict(obj: Any) -> 'Controllers':
        assert isinstance(obj, dict)
        controller = Controller.from_dict(obj.get("Controller"))
        return Controllers(controller)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Controller"] = to_class(Controller, self.controller)
        return result


class USB:
    controllers: Controllers

    def __init__(self, controllers: Controllers) -> None:
        self.controllers = controllers

    @staticmethod
    def from_dict(obj: Any) -> 'USB':
        assert isinstance(obj, dict)
        controllers = Controllers.from_dict(obj.get("Controllers"))
        return USB(controllers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Controllers"] = to_class(Controllers, self.controllers)
        return result


class Hardware:
    cpu: CPU
    memory: Memory
    hid: HID
    display: Display
    bios: BIOS
    usb: USB
    network: Network
    audio_adapter: AudioAdapter
    shared_folders: SharedFolders
    clipboard: Clipboard
    drag_and_drop: Clipboard
    guest_properties: GuestProperties
    storage_controllers: StorageControllers

    def __init__(self, cpu: CPU, memory: Memory, hid: HID, display: Display, bios: BIOS, usb: USB, network: Network, audio_adapter: AudioAdapter, shared_folders: SharedFolders, clipboard: Clipboard, drag_and_drop: Clipboard, guest_properties: GuestProperties, storage_controllers: StorageControllers) -> None:
        self.cpu = cpu
        self.memory = memory
        self.hid = hid
        self.display = display
        self.bios = bios
        self.usb = usb
        self.network = network
        self.audio_adapter = audio_adapter
        self.shared_folders = shared_folders
        self.clipboard = clipboard
        self.drag_and_drop = drag_and_drop
        self.guest_properties = guest_properties
        self.storage_controllers = storage_controllers

    @staticmethod
    def from_dict(obj: Any) -> 'Hardware':
        assert isinstance(obj, dict)
        cpu = CPU.from_dict(obj.get("CPU"))
        memory = Memory.from_dict(obj.get("Memory"))
        hid = HID.from_dict(obj.get("HID"))
        display = Display.from_dict(obj.get("Display"))
        bios = BIOS.from_dict(obj.get("BIOS"))
        usb = USB.from_dict(obj.get("USB"))
        network = Network.from_dict(obj.get("Network"))
        audio_adapter = AudioAdapter.from_dict(obj.get("AudioAdapter"))
        shared_folders = SharedFolders.from_dict(obj.get("SharedFolders"))
        clipboard = Clipboard.from_dict(obj.get("Clipboard"))
        drag_and_drop = Clipboard.from_dict(obj.get("DragAndDrop"))
        guest_properties = GuestProperties.from_dict(obj.get("GuestProperties"))
        storage_controllers = StorageControllers.from_dict(obj.get("StorageControllers"))
        return Hardware(cpu, memory, hid, display, bios, usb, network, audio_adapter, shared_folders, clipboard, drag_and_drop, guest_properties, storage_controllers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["CPU"] = to_class(CPU, self.cpu)
        result["Memory"] = to_class(Memory, self.memory)
        result["HID"] = to_class(HID, self.hid)
        result["Display"] = to_class(Display, self.display)
        result["BIOS"] = to_class(BIOS, self.bios)
        result["USB"] = to_class(USB, self.usb)
        result["Network"] = to_class(Network, self.network)
        result["AudioAdapter"] = to_class(AudioAdapter, self.audio_adapter)
        result["SharedFolders"] = to_class(SharedFolders, self.shared_folders)
        result["Clipboard"] = to_class(Clipboard, self.clipboard)
        result["DragAndDrop"] = to_class(Clipboard, self.drag_and_drop)
        result["GuestProperties"] = to_class(GuestProperties, self.guest_properties)
        result["StorageControllers"] = to_class(StorageControllers, self.storage_controllers)
        return result


class DVDImagesImage:
    uuid: str
    location: str

    def __init__(self, uuid: str, location: str) -> None:
        self.uuid = uuid
        self.location = location

    @staticmethod
    def from_dict(obj: Any) -> 'DVDImagesImage':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        location = from_str(obj.get("@location"))
        return DVDImagesImage(uuid, location)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        result["@location"] = from_str(self.location)
        return result


class DVDImages:
    image: DVDImagesImage

    def __init__(self, image: DVDImagesImage) -> None:
        self.image = image

    @staticmethod
    def from_dict(obj: Any) -> 'DVDImages':
        assert isinstance(obj, dict)
        image = DVDImagesImage.from_dict(obj.get("Image"))
        return DVDImages(image)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Image"] = to_class(DVDImagesImage, self.image)
        return result


class HardDisk:
    uuid: str
    location: str
    format: str
    type: str

    def __init__(self, uuid: str, location: str, format: str, type: str) -> None:
        self.uuid = uuid
        self.location = location
        self.format = format
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'HardDisk':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        location = from_str(obj.get("@location"))
        format = from_str(obj.get("@format"))
        type = from_str(obj.get("@type"))
        return HardDisk(uuid, location, format, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        result["@location"] = from_str(self.location)
        result["@format"] = from_str(self.format)
        result["@type"] = from_str(self.type)
        return result


class HardDisks:
    hard_disk: HardDisk

    def __init__(self, hard_disk: HardDisk) -> None:
        self.hard_disk = hard_disk

    @staticmethod
    def from_dict(obj: Any) -> 'HardDisks':
        assert isinstance(obj, dict)
        hard_disk = HardDisk.from_dict(obj.get("HardDisk"))
        return HardDisks(hard_disk)

    def to_dict(self) -> dict:
        result: dict = {}
        result["HardDisk"] = to_class(HardDisk, self.hard_disk)
        return result


class MediaRegistry:
    hard_disks: HardDisks
    dvd_images: DVDImages

    def __init__(self, hard_disks: HardDisks, dvd_images: DVDImages) -> None:
        self.hard_disks = hard_disks
        self.dvd_images = dvd_images

    @staticmethod
    def from_dict(obj: Any) -> 'MediaRegistry':
        assert isinstance(obj, dict)
        hard_disks = HardDisks.from_dict(obj.get("HardDisks"))
        dvd_images = DVDImages.from_dict(obj.get("DVDImages"))
        return MediaRegistry(hard_disks, dvd_images)

    def to_dict(self) -> dict:
        result: dict = {}
        result["HardDisks"] = to_class(HardDisks, self.hard_disks)
        result["DVDImages"] = to_class(DVDImages, self.dvd_images)
        return result


class Machine:
    uuid: str
    name: str
    os_type: str
    snapshot_folder: str
    last_state_change: datetime
    aborted: bool
    media_registry: MediaRegistry
    extra_data: ExtraData
    hardware: Hardware
    groups: Groups

    def __init__(self, uuid: str, name: str, os_type: str, snapshot_folder: str, last_state_change: datetime, aborted: bool, media_registry: MediaRegistry, extra_data: ExtraData, hardware: Hardware, groups: Groups) -> None:
        self.uuid = uuid
        self.name = name
        self.os_type = os_type
        self.snapshot_folder = snapshot_folder
        self.last_state_change = last_state_change
        self.aborted = aborted
        self.media_registry = media_registry
        self.extra_data = extra_data
        self.hardware = hardware
        self.groups = groups

    @staticmethod
    def from_dict(obj: Any) -> 'Machine':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        name = from_str(obj.get("@name"))
        os_type = from_str(obj.get("@OSType"))
        snapshot_folder = from_str(obj.get("@snapshotFolder"))
        last_state_change = from_datetime(obj.get("@lastStateChange"))
        aborted = from_stringified_bool(from_str(obj.get("@aborted")))
        media_registry = MediaRegistry.from_dict(obj.get("MediaRegistry"))
        extra_data = ExtraData.from_dict(obj.get("ExtraData"))
        hardware = Hardware.from_dict(obj.get("Hardware"))
        groups = Groups.from_dict(obj.get("Groups"))
        return Machine(uuid, name, os_type, snapshot_folder, last_state_change, aborted, media_registry, extra_data, hardware, groups)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        result["@name"] = from_str(self.name)
        result["@OSType"] = from_str(self.os_type)
        result["@snapshotFolder"] = from_str(self.snapshot_folder)
        result["@lastStateChange"] = self.last_state_change.isoformat()
        result["@aborted"] = from_str(str(self.aborted).lower())
        result["MediaRegistry"] = to_class(MediaRegistry, self.media_registry)
        result["ExtraData"] = to_class(ExtraData, self.extra_data)
        result["Hardware"] = to_class(Hardware, self.hardware)
        result["Groups"] = to_class(Groups, self.groups)
        return result


class VirtualBox:
    xmlns: str
    version: str
    machine: Machine

    def __init__(self, xmlns: str, version: str, machine: Machine) -> None:
        self.xmlns = xmlns
        self.version = version
        self.machine = machine

    @staticmethod
    def from_dict(obj: Any) -> 'VirtualBox':
        assert isinstance(obj, dict)
        xmlns = from_str(obj.get("@xmlns"))
        version = from_str(obj.get("@version"))
        machine = Machine.from_dict(obj.get("Machine"))
        return VirtualBox(xmlns, version, machine)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@xmlns"] = from_str(self.xmlns)
        result["@version"] = from_str(self.version)
        result["Machine"] = to_class(Machine, self.machine)
        return result


class Welcome4:
    virtual_box: VirtualBox

    def __init__(self, virtual_box: VirtualBox) -> None:
        self.virtual_box = virtual_box

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome4':
        assert isinstance(obj, dict)
        virtual_box = VirtualBox.from_dict(obj.get("VirtualBox"))
        return Welcome4(virtual_box)

    def to_dict(self) -> dict:
        result: dict = {}
        result["VirtualBox"] = to_class(VirtualBox, self.virtual_box)
        return result


def welcome4_from_dict(s: Any) -> Welcome4:
    return Welcome4.from_dict(s)


def welcome4_to_dict(x: Welcome4) -> Any:
    return to_class(Welcome4, x)

