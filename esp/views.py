from django.shortcuts import render , redirect
from django.http import HttpResponse,HttpResponseNotFound
from django.contrib.auth.hashers import make_password
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .checkThreshold import *
# Create your views here.
def home(request):
	if request.user.is_authenticated:
		return redirect('esp:dashboard')
	else :
		context = {}
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username = username, password= password)

		if user is not None:
			login(request,user)
			return redirect('esp:dashboard')
		else:
			messages.info(request, "Username or Password is incorrect")
			return render(request , 'Login.html',context)
	
	return render(request , 'Login.html',context)
	

def registerUser(request):
	if request.user.is_authenticated:
		return redirect('esp:dashboard')
	else:
		form = RegisterUserForm()
		if request.method == 'POST':
			form = RegisterUserForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, "Account was created for " + username)
				return redirect('esp:home')
		context = {'form':form}
		return render(request,'Register.html',context)

@login_required(login_url='esp:home')
def dashboard(request):
	context = {}
	users = User.objects.get(username=request.user)
	firstname = users.first_name
	context = {'firstname':firstname}
	return render(request,'Dashboard.html',context)

@login_required(login_url='esp:home')
def logoutUser(request):
	logout(request)
	return redirect('esp:home')

@login_required(login_url='esp:home')
def registerSensor(request):
	context = {}
	form = SensorRegForm()
	if request.method == 'POST':
		form = SensorRegForm(request.POST)
		if form.is_valid():
			form.save()
			uid =form.cleaned_data.get('UID')
			t,created = SensorData.objects.get_or_create(sensorId=SensorReg.objects.get(UID = uid ))
			t.save()
			messages.info(request, "New sensor registered with UID "+uid+" created.")
			return redirect('esp:dashboard')

	context = {'form':form,'addOrupdate':"Add Device", 'heading': "New Device Registration"}
	return render(request, 'DeviceRegistration.html',context)


@login_required(login_url='esp:home')
def updateSensor(request):
	sensorData = SensorReg.objects.all().order_by('UID')
	context = {'sensorData':sensorData}
	return render(request, 'DeviceModification.html',context)


@login_required(login_url='esp:home')
def modifySensor(request,pk):

	data = SensorReg.objects.get(id=pk)
	form = SensorRegForm(instance=data)
	if request.method == 'POST':
		form = SensorRegForm(request.POST, instance=data)
		if form.is_valid():
			form.save()
			uid =form.cleaned_data.get('UID')
			messages.info(request, "Sensor registered with UID "+uid+" modified")
			return redirect('esp:dashboard')
	context = {'form':form ,'addOrupdate':"Update Device", 'heading' : "Update Device" }
	return render(request, 'DeviceRegistration.html',context)


@login_required(login_url='esp:home')
def deleteSensor(request,pk):
	try:
		data = SensorReg.objects.get(id=pk)
		if request.method == 'POST':
			data.delete()
			return redirect('esp:updateSensor')

		context = {'item':data}
		return render(request, 'DeleteConfirmation.html',context)
	except:
		return redirect('esp:home')

@csrf_exempt
def submitData(request):
	context = {}
	try:
		if request.method == 'POST':
			received_json_data = json.loads(request.body.decode("utf-8"))
			print(received_json_data['UID'])
			uid = received_json_data['UID']
			t = SensorData.objects.get(sensorId=SensorReg.objects.get(UID=received_json_data['UID']))
			t.sensorValue = received_json_data['sensorValue']
			t.save(update_fields=['sensorValue'])
		
		return HttpResponse("Data Submitted")
	except:
		return HttpResponseNotFound('<h1>UID not found</h1>')

@login_required(login_url='esp:home')
def showDataView(request):
	context={}
	t = SensorData.objects.all().order_by('sensorId')
	data = SensorReg.objects.all().order_by('UID')
	context = {'sensorData':t}
	return render(request, 'ShowData.html',context)

@login_required(login_url='esp:home')
def showUpdatedData(request):
	sensors = SensorData.objects.all().order_by('sensorId')
	data = SensorReg.objects.all().order_by('UID')
	context = {}
	for sensor in sensors:
		uid,flag,loc,tos = checkMinMaxThreshold(sensor)
		context[uid] = [sensor.sensorValue,tos,loc,flag]
	return JsonResponse(context)

@login_required(login_url='esp:home')
def messageView(request):
	t = SensorData.objects.all().order_by('sensorId')
	for singleData in t:
		uid,flag,location,typeofsensor = checkMinMaxThreshold(singleData)
		if flag==True:
			pass
		else:
			messages.info(request, typeofsensor+ " ("+uid+") deployed at "+location+" has exceeded range !!!")
	return render(request, 'messages.html',{})