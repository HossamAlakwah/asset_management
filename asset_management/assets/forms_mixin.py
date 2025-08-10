from .models import FieldBehavior


class FieldBehaviorMixin:
    def apply_field_behaviors(self, model_name, user=None):
        field_configs = FieldBehavior.objects.filter(model_name=model_name)
        config_map = {conf.field_name: conf for conf in field_configs}

        for field_name, field in self.fields.items():
            config = config_map.get(field_name)
            if config:
                field.required = config.is_required
                if not (user and hasattr(user, 'is_superadmin') and user.is_superadmin()):
                    field.disabled = config.is_disabled
