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
#     result = welcome1_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Callable, Type, cast
from enum import Enum
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_none(x: Any) -> Any:
    assert x is None
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
    driver: str

    def __init__(self, driver: str) -> None:
        self.driver = driver

    @staticmethod
    def from_dict(obj: Any) -> 'AudioAdapter':
        assert isinstance(obj, dict)
        driver = from_str(obj.get("@driver"))
        return AudioAdapter(driver)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@driver"] = from_str(self.driver)
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


class BIOS:
    ioapic: Ioapic

    def __init__(self, ioapic: Ioapic) -> None:
        self.ioapic = ioapic

    @staticmethod
    def from_dict(obj: Any) -> 'BIOS':
        assert isinstance(obj, dict)
        ioapic = Ioapic.from_dict(obj.get("IOAPIC"))
        return BIOS(ioapic)

    def to_dict(self) -> dict:
        result: dict = {}
        result["IOAPIC"] = to_class(Ioapic, self.ioapic)
        return result


class Order:
    position: int
    device: str

    def __init__(self, position: int, device: str) -> None:
        self.position = position
        self.device = device

    @staticmethod
    def from_dict(obj: Any) -> 'Order':
        assert isinstance(obj, dict)
        position = int(from_str(obj.get("@position")))
        device = from_str(obj.get("@device"))
        return Order(position, device)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@position"] = from_str(str(self.position))
        result["@device"] = from_str(self.device)
        return result


class Boot:
    order: List[Order]

    def __init__(self, order: List[Order]) -> None:
        self.order = order

    @staticmethod
    def from_dict(obj: Any) -> 'Boot':
        assert isinstance(obj, dict)
        order = from_list(Order.from_dict, obj.get("Order"))
        return Boot(order)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Order"] = from_list(lambda x: to_class(Order, x), self.order)
        return result


class CPU:
    pae: Ioapic
    long_mode: Ioapic
    hardware_virt_ex_large_pages: Ioapic

    def __init__(self, pae: Ioapic, long_mode: Ioapic, hardware_virt_ex_large_pages: Ioapic) -> None:
        self.pae = pae
        self.long_mode = long_mode
        self.hardware_virt_ex_large_pages = hardware_virt_ex_large_pages

    @staticmethod
    def from_dict(obj: Any) -> 'CPU':
        assert isinstance(obj, dict)
        pae = Ioapic.from_dict(obj.get("PAE"))
        long_mode = Ioapic.from_dict(obj.get("LongMode"))
        hardware_virt_ex_large_pages = Ioapic.from_dict(obj.get("HardwareVirtExLargePages"))
        return CPU(pae, long_mode, hardware_virt_ex_large_pages)

    def to_dict(self) -> dict:
        result: dict = {}
        result["PAE"] = to_class(Ioapic, self.pae)
        result["LongMode"] = to_class(Ioapic, self.long_mode)
        result["HardwareVirtExLargePages"] = to_class(Ioapic, self.hardware_virt_ex_large_pages)
        return result


class Flags(Enum):
    EMPTY = ""
    RDONLYGUEST = "RDONLYGUEST"
    TRANSIENT_RDONLYGUEST = "TRANSIENT, RDONLYGUEST"
    TRANSIENT_TRANSRESET = "TRANSIENT, TRANSRESET"


class GuestProperty:
    name: str
    value: str
    timestamp: str
    flags: Flags

    def __init__(self, name: str, value: str, timestamp: str, flags: Flags) -> None:
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
        flags = Flags(obj.get("@flags"))
        return GuestProperty(name, value, timestamp, flags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@name"] = from_str(self.name)
        result["@value"] = from_str(self.value)
        result["@timestamp"] = from_str(self.timestamp)
        result["@flags"] = to_enum(Flags, self.flags)
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
    type: str
    disabled_modes: DisabledModes

    def __init__(self, slot: int, enabled: bool, mac_address: str, type: str, disabled_modes: DisabledModes) -> None:
        self.slot = slot
        self.enabled = enabled
        self.mac_address = mac_address
        self.type = type
        self.disabled_modes = disabled_modes

    @staticmethod
    def from_dict(obj: Any) -> 'Adapter':
        assert isinstance(obj, dict)
        slot = int(from_str(obj.get("@slot")))
        enabled = from_stringified_bool(from_str(obj.get("@enabled")))
        mac_address = from_str(obj.get("@MACAddress"))
        type = from_str(obj.get("@type"))
        disabled_modes = DisabledModes.from_dict(obj.get("DisabledModes"))
        return Adapter(slot, enabled, mac_address, type, disabled_modes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@slot"] = from_str(str(self.slot))
        result["@enabled"] = from_str(str(self.enabled).lower())
        result["@MACAddress"] = from_str(self.mac_address)
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


class VRDEProperties:
    property: List[ExtraDataItem]

    def __init__(self, property: List[ExtraDataItem]) -> None:
        self.property = property

    @staticmethod
    def from_dict(obj: Any) -> 'VRDEProperties':
        assert isinstance(obj, dict)
        property = from_list(ExtraDataItem.from_dict, obj.get("Property"))
        return VRDEProperties(property)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Property"] = from_list(lambda x: to_class(ExtraDataItem, x), self.property)
        return result


class RemoteDisplay:
    enabled: bool
    vrde_properties: VRDEProperties

    def __init__(self, enabled: bool, vrde_properties: VRDEProperties) -> None:
        self.enabled = enabled
        self.vrde_properties = vrde_properties

    @staticmethod
    def from_dict(obj: Any) -> 'RemoteDisplay':
        assert isinstance(obj, dict)
        enabled = from_stringified_bool(from_str(obj.get("@enabled")))
        vrde_properties = VRDEProperties.from_dict(obj.get("VRDEProperties"))
        return RemoteDisplay(enabled, vrde_properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@enabled"] = from_str(str(self.enabled).lower())
        result["VRDEProperties"] = to_class(VRDEProperties, self.vrde_properties)
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
    shared_folder: SharedFolder

    def __init__(self, shared_folder: SharedFolder) -> None:
        self.shared_folder = shared_folder

    @staticmethod
    def from_dict(obj: Any) -> 'SharedFolders':
        assert isinstance(obj, dict)
        shared_folder = SharedFolder.from_dict(obj.get("SharedFolder"))
        return SharedFolders(shared_folder)

    def to_dict(self) -> dict:
        result: dict = {}
        result["SharedFolder"] = to_class(SharedFolder, self.shared_folder)
        return result


class Image:
    uuid: str

    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        return Image(uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        return result


class AttachedDevice:
    type: str
    hotpluggable: bool
    port: int
    device: int
    image: Image

    def __init__(self, type: str, hotpluggable: bool, port: int, device: int, image: Image) -> None:
        self.type = type
        self.hotpluggable = hotpluggable
        self.port = port
        self.device = device
        self.image = image

    @staticmethod
    def from_dict(obj: Any) -> 'AttachedDevice':
        assert isinstance(obj, dict)
        type = from_str(obj.get("@type"))
        hotpluggable = from_stringified_bool(from_str(obj.get("@hotpluggable")))
        port = int(from_str(obj.get("@port")))
        device = int(from_str(obj.get("@device")))
        image = Image.from_dict(obj.get("Image"))
        return AttachedDevice(type, hotpluggable, port, device, image)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = from_str(self.type)
        result["@hotpluggable"] = from_str(str(self.hotpluggable).lower())
        result["@port"] = from_str(str(self.port))
        result["@device"] = from_str(str(self.device))
        result["Image"] = to_class(Image, self.image)
        return result


class StorageController:
    name: str
    type: str
    port_count: int
    use_host_io_cache: bool
    bootable: bool
    attached_device: AttachedDevice

    def __init__(self, name: str, type: str, port_count: int, use_host_io_cache: bool, bootable: bool, attached_device: AttachedDevice) -> None:
        self.name = name
        self.type = type
        self.port_count = port_count
        self.use_host_io_cache = use_host_io_cache
        self.bootable = bootable
        self.attached_device = attached_device

    @staticmethod
    def from_dict(obj: Any) -> 'StorageController':
        assert isinstance(obj, dict)
        name = from_str(obj.get("@name"))
        type = from_str(obj.get("@type"))
        port_count = int(from_str(obj.get("@PortCount")))
        use_host_io_cache = from_stringified_bool(from_str(obj.get("@useHostIOCache")))
        bootable = from_stringified_bool(from_str(obj.get("@Bootable")))
        attached_device = AttachedDevice.from_dict(obj.get("AttachedDevice"))
        return StorageController(name, type, port_count, use_host_io_cache, bootable, attached_device)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@name"] = from_str(self.name)
        result["@type"] = from_str(self.type)
        result["@PortCount"] = from_str(str(self.port_count))
        result["@useHostIOCache"] = from_str(str(self.use_host_io_cache).lower())
        result["@Bootable"] = from_str(str(self.bootable).lower())
        result["AttachedDevice"] = to_class(AttachedDevice, self.attached_device)
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


class Hardware:
    cpu: CPU
    memory: Memory
    boot: Boot
    remote_display: RemoteDisplay
    bios: BIOS
    network: Network
    audio_adapter: AudioAdapter
    shared_folders: SharedFolders
    clipboard: None
    guest_properties: GuestProperties
    storage_controllers: StorageControllers

    def __init__(self, cpu: CPU, memory: Memory, boot: Boot, remote_display: RemoteDisplay, bios: BIOS, network: Network, audio_adapter: AudioAdapter, shared_folders: SharedFolders, clipboard: None, guest_properties: GuestProperties, storage_controllers: StorageControllers) -> None:
        self.cpu = cpu
        self.memory = memory
        self.boot = boot
        self.remote_display = remote_display
        self.bios = bios
        self.network = network
        self.audio_adapter = audio_adapter
        self.shared_folders = shared_folders
        self.clipboard = clipboard
        self.guest_properties = guest_properties
        self.storage_controllers = storage_controllers

    @staticmethod
    def from_dict(obj: Any) -> 'Hardware':
        assert isinstance(obj, dict)
        cpu = CPU.from_dict(obj.get("CPU"))
        memory = Memory.from_dict(obj.get("Memory"))
        boot = Boot.from_dict(obj.get("Boot"))
        remote_display = RemoteDisplay.from_dict(obj.get("RemoteDisplay"))
        bios = BIOS.from_dict(obj.get("BIOS"))
        network = Network.from_dict(obj.get("Network"))
        audio_adapter = AudioAdapter.from_dict(obj.get("AudioAdapter"))
        shared_folders = SharedFolders.from_dict(obj.get("SharedFolders"))
        clipboard = from_none(obj.get("Clipboard"))
        guest_properties = GuestProperties.from_dict(obj.get("GuestProperties"))
        storage_controllers = StorageControllers.from_dict(obj.get("StorageControllers"))
        return Hardware(cpu, memory, boot, remote_display, bios, network, audio_adapter, shared_folders, clipboard, guest_properties, storage_controllers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["CPU"] = to_class(CPU, self.cpu)
        result["Memory"] = to_class(Memory, self.memory)
        result["Boot"] = to_class(Boot, self.boot)
        result["RemoteDisplay"] = to_class(RemoteDisplay, self.remote_display)
        result["BIOS"] = to_class(BIOS, self.bios)
        result["Network"] = to_class(Network, self.network)
        result["AudioAdapter"] = to_class(AudioAdapter, self.audio_adapter)
        result["SharedFolders"] = to_class(SharedFolders, self.shared_folders)
        result["Clipboard"] = from_none(self.clipboard)
        result["GuestProperties"] = to_class(GuestProperties, self.guest_properties)
        result["StorageControllers"] = to_class(StorageControllers, self.storage_controllers)
        return result


class HardDiskHardDisk:
    uuid: str
    location: str
    format: str

    def __init__(self, uuid: str, location: str, format: str) -> None:
        self.uuid = uuid
        self.location = location
        self.format = format

    @staticmethod
    def from_dict(obj: Any) -> 'HardDiskHardDisk':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        location = from_str(obj.get("@location"))
        format = from_str(obj.get("@format"))
        return HardDiskHardDisk(uuid, location, format)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        result["@location"] = from_str(self.location)
        result["@format"] = from_str(self.format)
        return result


class HardDisksHardDisk:
    uuid: str
    location: str
    format: str
    type: str
    hard_disk: HardDiskHardDisk

    def __init__(self, uuid: str, location: str, format: str, type: str, hard_disk: HardDiskHardDisk) -> None:
        self.uuid = uuid
        self.location = location
        self.format = format
        self.type = type
        self.hard_disk = hard_disk

    @staticmethod
    def from_dict(obj: Any) -> 'HardDisksHardDisk':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        location = from_str(obj.get("@location"))
        format = from_str(obj.get("@format"))
        type = from_str(obj.get("@type"))
        hard_disk = HardDiskHardDisk.from_dict(obj.get("HardDisk"))
        return HardDisksHardDisk(uuid, location, format, type, hard_disk)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        result["@location"] = from_str(self.location)
        result["@format"] = from_str(self.format)
        result["@type"] = from_str(self.type)
        result["HardDisk"] = to_class(HardDiskHardDisk, self.hard_disk)
        return result


class HardDisks:
    hard_disk: HardDisksHardDisk

    def __init__(self, hard_disk: HardDisksHardDisk) -> None:
        self.hard_disk = hard_disk

    @staticmethod
    def from_dict(obj: Any) -> 'HardDisks':
        assert isinstance(obj, dict)
        hard_disk = HardDisksHardDisk.from_dict(obj.get("HardDisk"))
        return HardDisks(hard_disk)

    def to_dict(self) -> dict:
        result: dict = {}
        result["HardDisk"] = to_class(HardDisksHardDisk, self.hard_disk)
        return result


class MediaRegistry:
    hard_disks: HardDisks

    def __init__(self, hard_disks: HardDisks) -> None:
        self.hard_disks = hard_disks

    @staticmethod
    def from_dict(obj: Any) -> 'MediaRegistry':
        assert isinstance(obj, dict)
        hard_disks = HardDisks.from_dict(obj.get("HardDisks"))
        return MediaRegistry(hard_disks)

    def to_dict(self) -> dict:
        result: dict = {}
        result["HardDisks"] = to_class(HardDisks, self.hard_disks)
        return result


class Snapshot:
    uuid: str
    name: str
    time_stamp: datetime
    state_file: str
    hardware: Hardware

    def __init__(self, uuid: str, name: str, time_stamp: datetime, state_file: str, hardware: Hardware) -> None:
        self.uuid = uuid
        self.name = name
        self.time_stamp = time_stamp
        self.state_file = state_file
        self.hardware = hardware

    @staticmethod
    def from_dict(obj: Any) -> 'Snapshot':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        name = from_str(obj.get("@name"))
        time_stamp = from_datetime(obj.get("@timeStamp"))
        state_file = from_str(obj.get("@stateFile"))
        hardware = Hardware.from_dict(obj.get("Hardware"))
        return Snapshot(uuid, name, time_stamp, state_file, hardware)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        result["@name"] = from_str(self.name)
        result["@timeStamp"] = self.time_stamp.isoformat()
        result["@stateFile"] = from_str(self.state_file)
        result["Hardware"] = to_class(Hardware, self.hardware)
        return result


class Machine:
    uuid: str
    name: str
    os_type: str
    state_file: str
    current_snapshot: str
    snapshot_folder: str
    current_state_modified: bool
    last_state_change: datetime
    media_registry: MediaRegistry
    extra_data: ExtraData
    snapshot: Snapshot
    hardware: Hardware
    groups: Groups

    def __init__(self, uuid: str, name: str, os_type: str, state_file: str, current_snapshot: str, snapshot_folder: str, current_state_modified: bool, last_state_change: datetime, media_registry: MediaRegistry, extra_data: ExtraData, snapshot: Snapshot, hardware: Hardware, groups: Groups) -> None:
        self.uuid = uuid
        self.name = name
        self.os_type = os_type
        self.state_file = state_file
        self.current_snapshot = current_snapshot
        self.snapshot_folder = snapshot_folder
        self.current_state_modified = current_state_modified
        self.last_state_change = last_state_change
        self.media_registry = media_registry
        self.extra_data = extra_data
        self.snapshot = snapshot
        self.hardware = hardware
        self.groups = groups

    @staticmethod
    def from_dict(obj: Any) -> 'Machine':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("@uuid"))
        name = from_str(obj.get("@name"))
        os_type = from_str(obj.get("@OSType"))
        state_file = from_str(obj.get("@stateFile"))
        current_snapshot = from_str(obj.get("@currentSnapshot"))
        snapshot_folder = from_str(obj.get("@snapshotFolder"))
        current_state_modified = from_stringified_bool(from_str(obj.get("@currentStateModified")))
        last_state_change = from_datetime(obj.get("@lastStateChange"))
        media_registry = MediaRegistry.from_dict(obj.get("MediaRegistry"))
        extra_data = ExtraData.from_dict(obj.get("ExtraData"))
        snapshot = Snapshot.from_dict(obj.get("Snapshot"))
        hardware = Hardware.from_dict(obj.get("Hardware"))
        groups = Groups.from_dict(obj.get("Groups"))
        return Machine(uuid, name, os_type, state_file, current_snapshot, snapshot_folder, current_state_modified, last_state_change, media_registry, extra_data, snapshot, hardware, groups)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@uuid"] = from_str(self.uuid)
        result["@name"] = from_str(self.name)
        result["@OSType"] = from_str(self.os_type)
        result["@stateFile"] = from_str(self.state_file)
        result["@currentSnapshot"] = from_str(self.current_snapshot)
        result["@snapshotFolder"] = from_str(self.snapshot_folder)
        result["@currentStateModified"] = from_str(str(self.current_state_modified).lower())
        result["@lastStateChange"] = self.last_state_change.isoformat()
        result["MediaRegistry"] = to_class(MediaRegistry, self.media_registry)
        result["ExtraData"] = to_class(ExtraData, self.extra_data)
        result["Snapshot"] = to_class(Snapshot, self.snapshot)
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


class Welcome1:
    virtual_box: VirtualBox

    def __init__(self, virtual_box: VirtualBox) -> None:
        self.virtual_box = virtual_box

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome1':
        assert isinstance(obj, dict)
        virtual_box = VirtualBox.from_dict(obj.get("VirtualBox"))
        return Welcome1(virtual_box)

    def to_dict(self) -> dict:
        result: dict = {}
        result["VirtualBox"] = to_class(VirtualBox, self.virtual_box)
        return result


def welcome1_from_dict(s: Any) -> Welcome1:
    return Welcome1.from_dict(s)


def welcome1_to_dict(x: Welcome1) -> Any:
    return to_class(Welcome1, x)

