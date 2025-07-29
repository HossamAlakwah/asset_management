from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify

from users.models import CustomUser as User

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




# '''
# Telecom Access table to store information about telecom access devices
# access control devices ( ZK Access Control Devices )
# and logs will be created for each device  change.'''



# class Telecom_Access(models.Model):
#     DEVICE_STATUS_CHOICES = [
#     ('In Use', 'In Use'),
#     ('Stock', 'Stock'),
#     ('Damage', 'Damage'),
#     ('Moved', 'Moved'),
#     ]

#     DEVICE_TYPE_CHOICES = [
#         ('Telephone', 'Telephone'),
#         ('ZK', 'ZK'),
#         ('Other', 'Other'),
#     ]
    
#     product = models.CharField(max_length=255)  # e.g. "Avaya 9620"
#     serial = models.CharField(max_length=255, unique=True)
#     status = models.CharField(max_length=20, choices=DEVICE_STATUS_CHOICES)
#     employee_name = models.CharField(max_length=255, blank=True, null=True)
#     warranty = models.DateField(blank=True, null=True)
#     on_hand_date = models.DateField(blank=True, null=True)
#     return_date = models.DateField(blank=True, null=True)
#     comments = models.TextField(blank=True, null=True)
#     branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
#     type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_communication_devices')

#     class Meta:
#         verbose_name = 'Communication Device'
#         verbose_name_plural = 'Communication Devices'

#     def __str__(self):
#         return f"{self.product} - {self.serial}"


# class Telecom_AccessLog(models.Model):
#     device = models.ForeignKey(Telecom_Access, on_delete=models.CASCADE, related_name='logs')
#     changed_by = models.CharField(max_length=255)
#     old_status = models.CharField(max_length=20, blank=True, null=True)
#     new_status = models.CharField(max_length=20)
#     old_assignee = models.CharField(max_length=255, blank=True, null=True)
#     new_assignee = models.CharField(max_length=255, blank=True, null=True)
#     branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
#     change_time = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ['-change_time']
#         verbose_name = 'Communication Device Log'
#         verbose_name_plural = 'Communication Device Logs'

#     def __str__(self):
#         return f"Log for {self.device.serial} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"

# '''

# camera table to store information about camera 
# and logs will be created for each change.

# '''

# class Camera(models.Model):

#     STATUS_CHOICES = [
#         ('In Use', 'In Use'),
#         ('Damage', 'Damage'),
#         ('Stock', 'Stock'),
#     ]
#     product=models.CharField(max_length=100)
#     serial = models.CharField(max_length=100, unique=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     branch = models.ForeignKey("Branch", on_delete=models.SET_NULL, null=True, blank=True)
#     location = models.CharField(max_length=255, blank=True, null=True)
#     comment = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_cameras')

#     def __str__(self):
#         return f"{self.product} - {self.serial} - {self.branch}"

# from django.db import models


# class CameraLog(models.Model):
#     camera = models.ForeignKey("Camera", on_delete=models.CASCADE, related_name="logs")

#     old_status = models.CharField(max_length=20, blank=True, null=True)
#     new_status = models.CharField(max_length=20, blank=True, null=True)
#     branch = models.ForeignKey("Branch", on_delete=models.SET_NULL, null=True, blank=True, related_name='camera_logs_new')
#     old_location = models.CharField(max_length=255, blank=True, null=True)
#     new_location = models.CharField(max_length=255, blank=True, null=True)
#     change_time = models.DateTimeField(auto_now_add=True)
#     changed_by = models.CharField(max_length=255, blank=True, null=True)  # Username or full name

#     def __str__(self):
#         return f"Log for {self.camera.serial} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"

# ''' network equipment table and its log'''

# class NetworkEquipment(models.Model):
    
#     STATUS_CHOICES = [
#         ('In Use', 'In Use'),
#         ('Stock', 'Stock'),
#         ('Damage', 'Damage'),
#         ('Moved', 'Moved'),
#     ]
    
#     device_type = models.CharField(max_length=50)
#     serial = models.CharField(max_length=255, unique=True)
#     model = models.CharField(max_length=255) 
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     location = models.CharField(max_length=255, blank=True, null=True)
#     ip_address = models.GenericIPAddressField(blank=True, null=True)  # Optional IP management
#     comments = models.TextField(blank=True, null=True)
#     branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         User, 
#         null=True, 
#         blank=True, 
#         on_delete=models.SET_NULL, 
#         related_name='created_network_equipment'
#     )

#     class Meta:
#         verbose_name = 'Network Equipment'
#         verbose_name_plural = 'Network Equipment'
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.device_type} - {self.model} ({self.serial})"


# class NetworkEquipmentLog(models.Model):
#     equipment = models.ForeignKey(
#         NetworkEquipment, 
#         on_delete=models.CASCADE, 
#         related_name='logs'
#     )
#     changed_by = models.CharField(max_length=255)
#     old_status = models.CharField(max_length=20, blank=True, null=True)
#     new_status = models.CharField(max_length=20)
#     old_location = models.CharField(max_length=255, blank=True, null=True)
#     new_location = models.CharField(max_length=255, blank=True, null=True)
#     old_ip_address = models.GenericIPAddressField(blank=True, null=True)
#     new_ip_address = models.GenericIPAddressField(blank=True, null=True)
#     branch = models.ForeignKey("Branch", on_delete=models.SET_NULL, null=True, blank=True, related_name='network_equipment_logs_new')
#     change_time = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ['-change_time']
#         verbose_name = 'Network Equipment Log'
#         verbose_name_plural = 'Network Equipment Logs'

#     def __str__(self):
#         return f"Log for {self.equipment.serial} on {self.change_time.strftime('%Y-%m-%d %H:%M')}"
    
# """ Consumers table to store information about consumers
# and logs will be created for each consumer change."""
# class ConsumerCategory(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     minimum_stock = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return self.name


#     def current_stock(self):
#         # Sum all available stock quantities from ConsumerStock for this category
#         result = self.stocks.aggregate(total=Sum('quantity'))
#         return result['total'] or 0
#     def needs_restock(self):
#         return self.current_stock() <= self.minimum_stock

# class ConsumerStock(models.Model):
#     STATUS_CHOICES = [
#         ('available', 'available'),

#     ]
#     category = models.ForeignKey(ConsumerCategory, on_delete=models.CASCADE, related_name='stocks')
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

#     quantity = models.PositiveIntegerField(default=0)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ('category', 'branch')

#     def __str__(self):
#         return f"{self.quantity}x {self.category.name} @ {self.branch.name}"

# from assets.models import Asset  # Import your Asset model


# class ConsumerItem(models.Model):
#     STATUS_CHOICES = [
#         ('in_use', 'In Use'),
#         ('damaged', 'Damaged'),
#         ('lost', 'Lost'),
#     ]

#     category = models.ForeignKey(ConsumerCategory, on_delete=models.CASCADE, related_name='items')
#     serial = models.CharField(max_length=100, blank=True, null=True)

#     assigned_to_asset = models.ForeignKey(
#         Asset,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='consumable_items_assigned',
#         help_text='The asset (e.g., laptop) this consumable item is assigned to.'
#     )

#     assigned_to_name = models.CharField(max_length=100, blank=True, null=True)

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_use')
#     comment = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if self.assigned_to_asset:
#             # Store name directly from asset
#             self.assigned_to_name = self.assigned_to_asset.employee_name

#             # Try to match a real user
#             if not self.assigned_to_name:
#                 employee_name = self.assigned_to_asset.employee_name
#                 user = None

#                 if employee_name:
#                     try:
#                         user = User.objects.get(username=employee_name)
#                     except User.DoesNotExist:
#                         try:
#                             parts = employee_name.strip().split(' ', 1)
#                             if len(parts) == 2:
#                                 user = User.objects.filter(
#                                     first_name__iexact=parts[0],
#                                     last_name__iexact=parts[1]
#                                 ).first()
#                         except Exception:
#                             pass

#                 if user:
#                     self.assigned_to_name = user.get_full_name() or user.username


#         else:
#             self.assigned_to_name = None
#             self.assigned_to_name = None

#         super().save(*args, **kwargs)
#     def __str__(self):
#         assigned_asset = self.assigned_to_asset.serial if self.assigned_to_asset else "Unassigned"
#         assigned_user = self.assigned_to_name or "No User"
#         return f"{self.category.name} - {self.status} - Asset: {assigned_asset} - User: {assigned_user}"




