"""Module-level aliases for shared choice sets.

Several models expose a field named ``status`` or ``environment`` with
different value sets. OpenAPI generation needs a stable, explicit name for
each set, and it resolves them by dotted module path, so the aliases have to
live at module level rather than on the model classes.
"""

from .models import UPS, Camera, ColocationVM, VirtualMachine

# Endpoints and infrastructure share the same set of status values, so they
# also share a single generated enum.
ASSET_STATUS_CHOICES = Camera.Status.choices
VIRTUAL_MACHINE_STATUS_CHOICES = VirtualMachine.Status.choices
VIRTUAL_MACHINE_ENVIRONMENT_CHOICES = VirtualMachine.Environment.choices
COLOCATION_ENVIRONMENT_CHOICES = ColocationVM.Environment.choices
POWER_SOURCE_CHOICES = UPS.PowerSource.choices
