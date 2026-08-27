"""Load fictional demo inventory for local development.

Safe to re-run: records are keyed on unique serials, emails, and names.
Pass --reset to delete previously seeded demo rows first.
"""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from assets.models import (
    UPS,
    AccessPoint,
    Branch,
    Camera,
    Desktop,
    DesktopStorage,
    Employee,
    Firewall,
    Laptop,
    LaptopStorage,
    NotificationConfig,
    NotificationRecipient,
    NVR,
    ColocationVM,
    Router,
    Screen,
    Server,
    Switch,
    Telephone,
    VirtualMachine,
    ZKDevice,
)

User = get_user_model()

BRANCH_NAMES = ("Headquarters", "Downtown", "Warehouse")
DEMO_EMAIL_DOMAIN = "@example.com"
SERIAL_PREFIX = "DEMO-"


class Command(BaseCommand):
    help = "Load fictional demo inventory for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete previously seeded demo records before inserting.",
        )
        parser.add_argument(
            "--password",
            default="demo12345",
            help="Password for demo users (default: demo12345).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            self._reset()
            self.stdout.write(self.style.WARNING("Removed previous demo records."))

        created_by = self._users(options["password"])
        branches = self._branches()
        employees = self._employees(branches, created_by)
        self._endpoints(branches, employees, created_by)
        self._infrastructure(branches, created_by)
        self._compute(branches, created_by)
        self._notifications()
        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
        self.stdout.write("Sign in as demo.admin / %s" % options["password"])

    def _reset(self):
        VirtualMachine.objects.filter(name__startswith="demo-").delete()
        Server.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        Laptop.objects.filter(serial__startswith=SERIAL_PREFIX).delete()
        Desktop.objects.filter(serial__startswith=SERIAL_PREFIX).delete()
        Screen.objects.filter(serial__startswith=SERIAL_PREFIX).delete()
        Telephone.objects.filter(serial__startswith=SERIAL_PREFIX).delete()
        Camera.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        NVR.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        Firewall.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        Switch.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        AccessPoint.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        Router.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        UPS.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        ZKDevice.objects.filter(serial_number__startswith=SERIAL_PREFIX).delete()
        ColocationVM.objects.filter(name__startswith="demo-").delete()
        NotificationRecipient.objects.filter(email__endswith=DEMO_EMAIL_DOMAIN).delete()
        NotificationConfig.objects.filter(
            notification_message__startswith="[demo]"
        ).delete()
        Employee.objects.filter(email__endswith=DEMO_EMAIL_DOMAIN).delete()

    def _users(self, password):
        admin, created = User.objects.get_or_create(
            username="demo.admin",
            defaults={
                "email": "demo.admin@example.com",
                "first_name": "Demo",
                "last_name": "Admin",
                "role": "super_admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password(password)
            admin.save()
        else:
            if admin.role != "super_admin":
                admin.role = "super_admin"
                admin.is_staff = True
                admin.is_superuser = True
                admin.save(update_fields=["role", "is_staff", "is_superuser"])

        viewer, viewer_created = User.objects.get_or_create(
            username="demo.user",
            defaults={
                "email": "demo.user@example.com",
                "first_name": "Demo",
                "last_name": "Viewer",
                "role": "user",
            },
        )
        if viewer_created:
            viewer.set_password(password)
            viewer.save()

        return admin

    def _branches(self):
        return {
            name: Branch.objects.get_or_create(name=name, defaults={"choosable": True})[0]
            for name in BRANCH_NAMES
        }

    def _employees(self, branches, created_by):
        specs = [
            ("Alex Rivera", "IT", "Systems Engineer", "alex.rivera", "Headquarters"),
            ("Jordan Lee", "Finance", "Accountant", "jordan.lee", "Headquarters"),
            ("Sam Patel", "Operations", "Branch Manager", "sam.patel", "Downtown"),
            ("Riley Chen", "IT", "Helpdesk", "riley.chen", "Downtown"),
            ("Morgan Blake", "Warehouse", "Storekeeper", "morgan.blake", "Warehouse"),
        ]
        employees = {}
        for name, department, title, local, branch_name in specs:
            employee, _ = Employee.objects.get_or_create(
                email=f"{local}{DEMO_EMAIL_DOMAIN}",
                defaults={
                    "name": name,
                    "department": department,
                    "title": title,
                    "branch": branches[branch_name],
                    "created_by": created_by,
                },
            )
            employees[local] = employee
        return employees

    def _endpoints(self, branches, employees, created_by):
        hq = branches["Headquarters"]
        downtown = branches["Downtown"]
        warehouse = branches["Warehouse"]

        laptops = [
            {
                "product": "ThinkPad T14",
                "serial": f"{SERIAL_PREFIX}LT-0001",
                "cpu": Laptop.Cpu.I7,
                "cpu_generation": Laptop.CpuGeneration.GEN_12,
                "ram": Laptop.Ram.GB_16,
                "employee": employees["alex.rivera"],
                "branch": hq,
            },
            {
                "product": "ThinkPad E14",
                "serial": f"{SERIAL_PREFIX}LT-0002",
                "cpu": Laptop.Cpu.I5,
                "cpu_generation": Laptop.CpuGeneration.GEN_11,
                "ram": Laptop.Ram.GB_8,
                "employee": employees["sam.patel"],
                "branch": downtown,
            },
            {
                "product": "Latitude 5540",
                "serial": f"{SERIAL_PREFIX}LT-0003",
                "cpu": Laptop.Cpu.I5,
                "cpu_generation": Laptop.CpuGeneration.GEN_13,
                "ram": Laptop.Ram.GB_16,
                "branch": warehouse,
            },
        ]
        for spec in laptops:
            laptop, created = Laptop.objects.get_or_create(
                serial=spec["serial"],
                defaults={
                    **spec,
                    "warranty": date.today() + timedelta(days=365),
                    "created_by": created_by,
                    "comments": "Demo laptop",
                },
            )
            if created:
                LaptopStorage.objects.create(
                    laptop=laptop,
                    type=LaptopStorage.StorageType.SSD,
                    size=LaptopStorage.StorageSize.GB_512,
                )

        desktops = [
            {
                "product": "OptiPlex 7010",
                "serial": f"{SERIAL_PREFIX}DT-0001",
                "cpu": Desktop.Cpu.I7,
                "cpu_generation": Desktop.CpuGeneration.GEN_12,
                "ram": Desktop.Ram.GB_16,
                "employee": employees["jordan.lee"],
                "branch": hq,
            },
            {
                "product": "OptiPlex 5090",
                "serial": f"{SERIAL_PREFIX}DT-0002",
                "cpu": Desktop.Cpu.I5,
                "cpu_generation": Desktop.CpuGeneration.GEN_10,
                "ram": Desktop.Ram.GB_8,
                "branch": downtown,
            },
        ]
        for spec in desktops:
            desktop, created = Desktop.objects.get_or_create(
                serial=spec["serial"],
                defaults={
                    **spec,
                    "warranty": date.today() + timedelta(days=730),
                    "created_by": created_by,
                    "comments": "Demo desktop",
                },
            )
            if created:
                DesktopStorage.objects.create(
                    desktop=desktop,
                    type=DesktopStorage.StorageType.SSD,
                    size=DesktopStorage.StorageSize.GB_256,
                )

        screens = [
            ("SCR-0001", Screen.Product.SCREEN, employees["jordan.lee"], hq),
            ("SCR-0002", Screen.Product.SCREEN, employees["sam.patel"], downtown),
            ("SCR-0003", Screen.Product.SCREEN_PC, None, warehouse),
        ]
        for serial, product, employee, branch in screens:
            Screen.objects.get_or_create(
                serial=f"{SERIAL_PREFIX}{serial}",
                defaults={
                    "product": product,
                    "brand": "Dell",
                    "employee": employee,
                    "branch": branch,
                    "created_by": created_by,
                },
            )

        phones = [
            ("TEL-0001", employees["alex.rivera"], hq),
            ("TEL-0002", employees["riley.chen"], downtown),
            ("TEL-0003", None, warehouse),
        ]
        for serial, employee, branch in phones:
            Telephone.objects.get_or_create(
                serial=f"{SERIAL_PREFIX}{serial}",
                defaults={
                    "product": "IP Phone 8841",
                    "brand": "Cisco",
                    "employee": employee,
                    "branch": branch,
                    "created_by": created_by,
                },
            )

    def _infrastructure(self, branches, created_by):
        hq = branches["Headquarters"]
        downtown = branches["Downtown"]
        warehouse = branches["Warehouse"]
        today = date.today()

        Camera.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}CAM-0001",
            defaults={
                "model": "DS-2CD2143G2",
                "location": "Lobby",
                "ip_address": "10.10.20.11",
                "status": Camera.Status.IN_USE,
                "power_source": "PoE",
                "branch": hq,
                "created_by": created_by,
            },
        )
        Camera.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}CAM-0002",
            defaults={
                "model": "DS-2CD2143G2",
                "location": "Loading dock",
                "ip_address": "10.10.30.11",
                "status": Camera.Status.IN_USE,
                "power_source": "PoE",
                "branch": warehouse,
                "created_by": created_by,
            },
        )
        NVR.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}NVR-0001",
            defaults={
                "model": "DS-7608NI",
                "location": "Server room",
                "ip_address": "10.10.20.12",
                "status": NVR.Status.IN_USE,
                "hdd_capacity": "8 TB",
                "number_of_ports": 8,
                "branch": hq,
                "created_by": created_by,
            },
        )
        Firewall.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}FW-0001",
            defaults={
                "model": "FortiGate 60F",
                "location": "Server room",
                "ip_address": "10.10.20.1",
                "status": Firewall.Status.IN_USE,
                "firmware_version": "7.2.8",
                "number_of_ports": 10,
                "license_expiry_date": today + timedelta(days=200),
                "branch": hq,
                "created_by": created_by,
            },
        )
        Switch.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}SW-0001",
            defaults={
                "model": "Catalyst 9200",
                "location": "Rack A1",
                "ip_address": "10.10.20.2",
                "status": Switch.Status.IN_USE,
                "number_of_ports": 48,
                "number_of_poe_ports": 24,
                "branch": hq,
                "created_by": created_by,
            },
        )
        Switch.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}SW-0002",
            defaults={
                "model": "Catalyst 9200",
                "location": "IDF",
                "ip_address": "10.10.21.2",
                "status": Switch.Status.IN_USE,
                "number_of_ports": 24,
                "number_of_poe_ports": 24,
                "branch": downtown,
                "created_by": created_by,
            },
        )
        AccessPoint.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}AP-0001",
            defaults={
                "model": "Meraki MR36",
                "location": "Open office",
                "ip_address": "10.10.20.30",
                "status": AccessPoint.Status.IN_USE,
                "expiry_date": today + timedelta(days=400),
                "branch": hq,
                "created_by": created_by,
            },
        )
        Router.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}RT-0001",
            defaults={
                "model": "ISR 4331",
                "location": "Server room",
                "ip_address": "10.10.20.3",
                "status": Router.Status.IN_USE,
                "branch": hq,
                "created_by": created_by,
            },
        )
        UPS.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}UPS-0001",
            defaults={
                "model": "APC SMT1500",
                "location": "Server room",
                "ip_address": "10.10.20.40",
                "status": UPS.Status.IN_USE,
                "voltage": 220,
                "power_source": UPS.PowerSource.UTILITY,
                "last_maintenance_date": today - timedelta(days=90),
                "next_maintenance_date": today + timedelta(days=90),
                "branch": hq,
                "created_by": created_by,
            },
        )
        ZKDevice.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}ZK-0001",
            defaults={
                "model": "ZKTeco MB360",
                "location": "Main entrance",
                "ip_address": "10.10.20.50",
                "status": ZKDevice.Status.IN_USE,
                "device_type": ZKDevice.DeviceType.ATTENDANCE,
                "vendor": "ZKTeco",
                "branch": hq,
                "created_by": created_by,
            },
        )

    def _compute(self, branches, created_by):
        hq = branches["Headquarters"]
        host, created = Server.objects.get_or_create(
            serial_number=f"{SERIAL_PREFIX}SRV-0001",
            defaults={
                "model": "PowerEdge R750",
                "hostname": "demo-esxi-01",
                "location": "Rack A2",
                "ip_address": "10.10.20.100",
                "status": Server.Status.IN_USE,
                "cpu_cores": 32,
                "ram_gb": 256,
                "storage_gb": 4096,
                "hypervisor": Server.Hypervisor.VMWARE,
                "branch": hq,
                "created_by": created_by,
                "comment": "Demo hypervisor",
            },
        )
        if created or not VirtualMachine.objects.filter(server=host).exists():
            VirtualMachine.objects.get_or_create(
                server=host,
                name="demo-ad-01",
                defaults={
                    "ip_address": "10.10.20.101",
                    "operating_system": "Windows Server 2022",
                    "vcpu": 4,
                    "vram_gb": 16,
                    "storage_gb": 200,
                    "environment": VirtualMachine.Environment.PROD,
                    "status": VirtualMachine.Status.RUNNING,
                },
            )
            VirtualMachine.objects.get_or_create(
                server=host,
                name="demo-app-01",
                defaults={
                    "ip_address": "10.10.20.102",
                    "operating_system": "Ubuntu 24.04",
                    "vcpu": 8,
                    "vram_gb": 32,
                    "storage_gb": 400,
                    "environment": VirtualMachine.Environment.PROD,
                    "status": VirtualMachine.Status.RUNNING,
                },
            )
            VirtualMachine.objects.get_or_create(
                server=host,
                name="demo-uat-01",
                defaults={
                    "ip_address": "10.10.20.110",
                    "operating_system": "Ubuntu 24.04",
                    "vcpu": 4,
                    "vram_gb": 8,
                    "storage_gb": 120,
                    "environment": VirtualMachine.Environment.UAT,
                    "status": VirtualMachine.Status.STOPPED,
                },
            )
            host.update_available_resources()

        ColocationVM.objects.get_or_create(
            name="demo-dc-core",
            defaults={
                "ip_address": "172.16.8.10",
                "vcpu": 8,
                "vram_gb": 32,
                "allocated_storage_gb": 500,
                "operating_system": "Ubuntu Linux",
                "environment": ColocationVM.Environment.PROD,
                "contract_start": date.today() - timedelta(days=180),
                "contract_end": date.today() + timedelta(days=185),
                "renewal_date": date.today() + timedelta(days=150),
                "created_by": created_by,
            },
        )

    def _notifications(self):
        configs = []
        for model_name, threshold in (
            ("Laptop", "2"),
            ("Desktop", "1"),
            ("Screen", "2"),
        ):
            config, _ = NotificationConfig.objects.get_or_create(
                model_name=model_name,
                condition_type="stock_count",
                condition_value=threshold,
                defaults={
                    "is_active": True,
                    "notification_message": f"[demo] {model_name} stock is at or below {threshold}.",
                },
            )
            configs.append(config)

        recipient, _ = NotificationRecipient.objects.get_or_create(
            email="it-alerts@example.com",
            defaults={"is_active": True},
        )
        recipient.models_to_notify.set(configs)
