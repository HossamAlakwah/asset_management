"""Assignment rules for employee-owned devices."""

from django.utils import timezone


def sync_assignment(instance):
    """Keep branch, status and hand-over dates consistent with the assignee.

    Called from each device model's ``save`` so Laptop, Desktop, Screen and
    Telephone stay independent types while sharing one rule:
    - an assigned device follows the employee's branch
    - assigning a stock device marks it In Use and stamps on-hand date
    - clearing the employee (unassign) is handled by the unassign action
    """
    employee = getattr(instance, "employee", None)
    if employee is None:
        return

    if getattr(employee, "branch", None):
        instance.branch = employee.branch

    status_field = getattr(instance, "Status", None)
    if status_field is None:
        return

    if instance.status == status_field.STOCK:
        instance.status = status_field.IN_USE

    if instance.status == status_field.IN_USE and hasattr(instance, "on_hand_date"):
        if not instance.on_hand_date:
            instance.on_hand_date = timezone.now().date()
        instance.return_date = None
