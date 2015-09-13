from django.contrib.admin.models import LogEntry, DELETION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode, force_text

from rest_framework import viewsets


class LoggerViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        """
        The destroy() method of ModelViewSet is being overridden here in
        order to get access to the object being destroyed.
        The object is being captured before calling the destroy() method
        of the parent class.
        This object is necessary for logging the action being performed on
        the object.
        """
        instance = self.get_object()
        response = super(viewsets.ModelViewSet, self).destroy(
            request, *args, **kwargs
        )

        if response.status_code == 204:
            # insert into LogEntry
            message = [
                ('Deleted %(name)s "%(object)s".') % {
                    'name': force_text(instance._meta.verbose_name),
                    'object': force_text(instance)
                }
            ]
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(
                    instance).pk,
                object_id=instance.pk,
                object_repr=force_unicode(instance),
                action_flag=DELETION,
                change_message=message,
            )
        return response

    def update(self, request, *args, **kwargs):
        """
        The update() method of ModelViewSet is being overridden
        here in order to get the object on which update operation
        is being performed.
        The object is needed in order to log the action being performed
        on the object.
        """
        instance = self.get_object()
        response = super(viewsets.ModelViewSet, self).update(
            request, *args, **kwargs
        )

        if response.status_code == 200:
            # insert into LogEntry
            # TODO: Change the message in order to include
            #       the fields that has been updated.
            message = [
                ('Changed %(requestdata)s for %(name)s "%(object)s".') % {
                    'requestdata': force_text(request.data),
                    'name': force_text(instance._meta.verbose_name),
                    'object': force_text(instance)
                }
            ]
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(
                    instance).pk,
                object_id=instance.pk,
                object_repr=force_unicode(instance),
                action_flag=CHANGE,
                change_message=message,
            )
        return response
