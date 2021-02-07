from .models import *

def checkMinMaxThreshold(object):
	sensorobj = SensorReg.objects.get(UID=object.sensorId)
	mini = sensorobj.min_threshold
	maxi = sensorobj.max_threshold
	uid = sensorobj.UID
	location = sensorobj.location
	typeofsensor = sensorobj.typeOfSensor
	if(object.sensorValue>=mini and object.sensorValue<=maxi):
		return (uid,True,location,typeofsensor)
	else:
		return (uid,False,location,typeofsensor)