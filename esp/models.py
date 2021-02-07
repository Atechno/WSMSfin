from django.db import models

# Create your models here.
class SensorReg(models.Model):
	TOS = (
			("Temperature Sensor","Temperature Sensor"),
			("CO2 gas Sensor","CO2 gas Sensor"),
			("Humidity Sensor","Humidity Sensor"),
			("Motion Sensor","Motion Sensor"),
			("Pressure Sensor","Pressure Sensor")
		)
	UID = models.CharField(max_length=10,unique=True)
	typeOfSensor = models.CharField(max_length=20,null=True,choices=TOS,default="Temperature Sensor")
	location = models.CharField(max_length=100,null=True)
	min_threshold = models.DecimalField(max_digits=5, decimal_places=2,null=True)
	max_threshold = models.DecimalField(max_digits=5, decimal_places=2,null=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.UID

class SensorData(models.Model):
	sensorId = models.ForeignKey(SensorReg, null=True, on_delete=models.CASCADE)
	sensorValue = models.DecimalField(max_digits=5, decimal_places=2,null=True,default=0)
