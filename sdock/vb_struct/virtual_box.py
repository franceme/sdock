from dataclasses import dataclass, field
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDateTime


@dataclass
class AudioAdapter:
    driver: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ExtraDataItem:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Group:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class GuestProperty:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[Union[int, str, bool]] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    timestamp: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    flags: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class HardDisk:
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    format: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    hard_disk: Optional["HardDisk"] = field(
        default=None,
        metadata={
            "name": "HardDisk",
            "type": "Element",
        }
    )


@dataclass
class HardwareVirtExLargePages:
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Ioapic:
    class Meta:
        name = "IOAPIC"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Image:
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class InternalNetwork:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class LongMode:
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Memory:
    ramsize: Optional[int] = field(
        default=None,
        metadata={
            "name": "RAMSize",
            "type": "Attribute",
        }
    )


@dataclass
class Nat:
    class Meta:
        name = "NAT"

    localhost_reachable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "localhost-reachable",
            "type": "Attribute",
        }
    )


@dataclass
class Natnetwork:
    class Meta:
        name = "NATNetwork"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Order:
    position: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    device: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Pae:
    class Meta:
        name = "PAE"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Property:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class SharedFolder:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    host_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "hostPath",
            "type": "Attribute",
        }
    )
    writable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    auto_mount: Optional[bool] = field(
        default=None,
        metadata={
            "name": "autoMount",
            "type": "Attribute",
        }
    )


@dataclass
class AttachedDevice:
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    hotpluggable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    port: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    device: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    image: Optional[Image] = field(
        default=None,
        metadata={
            "name": "Image",
            "type": "Element",
        }
    )


@dataclass
class Bios:
    class Meta:
        name = "BIOS"

    ioapic: Optional[Ioapic] = field(
        default=None,
        metadata={
            "name": "IOAPIC",
            "type": "Element",
        }
    )


@dataclass
class Boot:
    order: List[Order] = field(
        default_factory=list,
        metadata={
            "name": "Order",
            "type": "Element",
        }
    )


@dataclass
class Cpu:
    class Meta:
        name = "CPU"

    pae: Optional[Pae] = field(
        default=None,
        metadata={
            "name": "PAE",
            "type": "Element",
        }
    )
    long_mode: Optional[LongMode] = field(
        default=None,
        metadata={
            "name": "LongMode",
            "type": "Element",
        }
    )
    hardware_virt_ex_large_pages: Optional[HardwareVirtExLargePages] = field(
        default=None,
        metadata={
            "name": "HardwareVirtExLargePages",
            "type": "Element",
        }
    )


@dataclass
class DisabledModes:
    nat: Optional[Nat] = field(
        default=None,
        metadata={
            "name": "NAT",
            "type": "Element",
        }
    )
    internal_network: Optional[InternalNetwork] = field(
        default=None,
        metadata={
            "name": "InternalNetwork",
            "type": "Element",
        }
    )
    natnetwork: Optional[Natnetwork] = field(
        default=None,
        metadata={
            "name": "NATNetwork",
            "type": "Element",
        }
    )


@dataclass
class ExtraData:
    extra_data_item: List[ExtraDataItem] = field(
        default_factory=list,
        metadata={
            "name": "ExtraDataItem",
            "type": "Element",
        }
    )


@dataclass
class Groups:
    group: Optional[Group] = field(
        default=None,
        metadata={
            "name": "Group",
            "type": "Element",
        }
    )


@dataclass
class GuestProperties:
    guest_property: List[GuestProperty] = field(
        default_factory=list,
        metadata={
            "name": "GuestProperty",
            "type": "Element",
        }
    )


@dataclass
class HardDisks:
    hard_disk: Optional[HardDisk] = field(
        default=None,
        metadata={
            "name": "HardDisk",
            "type": "Element",
        }
    )


@dataclass
class SharedFolders:
    shared_folder: Optional[SharedFolder] = field(
        default=None,
        metadata={
            "name": "SharedFolder",
            "type": "Element",
        }
    )


@dataclass
class Vrdeproperties:
    class Meta:
        name = "VRDEProperties"

    property: List[Property] = field(
        default_factory=list,
        metadata={
            "name": "Property",
            "type": "Element",
        }
    )


@dataclass
class Adapter:
    slot: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    macaddress: Optional[str] = field(
        default=None,
        metadata={
            "name": "MACAddress",
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    disabled_modes: Optional[DisabledModes] = field(
        default=None,
        metadata={
            "name": "DisabledModes",
            "type": "Element",
        }
    )


@dataclass
class MediaRegistry:
    hard_disks: Optional[HardDisks] = field(
        default=None,
        metadata={
            "name": "HardDisks",
            "type": "Element",
        }
    )


@dataclass
class RemoteDisplay:
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    vrdeproperties: Optional[Vrdeproperties] = field(
        default=None,
        metadata={
            "name": "VRDEProperties",
            "type": "Element",
        }
    )


@dataclass
class StorageController:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    port_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "PortCount",
            "type": "Attribute",
        }
    )
    use_host_iocache: Optional[bool] = field(
        default=None,
        metadata={
            "name": "useHostIOCache",
            "type": "Attribute",
        }
    )
    bootable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Bootable",
            "type": "Attribute",
        }
    )
    attached_device: Optional[AttachedDevice] = field(
        default=None,
        metadata={
            "name": "AttachedDevice",
            "type": "Element",
        }
    )


@dataclass
class Network:
    adapter: Optional[Adapter] = field(
        default=None,
        metadata={
            "name": "Adapter",
            "type": "Element",
        }
    )


@dataclass
class StorageControllers:
    storage_controller: Optional[StorageController] = field(
        default=None,
        metadata={
            "name": "StorageController",
            "type": "Element",
        }
    )


@dataclass
class Hardware:
    cpu: Optional[Cpu] = field(
        default=None,
        metadata={
            "name": "CPU",
            "type": "Element",
        }
    )
    memory: Optional[Memory] = field(
        default=None,
        metadata={
            "name": "Memory",
            "type": "Element",
        }
    )
    boot: Optional[Boot] = field(
        default=None,
        metadata={
            "name": "Boot",
            "type": "Element",
        }
    )
    remote_display: Optional[RemoteDisplay] = field(
        default=None,
        metadata={
            "name": "RemoteDisplay",
            "type": "Element",
        }
    )
    bios: Optional[Bios] = field(
        default=None,
        metadata={
            "name": "BIOS",
            "type": "Element",
        }
    )
    network: Optional[Network] = field(
        default=None,
        metadata={
            "name": "Network",
            "type": "Element",
        }
    )
    audio_adapter: Optional[AudioAdapter] = field(
        default=None,
        metadata={
            "name": "AudioAdapter",
            "type": "Element",
        }
    )
    shared_folders: Optional[SharedFolders] = field(
        default=None,
        metadata={
            "name": "SharedFolders",
            "type": "Element",
        }
    )
    clipboard: Optional[object] = field(
        default=None,
        metadata={
            "name": "Clipboard",
            "type": "Element",
        }
    )
    guest_properties: Optional[GuestProperties] = field(
        default=None,
        metadata={
            "name": "GuestProperties",
            "type": "Element",
        }
    )
    storage_controllers: Optional[StorageControllers] = field(
        default=None,
        metadata={
            "name": "StorageControllers",
            "type": "Element",
        }
    )


@dataclass
class Snapshot:
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    time_stamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "timeStamp",
            "type": "Attribute",
        }
    )
    state_file: Optional[str] = field(
        default=None,
        metadata={
            "name": "stateFile",
            "type": "Attribute",
        }
    )
    hardware: Optional[Hardware] = field(
        default=None,
        metadata={
            "name": "Hardware",
            "type": "Element",
        }
    )


@dataclass
class Machine:
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ostype: Optional[str] = field(
        default=None,
        metadata={
            "name": "OSType",
            "type": "Attribute",
        }
    )
    state_file: Optional[str] = field(
        default=None,
        metadata={
            "name": "stateFile",
            "type": "Attribute",
        }
    )
    current_snapshot: Optional[str] = field(
        default=None,
        metadata={
            "name": "currentSnapshot",
            "type": "Attribute",
        }
    )
    snapshot_folder: Optional[str] = field(
        default=None,
        metadata={
            "name": "snapshotFolder",
            "type": "Attribute",
        }
    )
    current_state_modified: Optional[bool] = field(
        default=None,
        metadata={
            "name": "currentStateModified",
            "type": "Attribute",
        }
    )
    last_state_change: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lastStateChange",
            "type": "Attribute",
        }
    )
    media_registry: Optional[MediaRegistry] = field(
        default=None,
        metadata={
            "name": "MediaRegistry",
            "type": "Element",
        }
    )
    extra_data: Optional[ExtraData] = field(
        default=None,
        metadata={
            "name": "ExtraData",
            "type": "Element",
        }
    )
    snapshot: Optional[Snapshot] = field(
        default=None,
        metadata={
            "name": "Snapshot",
            "type": "Element",
        }
    )
    hardware: Optional[Hardware] = field(
        default=None,
        metadata={
            "name": "Hardware",
            "type": "Element",
        }
    )
    groups: Optional[Groups] = field(
        default=None,
        metadata={
            "name": "Groups",
            "type": "Element",
        }
    )


@dataclass
class VirtualBox:
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    machine: Optional[Machine] = field(
        default=None,
        metadata={
            "name": "Machine",
            "type": "Element",
        }
    )
