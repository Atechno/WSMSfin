from django.urls import path
from . import views

app_name = 'esp'

urlpatterns = [
	
	path('', views.home, name = 'home'),
	path('register/', views.registerUser, name= 'register'),
	path('logout/',views.logoutUser, name='logout'),
	path('dashboard/',views.dashboard, name='dashboard'),
	path('registerSensor/',views.registerSensor, name='registerSensor'),
	path('updateSensor/',views.updateSensor, name='updateSensor'),
	path('modifySensor/<str:pk>/',views.modifySensor, name='modifySensor'),
	path('deleteSensor/<str:pk>/',views.deleteSensor, name='deleteSensor'),
	path('submitData/',views.submitData,name='submitData'),
	path('showData/',views.showDataView,name='ShowData'),
	path('showUpdatedData/',views.showUpdatedData,name='showUpdatedData'),
	path('messageView/',views.messageView,name='messageView'),
]