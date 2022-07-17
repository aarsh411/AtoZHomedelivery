from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.timezone import now

class Customer(models.Model):
	c_name=models.CharField(max_length=20)
	c_password=models.CharField(max_length=10)
	c_phone_no=models.IntegerField()
	c_email_id=models.EmailField(max_length=50)
	c_address= models.CharField(max_length=50)
	c_photo = models.ImageField(upload_to='static/images/cust_photoes',default='static/images/bg-01.jpg')
	def __str__(self):
		return self.c_name

class tasker(models.Model):
	t_name=models.CharField(max_length=20)
	t_password=models.CharField(max_length=10)
	t_phone_no=models.IntegerField()
	t_email=models.CharField(max_length=20)
	t_type= models.CharField(max_length=15)
	t_location= models.CharField(max_length=20)
	t_rupee=models.IntegerField()
	t_address=models.CharField(max_length=50)
	t_rate= models.CharField(max_length=5,default=0.0)
	t_photo = models.ImageField(upload_to='static/images/tasker_photoes',default='static/images/bg-01.jpg')
	def __str__(self):
		return self.t_name

class orders(models.Model):
	order_id=models.CharField(max_length=20)
	c_name= models.CharField(max_length=20)
	t_id= models.CharField(max_length=20)
	order_review=models.FloatField(default=0.0)
	order_time=models.DateTimeField(default=now)
	t_type = models.CharField(max_length=20, default=" ")
	t_rupee= models.IntegerField(default=0)
	order_status = models.IntegerField(default=0)
	order_address= models.CharField(default=" ", max_length=50)
	def __str__(self):
		return self.order_id
