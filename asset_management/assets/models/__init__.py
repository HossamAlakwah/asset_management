from .access_point import AccessPoint, AccessPointLog
from .branch import Branch
from .camera import Camera, CameraLog
from .colocation import ColocationVM
from .desktop import Desktop, DesktopLog, DesktopStorage
from .employee import Employee
from .firewall import Firewall, FirewallLog
from .laptop import Laptop, LaptopLog, LaptopStorage
from .notifications import NotificationConfig, NotificationRecipient, SentNotification
from .nvr import NVR, NVRLog
from .router import Router, RouterLog
from .screen import Screen, ScreenLog
from .server import Server, ServerLog
from .switch import Switch, SwitchLog
from .telephone import Telephone, TelephoneLog
from .ups import UPS, UPSLog
from .virtual_machine import VirtualMachine, VirtualMachineLog
from .zk_device import ZKDevice, ZKDeviceLog

__all__ = [
    "AccessPoint",
    "AccessPointLog",
    "Branch",
    "Camera",
    "CameraLog",
    "ColocationVM",
    "Desktop",
    "DesktopLog",
    "DesktopStorage",
    "Employee",
    "Firewall",
    "FirewallLog",
    "Laptop",
    "LaptopLog",
    "LaptopStorage",
    "NotificationConfig",
    "NotificationRecipient",
    "NVR",
    "NVRLog",
    "Router",
    "RouterLog",
    "Screen",
    "ScreenLog",
    "SentNotification",
    "Server",
    "ServerLog",
    "Switch",
    "SwitchLog",
    "Telephone",
    "TelephoneLog",
    "UPS",
    "UPSLog",
    "VirtualMachine",
    "VirtualMachineLog",
    "ZKDevice",
    "ZKDeviceLog",
]
