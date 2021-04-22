from django.db import models
from django_mysql.models import JSONField
from django.conf import settings

class ServiceMenu(models.Model):
	company_name = models.CharField(max_length=200, null=True)
	items = JSONField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.company_name

def default_json():
	return {"items": []}

class Clients(models.Model):
	email = models.EmailField(max_length=100)
	serviceId = models.ForeignKey(ServiceMenu, on_delete=models.CASCADE, null=True)
	service_opted = JSONField(default=default_json)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	total_payment = models.CharField(max_length=100, null=True)

	def __str__(self):
			return self.email

