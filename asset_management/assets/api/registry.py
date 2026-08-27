"""Single place where every API resource is registered.

The UI reads this registry through the schema endpoint, so adding a ViewSet
here is all that is needed for it to appear in the web app.
"""

from rest_framework.routers import DefaultRouter

from users.api_views import UserViewSet

from .access_points import AccessPointViewSet
from .branches import BranchViewSet
from .cameras import CameraViewSet
from .desktops import DesktopViewSet
from .employees import EmployeeViewSet
from .firewalls import FirewallViewSet
from .laptops import LaptopViewSet
from .notifications import (
    NotificationConfigViewSet,
    NotificationRecipientViewSet,
    SentNotificationViewSet,
)
from .nvrs import NVRViewSet
from .colocation import ColocationVMViewSet
from .routers import RouterViewSet
from .screens import ScreenViewSet
from .servers import ServerViewSet
from .switches import SwitchViewSet
from .telephones import TelephoneViewSet
from .ups import UPSViewSet
from .virtual_machines import VirtualMachineViewSet
from .zk_devices import ZKDeviceViewSet

router = DefaultRouter()

router.register("branches", BranchViewSet, basename="branch")
router.register("employees", EmployeeViewSet, basename="employee")

router.register("laptops", LaptopViewSet, basename="laptop")
router.register("desktops", DesktopViewSet, basename="desktop")
router.register("screens", ScreenViewSet, basename="screen")
router.register("telephones", TelephoneViewSet, basename="telephone")

router.register("cameras", CameraViewSet, basename="camera")
router.register("nvrs", NVRViewSet, basename="nvr")
router.register("firewalls", FirewallViewSet, basename="firewall")
router.register("switches", SwitchViewSet, basename="switch")
router.register("access-points", AccessPointViewSet, basename="access-point")
router.register("routers", RouterViewSet, basename="router")
router.register("ups", UPSViewSet, basename="ups")
router.register("zk-devices", ZKDeviceViewSet, basename="zk-device")

router.register("servers", ServerViewSet, basename="server")
router.register("virtual-machines", VirtualMachineViewSet, basename="virtual-machine")
router.register("colocation-vms", ColocationVMViewSet, basename="colocation-vm")

router.register(
    "notification-configs", NotificationConfigViewSet, basename="notification-config"
)
router.register(
    "notification-recipients",
    NotificationRecipientViewSet,
    basename="notification-recipient",
)
router.register(
    "sent-notifications", SentNotificationViewSet, basename="sent-notification"
)

router.register("users", UserViewSet, basename="user")


def registered_resources():
    """Yield ``(prefix, viewset)`` for every registered resource."""
    for prefix, viewset, _basename in router.registry:
        yield prefix, viewset


def model_to_prefix():
    """Map each model class onto its URL prefix, for relation lookups."""
    mapping = {}
    for prefix, viewset in registered_resources():
        queryset = getattr(viewset, "queryset", None)
        if queryset is not None:
            mapping[queryset.model] = prefix
    return mapping
