from django.core.exceptions import (
    MultipleObjectsReturned,
    ObjectDoesNotExist,
)
from rest_framework import serializers

class ManyToManySaveMixin(object):
    """
    Mixin for serializers that saves ManyToMany fields by looking up related models.
    Create a new attribute called "save_related_fields" in the Meta class that
    represents the ManyToMany fields that should have save behavior.
    You can also specify a dictionary instead of a string, with the following fields:
        - field (string, required): The field to implement saving behavior on.
        - mode (bool):
            - If set to create, create the related model if it does not exist.
            - Otherwise, raise an exception if the user links to a nonexistent object.
    """

    def _lookup_item(self, model, field_name, item, mode=None):
        if mode == "create":
            obj, _ = model.objects.get_or_create(**item)
            return obj
        else:
            try:
                return model.objects.get(**item)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    {
                        field_name: [
                            "The object with these values does not exist: {}".format(
                                item
                            )
                        ]
                    },
                    code="invalid",
                )
            except MultipleObjectsReturned:
                raise serializers.ValidationError(
                    {
                        field_name: [
                            "Multiple objects exist with these values: {}".format(item)
                        ]
                    }
                )

    def save(self):
        m2m_to_save = getattr(self.Meta, "save_related_fields", [])

        # turn all entries into dict configs
        for i, m2m in enumerate(m2m_to_save):
            if not isinstance(m2m, dict):
                m2m_to_save[i] = {"field": m2m, "mode": None}

        # ignore fields that aren't specified
        ignore_fields = set()

        # remove m2m from validated data and save
        m2m_lists = {}
        for m2m in m2m_to_save:
            mode = m2m.get("mode", None)
            field_name = m2m["field"]

            field = self.fields[field_name]
            if isinstance(field, serializers.ListSerializer):
                m2m["many"] = True
                model = field.child.Meta.model
                m2m_lists[field_name] = []
                items = self.validated_data.pop(field_name, None)
                if items is None:
                    ignore_fields.add(field_name)
                    continue
                for item in items:
                    m2m_lists[field_name].append(
                        self._lookup_item(model, field_name, item, mode)
                    )
            else:
                m2m["many"] = False
                if hasattr(field, "Meta"):
                    model = field.Meta.model
                    item = self.validated_data.pop(field_name, None)
                    m2m_lists[field_name] = self._lookup_item(
                        model, field_name, item, mode
                    )
                else:
                    ignore_fields.add(field_name)

        obj = super(ManyToManySaveMixin, self).save()

        # link models to this model
        updates = []
        for m2m in m2m_to_save:
            field = m2m["field"]
            if field in ignore_fields:
                continue
            value = m2m_lists[field]
            if m2m["many"]:
                getattr(obj, field).set(value)
            else:
                setattr(obj, field, value)
                updates.append(field)

        if updates:
            obj.save(update_fields=updates)

        return obj