from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from AtoZdelivery.models import Customer,tasker,orders
from django.utils import timezone
import time

def home(request):
	return render(request,'home.html')

def cust_login(request):
	msg=''
	c={}
	c.update(csrf(request))
	return render(request,'cust_login.html',{"msg":msg})

def task_login(request):
	return render(request,'task_login.html')

def cust_auth_view(request):
	if("usernamee" in request.session ):
		del request.session['usernamee']
	if("taskernamee" in request.session ):
		del request.session['taskernamee']
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user1 = auth.authenticate(Customer.objects.filter(c_name=username,c_password=password))
	print(user1)
	if not (Customer.objects.filter(c_name=username,c_password=password)).exists():
		return HttpResponseRedirect('/invalidlogin/')
	else:
		u1 = Customer.objects.get(c_name=username,c_password=password)
		request.session['usernamee']=u1.c_name
		catagory=tasker.objects.values('t_type').distinct()
		locations=tasker.objects.values('t_location').distinct()
		return render_to_response('loggedin.html',{'name':username,'catagories':catagory,'locations':locations})
	


def task_auth_view(request):
	if("usernamee" in request.session ):
		del request.session['usernamee']
	if("taskernamee" in request.session ):
		del request.session['taskernamee']
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	temp=auth.authenticate(tasker.objects.filter(t_name=username,t_password=password))
	if not (tasker.objects.filter(t_name=username,t_password=password)).exists():
		return HttpResponseRedirect('/invalidlogin/')
	else:
		t1 = tasker.objects.get(t_name=username,t_password=password)
		request.session['taskernamee']=t1.id
		tasker1 = tasker.objects.get(id=request.session['taskernamee'])
		return render(request,'tasker_profile.html',{'tasker1':tasker1,"name":username})

		#print(t1.id)
		

def loggedin(request):
	print(request.session['usernamee'])
	if(request.session['usernamee']):
		catagory=tasker.objects.values('t_type').distinct()
		locations=tasker.objects.values('t_location').distinct()
		return render_to_response('loggedin.html',{'catagories':catagory,'locations':locations})
	else:
		return render_to_response('home.html')


def invalid(request):
	return render_to_response('invalid.html')

def signup_cust(request):
	msg="successful signup..."
	h=Customer(c_name= request.POST.get('name'),c_password=request.POST.get('password'),c_email_id=request.POST.get('emailid'),c_phone_no=request.POST.get('phoneno'),c_address="hiii")
	h.save()
	return render(request,'cust_login.html')

def signup_cust_ht(request):
	return render(request, 'signup_cust_ht.html')

def signup_tasker(request):
	msg="successful signup..."
	print(request.POST.get('photo1'))
	h=tasker(t_name=request.POST.get('name'),t_password=request.POST.get('password'),t_phone_no=request.POST.get('phoneno'),t_email=request.POST.get('emailid'),t_rupee=request.POST.get('rupee'),t_location=request.POST.get('location'),t_type=request.POST.get('type'))	
	h.save()
	return render(request,'task_login.html')

def signup_tasker_ht(request):
	catagory=tasker.objects.values('t_type').distinct()
	locations=tasker.objects.values('t_location').distinct()
	return render(request, 'signup_tasker_ht.html',{'locations':locations,'catagories':catagory})

def list_location(request):
	values=tasker.objects.filter(t_type=request.GET.get('type'),t_location= request.GET.get('location')).order_by('-t_rate')
	return render_to_response('list_tasker.html',{"values":values,"type":request.GET.get('type'),"location":request.GET.get('location')})

def view_tasker(request):
	taskerpro= tasker.objects.get(t_name= request.GET.get('taskername'))
	return render(request,'one_tasker.html',{"taskerpro": taskerpro})

def logout(request):
	if("usernamee" in request.session ):
		del request.session['usernamee']
	if("taskernamee" in request.session ):
		del request.session['taskernamee']
	return render_to_response('home.html')

def take_order(request):
	if(request.session['usernamee']!="rahul"):
		custom = Customer.objects.get(c_name= request.session['usernamee'])
		now= int(round(time.time() * 1000))
		now1=timezone.now()
		o = orders(order_id=now,c_name=request.session['usernamee'],t_id=request.POST.get('taskerinfo'),order_time=now1,t_type=request.POST.get('taskertype'),order_address=custom.c_address)
		o.save()
		return render(request,'take_order.html')
	else:
		return render(request,'cust_login.html')

def my_orders(request):
 	o = orders.objects.filter(c_name=request.session['usernamee']).order_by('-order_time')
 	return render(request,'my_orders.html',{"myorders":o})

def details(request):
	o1 = orders.objects.get(order_id = request.POST.get('orderid'))
	print(o1.order_status)
	return render(request,'order_details.html',{"myorders":o1})

def list_tasker_work(request):
	list_of = orders.objects.filter(t_id = request.session['taskernamee']).order_by('-order_time')
	return render(request,'my_list.html',{"list_of":list_of})

def profile_cust(request):
	cust = Customer.objects.get(c_name=request.session['usernamee'])
	return render(request,'profile_cust.html',{'cust':cust})

def submit_review(request):
	o = orders.objects.filter(order_id=request.POST.get('orderid'))
	taskerone  = tasker.objects.get(id=request.POST.get('taskerid'))
	p = request.POST.get('review')
	taskerone1 = tasker.objects.filter(id=request.POST.get('taskerid'))
	p1=float(taskerone.t_rate)+float(p)
	p1= p1/2
	taskerone1.update(t_rate=p1)
	o1 = orders.objects.get(order_id = request.POST.get('orderid'))
	o.update(order_review=request.POST.get('review'))
	return render(request,'order_details.html',{'myorders':o1})

def profile_tasker(request):
	#print(request.session['taskernamee'])
	tasker1 = tasker.objects.get(id=request.session['taskernamee'])
	return render(request,'tasker_profile.html',{'tasker1':tasker1})

def my_List(request):
	list = orders.objects.filter(t_id= request.session['taskernamee'])
	print(list)
	return render(request,'tasker_ownlist.html',{'list':list})

def details_for_tasker(request):
	o = orders.objects.get(order_id = request.POST.get('orderid'))
	return render(request,'details_for_tasker.html',{'o':o})

def work_over(request):
	o1 = orders.objects.filter(order_id= request.POST.get('order'))
	o1.update(order_status=1)
	o = orders.objects.get(order_id = request.POST.get('orderid'))
	return render(request,'details_for_tasker.html',{'o':o})