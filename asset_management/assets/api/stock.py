"""Create-time stock rules for inventory serializers."""

from rest_framework import serializers


def _status_enum(model):
    return getattr(model, "Status", None)


def _has_field(model, name):
    return any(field.name == name for field in model._meta.fields)


def _is_assignable(model):
    return _has_field(model, "employee")


def _resolved(attrs, instance, name, default=None):
    if name in attrs:
        return attrs[name]
    if instance is not None:
        return getattr(instance, name, default)
    return default


def _is_blank(value):
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    return False


def prepare_create(validated_data, model):
    """First insert is always Stock, with no assignee.

    If an employee was provided, it is returned so the caller can save again
    and produce a second history row (Stock → In Use).
    """
    data = dict(validated_data)
    employee = None
    status_enum = _status_enum(model)
    if status_enum is None or not hasattr(status_enum, "STOCK"):
        return data, employee
    if _is_assignable(model):
        employee = data.pop("employee", None)
    data["status"] = status_enum.STOCK
    return data, employee


def assign_after_create(instance, employee, context=None):
    if employee is None:
        return instance
    instance.employee = employee
    request = (context or {}).get("request")
    if request is not None and getattr(request, "user", None):
        instance._changed_by = request.user
    instance.save()
    return instance


class RequireOnCreateMixin:
    """Mark selected fields required when creating, even if the model allows blank."""

    require_on_create = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            return
        for name in self.require_on_create:
            field = self.fields.get(name)
            if field is None:
                continue
            field.required = True
            field.allow_null = False
            if hasattr(field, "allow_blank"):
                field.allow_blank = False


class StockOnCreateMixin:
    """New rows start as Stock. In Use needs an employee and/or a location."""

    def validate(self, attrs):
        attrs = super().validate(attrs)
        model = self.Meta.model
        status_enum = _status_enum(model)
        if status_enum is None or not hasattr(status_enum, "STOCK"):
            return attrs

        assignable = _is_assignable(model)
        in_use = getattr(status_enum, "IN_USE", None)
        errors = {}

        if self.instance is None:
            requested = attrs.get("status") or status_enum.STOCK
            allowed = [status_enum.STOCK]
            if assignable and in_use:
                allowed.append(in_use)
            if requested not in allowed:
                errors["status"] = "New records must be created as Stock."
            if requested == in_use and not attrs.get("employee"):
                errors["employee"] = "In Use requires an assigned employee."
            status = requested
        else:
            status = attrs.get("status", self.instance.status)
            if assignable and in_use and status == in_use:
                employee = _resolved(attrs, self.instance, "employee")
                if not employee:
                    errors["employee"] = "In Use requires an assigned employee."

        if in_use and status == in_use and _has_field(model, "location"):
            location = _resolved(attrs, self.instance, "location")
            if _is_blank(location):
                errors["location"] = "Location is required when status is In Use."

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        model = self.Meta.model
        validated_data, employee = prepare_create(validated_data, model)
        instance = model(**validated_data)
        if request is not None:
            if hasattr(instance, "created_by"):
                instance.created_by = request.user
            instance._changed_by = request.user
        instance.save()
        return assign_after_create(instance, employee, self.context)
