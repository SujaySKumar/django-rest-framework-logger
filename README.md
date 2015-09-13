# django-rest-framework-logger
Add the serializer.py and viewsets.py in the root folder of your project.
Inherit LoggerSerializer and LoggerViewSet in the serializer and viewset class of your custom app respectively.
The model which you've accessed in your respective serializers and viewsets will be logged in the admin LogEntry model.

Note: Still trying to figure out a way of abstracting logging into a separate plugin.
Pull requests and suggestions are appreciated.
