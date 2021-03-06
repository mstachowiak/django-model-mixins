"""
Mixin support for django models
"""
from django.db import models
from django.db.models.signals import class_prepared
from django.dispatch import receiver
from django.db.models.fields import Field


class ModelMixin(object):
    """
    Base class for model mixins
    """

    @classmethod
    def model_mixin(cls, target):
        """
        Adds the fields of the class to the target passed in.
        """
        assert issubclass(target, models.Model)
        
        fields = {}

        for (name, attr) in cls.__dict__.items():
            if isinstance(attr, models.Field):
                fields[name] = attr

        for (key, field) in fields.items():
            field.contribute_to_class(target, key)


@receiver(class_prepared)
def mixin(sender, **kwargs):
    for base in sender.__bases__:
        if issubclass(base, ModelMixin):
            base.model_mixin(sender)
