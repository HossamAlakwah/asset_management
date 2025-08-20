from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify

today = timezone.now().date()
from users.models import CustomUser as User


# models.py
class FieldBehavior(models.Model):
    model_name = models.CharField(max_length=100)  # e.g. "UPS"
    field_name = models.CharField(max_length=100)  # e.g. "voltage"
    is_required = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('model_name', 'field_name')
        ordering = ['model_name', 'field_name']

    def __str__(self):
        return f"{self.model_name}.{self.field_name}"
'''

Branches table to store different branches of the company.

This table will be used to categorize assets based on their location.

'''
class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=False, blank=True)
    created_at = models.DateTimeField(default=timezone.now)  
    choosable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = self.name.replace(' ', '-')
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['id']
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=False)  

    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return self.name
    
'''

Asset table to store information about assets.
Laptops and desktops will be stored in this table.
and logs will be created for each asset change.

'''
class StorageDevice(models.Model):
    STORAGE_TYPE_CHOICES = [
        ('HDD', 'HDD'),
        ('SSD', 'SSD'),
    ]

    STORAGE_SIZE_CHOICES = [
        ('128', '128 GB'),
        ('256', '256 GB'),
        ('512', '512 GB'),
        ('1TB', '1 TB'),
    ]

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name='storage_devices')
    type = models.CharField(max_length=10, choices=STORAGE_TYPE_CHOICES)
    size = models.CharField(max_length=10, choices=STORAGE_SIZE_CHOICES)

    def __str__(self):
        return f"{self.size} {self.type}"

class Asset(models.Model):
    ASSET_STATUS_CHOICES = [
        ('In Use', 'In Use'),
        ('Stock', 'Stock'),
        ('Damage', 'Damage'),
    ]
    
    ASSET_TYPE_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
    ]
    
    CPU_CHOICES = [
        ('i3', 'Intel Core i3'),
        ('i5', 'Intel Core i5'),
        ('i7', 'Intel Core i7'),
        ('i9', 'Intel Core i9'),

    ]

    CPU_GEN_CHOICES = [
        ('1',  '1th Gen'),
        ('2',  '2th Gen'),
        ('3',  '3th Gen'),
        ('4',  '4th Gen'),
        ('5',  '5th Gen'),
        ('6',  '6th Gen'),
        ('7',  '7th Gen'),
        ('8',  '8th Gen'),
        ('9',  '9th Gen'),
        ('10', '10th Gen'),
        ('11', '11th Gen'),
        ('12', '12th Gen'),
        ('13', '13th Gen'),
    ]
    RAM_CHOICES = [
        ('4GB', '4 GB'),
        ('8GB', '8 GB'),
        ('16GB', '16 GB'),
        ('32GB', '32 GB'),
    ]
    
    STORAGE_CHOICES = [
        ('128', '128 GB'),
        ('256', '256 GB'),
        ('512', '512 GB'),
        ('1TB', '1 TB'),
    ]

    STORAGE_TYPE = [
        ('HDD', 'HDD'),
        ('SSD', 'SSD'),
    ] 
    
    product = models.CharField(max_length=255)
    serial = models.CharField(max_length=255, unique=True)
    cpu= models.CharField(max_length=20, choices=CPU_CHOICES,blank=True, null=True)    
    cpu_generation = models.CharField(max_length=3,  choices=CPU_GEN_CHOICES,blank=True, null=True)
    ram = models.CharField(max_length=10, choices=RAM_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ASSET_STATUS_CHOICES)
    employee_name = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    warranty = models.DateField(blank=True, null=True)
    on_hand_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=False)
    type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL, related_name='created_assets')

    def save(self, *args, **kwargs):
        if self.employee_name and self.employee_name.branch:
            self.branch = self.employee_name.branch
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'

    def __str__(self):
        return f"{self.product} - {self.serial}"


class AssetLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='logs')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    old_employee = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_employee_logs'
    )
    new_employee = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_employee_logs'
    )
    on_hand_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    change_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-change_time']
        verbose_name = 'Asset Log'
        verbose_name_plural = 'Asset Logs'

    def __str__(self):
        return f"Log for {self.asset.serial} at {self.change_time}"
    
    
    
# Which models (tables) are reportable
class ReportableModel(models.Model):
    name = models.CharField(max_length=100)       # e.g. "Asset"
    model_path = models.CharField(
        max_length=100,
        help_text="Dotted path to model, e.g. 'assets.Asset'"
    )
    def __str__(self):
        return self.model_path

# Which fields (columns) can be shown
class ReportableField(models.Model):
    FIELD_TYPE_CHOICES = [
        ('char', 'CharField / Text'),
        ('choice', 'Choice Field (dropdown)'),
        ('foreign', 'ForeignKey (name/display)'),
        ('date', 'Date Field'),
        ('numeric', 'Integer / Float'),
    ]

    model = models.ForeignKey(
        ReportableModel,
        on_delete=models.CASCADE,
        related_name='fields'
    )
    field_name = models.CharField(
        max_length=100,
        help_text="Exact field or dotted path (e.g. 'branch__name')"
    )
    display_name = models.CharField(
        max_length=100,
        help_text="Human-readable name for UI"
    )
    is_filter = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    field_type = models.CharField(
        max_length=20,
        choices=FIELD_TYPE_CHOICES,
        default='char'
    )
    choices = models.JSONField(
        blank=True,
        null=True,
        help_text="Only for 'choice' fields: list of allowed values"
    )

    def __str__(self):
        return f"{self.model.name} - {self.display_name}"


'''

Screens table to store information about screens.
screens, printers, and screen-PCs will be stored in this table.
log will be created for each screen change.

'''
class Screen(models.Model):
    PRODUCT_CHOICES = [
        ('Screen', 'Screen'),
        ('Screen-PC', 'Screen-PC'),
    ]

    STATUS_CHOICES = [
        ('In Use', 'In Use'),
        ('Damage', 'Damage'),
        ('Stock', 'Stock'),
    ]

    product = models.CharField(max_length=50, choices=PRODUCT_CHOICES,blank=False, null=False)
    serial = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    brand= models.CharField(max_length=50, blank=False, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='created_screens')


    def save(self, *args, **kwargs):
        if self.employee and self.employee.branch:
            self.branch = self.employee.branch
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Screen'
        verbose_name_plural = 'Screens'

    def __str__(self):
        return f"{self.product} - {self.serial}"


class ScreenLog(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='logs')

    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)

    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)

    old_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='screen_old_employee_logs'
    )
    new_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='screen_new_employee_logs'
    )

    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    change_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-change_time']
        verbose_name = 'Screen Log'
        verbose_name_plural = 'Screen Logs'

    def __str__(self):
        return f"Log for {self.screen.serial} at {self.change_time.strftime('%Y-%m-%d %H:%M')}"


'''

telephones table to store information about telephones.
telephones, printers, and screen-PCs will be stored in this table.
log will be created for each screen change.

'''
class Telephone(models.Model):

    STATUS_CHOICES = [
        ('In Use', 'In Use'),
        ('Damage', 'Damage'),
        ('Stock', 'Stock'),
    ]

    product = models.CharField(max_length=50,blank=False, null=False)
    serial = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    brand= models.CharField(max_length=50, blank=False, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='created_telephones')


    def save(self, *args, **kwargs):
        if self.employee and self.employee.branch:
            self.branch = self.employee.branch
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Telephone'
        verbose_name_plural = 'Telephone'

    def __str__(self):
        return f"{self.product} - {self.serial}"


class TelephoneLog(models.Model):
    telephone = models.ForeignKey(Telephone, on_delete=models.CASCADE, related_name='logs')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)

    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)

    old_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='telephone_old_employee_logs'
    )
    new_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='telephone_new_employee_logs'
    )

    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    change_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-change_time']
        verbose_name = 'telephone Log'
        verbose_name_plural = 'telephone Logs'

    def __str__(self):
        return f"Log for {self.telephone.serial} at {self.change_time.strftime('%Y-%m-%d %H:%M')}"

    
'''
Base model for Infra items
'''
class InfraAsset(models.Model):
    STATUS_CHOICES = [
        ('Stock', 'Stock'),
        ('In Use', 'In Use'),
        ('Damage', 'Damage'),
    ]

    model = models.CharField(max_length=100)
    serial_number = models.CharField("Serial Number", max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=True, blank=True)
    mac_address = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Stock')
    purchase_date = models.DateField(blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,  
            related_name="%(class)s_created",
        )    
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)
    class Meta:
        abstract = True 
'''
Base log model for Infra items
'''

class InfraAssetLogBase(models.Model):
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)

    old_location = models.CharField(max_length=200, blank=True, null=True)
    new_location = models.CharField(max_length=200)

    old_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_old_branch')
    new_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_new_branch')

    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    change_time = models.DateTimeField(default=timezone.now)

    comment = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-change_time']

'''
Cameras model ( inheritng the base for INFRA )
'''

class Camera(InfraAsset):
    power_source = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Cameras"
        
        
''' Cameras log model  ( inheritng the base for INFRA logs ) '''
class CameraLog(InfraAssetLogBase):
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE, related_name='logs')

    class Meta:
        verbose_name = 'Camera Log'
        verbose_name_plural = 'Camera Logs'

    def __str__(self):
        return f"Log for Camera {self.camera.serial_number} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"
    
    
'''
NVR model ( inhereting the base INFRA )
'''
class NVR(InfraAsset):
    hdd_capacity = models.CharField(max_length=50)  
    number_of_ports = models.PositiveIntegerField()

    class Meta:
        verbose_name = "NVR"
        verbose_name_plural = "NVRs"   
'''
NVR log model ( inhereting the base INFRA log )
'''      
class NVRLog(InfraAssetLogBase):
    nvr = models.ForeignKey('NVR', on_delete=models.CASCADE, related_name='logs')

    class Meta:
        verbose_name = 'NVR Log'
        verbose_name_plural = 'NVR Logs'

    def __str__(self):
        return f"Log for NVR {self.nvr.serial_number} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"

''' Firewall part '''
class Firewall(InfraAsset):
    firmware_version = models.CharField(max_length=255, blank=True, null=True)
    number_of_ports = models.IntegerField(blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.model} - {self.serial_number}"

class FirewallLog(InfraAssetLogBase):
    firewall = models.ForeignKey(Firewall, on_delete=models.CASCADE, related_name='logs')

    def __str__(self):
        return f"Log for {self.firewall.serial_number} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"        
'''
Switch part 
'''
class Switch(InfraAsset):
    number_of_ports = models.PositiveIntegerField()
    number_of_poe_ports = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Switch"
        verbose_name_plural = "Switches"

'''
switch log model
'''
class SwitchLog(InfraAssetLogBase):
    switch = models.ForeignKey('Switch', on_delete=models.CASCADE, related_name='logs')

    class Meta:
        verbose_name = 'Switch Log'
        verbose_name_plural = 'Switch Logs'

    def __str__(self):
        return f"Log for Switch {self.switch.serial_number} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"


# Access Point model (inherits from InfraAsset and adds expiry_date)
class AccessPoint(InfraAsset):
    expiry_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Access Point"
        verbose_name_plural = "Access Points"


# Access Point log model (inherits from InfraAssetLogBase)
class AccessPointLog(InfraAssetLogBase):
    access_point = models.ForeignKey('AccessPoint', on_delete=models.CASCADE, related_name='logs')

    class Meta:
        verbose_name = 'Access Point Log'
        verbose_name_plural = 'Access Point Logs'

    def __str__(self):
        return f"Log for Access Point {self.access_point.serial_number} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"


# Router model (inherits from InfraAsset, no extra fields)
class Router(InfraAsset):

    class Meta:
        verbose_name = "Router"
        verbose_name_plural = "Routers"


# Router log model (inherits from InfraAssetLogBase)
class RouterLog(InfraAssetLogBase):
    router = models.ForeignKey('Router', on_delete=models.CASCADE, related_name='logs')

    class Meta:
        verbose_name = 'Router Log'
        verbose_name_plural = 'Router Logs'

    def __str__(self):
        return f"Log for Router {self.router.serial_number} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"
    
'''
UPS part
'''
class UPS(InfraAsset):
    # Override inherited field to nullify it
    mac_address = None  # This hides it from model/form logic

    # Add UPS-specific fields
    POWER_SOURCE_CHOICES = [
        ('Utility', 'Utility'),
        ('Battery', 'Battery'),
        ('Generator', 'Generator'),
    ]

    voltage = models.FloatField(blank=True, null=True)
    power_source = models.CharField(max_length=20, choices=POWER_SOURCE_CHOICES, blank=True, null=True)
    last_maintenance_date = models.DateField(blank=True, null=True)
    next_maintenance_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "UPS"
        verbose_name_plural = "UPS Devices"

class UPSLog(InfraAssetLogBase):
    POWER_SOURCE_CHOICES = [
        ('Utility', 'Utility'),
        ('Battery', 'Battery'),
        ('Generator', 'Generator'),
    ]

    # New UPS-specific fields to track changes
    old_voltage = models.FloatField(blank=True, null=True)
    new_voltage = models.FloatField(blank=True, null=True)

    old_power_source = models.CharField(max_length=20, choices=POWER_SOURCE_CHOICES, blank=True, null=True)
    new_power_source = models.CharField(max_length=20, choices=POWER_SOURCE_CHOICES, blank=True, null=True)

    old_last_maintenance_date = models.DateField(blank=True, null=True)
    new_last_maintenance_date = models.DateField(blank=True, null=True)

    old_next_maintenance_date = models.DateField(blank=True, null=True)
    new_next_maintenance_date = models.DateField(blank=True, null=True)

    ups = models.ForeignKey("UPS", on_delete=models.CASCADE, related_name="logs")

    class Meta:
        verbose_name = "UPS Log"
        verbose_name_plural = "UPS Logs"


'''
Raya Data center
'''
class RayaDataCenterVM(models.Model):
    ENV_CHOICES = [
        ("uat", "UAT"),
        ("prod", "Production"),
    ]

    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(protocol="IPv4")
    vcpu = models.PositiveIntegerField(help_text="Number of vCPUs (in cores)")
    vram_gb = models.PositiveIntegerField(help_text="vRAM in GB")
    allocated_storage_gb = models.PositiveIntegerField(default=0, help_text="Allocated Storage in GB")
    operating_system = models.CharField(max_length=100, default="Ubuntu Linux")
    environment = models.CharField(max_length=20, choices=ENV_CHOICES)
    comments = models.TextField(blank=True, null=True)
    # 🔹 Contract details
    contract_start = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Raya Data Center VM"
        verbose_name_plural = "Raya Data Center VMs"
        ordering = ["environment", "name"]

    def __str__(self):
        return f"{self.name} ({self.environment})"

    # 🔹 Helpers
    @property
    def is_active_contract(self):
        """Check if VM contract is still valid."""

        return self.contract_end is None or self.contract_end >= today

    @property
    def is_due_for_renewal(self):
        """Check if renewal date is near."""

        return self.renewal_date and self.renewal_date <= today

'''
ZK Device model (Attendance Machine, Access Control, Access Door, etc.)
'''
class ZKDevice(InfraAsset):
    DEVICE_TYPE_CHOICES = [
        ('Attendance Machine', 'Attendance Machine'),
        ('Access Control', 'Access Control'),
        ('Access Door', 'Access Door'),
    ]

    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES)
    vendor = models.CharField(max_length=100, blank=True, null=True)
    
    # Override ip_address from InfraAsset (make mandatory)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    class Meta:
        verbose_name = "ZK Device"
        verbose_name_plural = "ZK Devices"

    def __str__(self):
        return f"{self.device_type} - {self.serial_number} ({self.ip_address})"


'''
ZK Device Log model (inherits InfraAssetLogBase)
'''
class ZKDeviceLog(InfraAssetLogBase):
    device = models.ForeignKey('ZKDevice', on_delete=models.CASCADE, related_name='logs')

    class Meta:
        verbose_name = 'ZK Device Log'
        verbose_name_plural = 'ZK Device Logs'

    def __str__(self):
        return f"Log for {self.device.device_type} ({self.device.serial_number}) on {self.change_time.strftime('%Y-%m-%d %H:%M')}"
