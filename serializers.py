from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode, force_text

from rest_framework import serializers


class LoggerSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """
        The create function of the ModelSerializer class in Django-REST
        Framework is being overriden here in order to get access to the
        object being created.
        The object instance which is being created is necessary in order
        to log the action being performed.
        """
        user = self.context['request'].user
        instance = super(LoggerSerializer, self).create(validated_data)

        if instance.pk:
            # insert into LogEntry
            message = [
                ('Added %(name)s "%(object)s".') % {
                    'name': force_text(instance._meta.verbose_name),
                    'object': force_text(instance)
                }
            ]
            LogEntry.objects.log_action(
                user_id=user.pk,
                content_type_id=ContentType.objects.get_for_model(instance).pk,
                object_id=instance.pk,
                object_repr=force_unicode(instance),
                action_flag=ADDITION,
                change_message=message,
            )
        return instance
