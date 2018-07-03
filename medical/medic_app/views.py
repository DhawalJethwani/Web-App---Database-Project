# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django.views import generic
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.context_processors import auth
from django.db import connection
from datetime import datetime
from email.mime.text import MIMEText
from django.contrib.auth.models import User


# Create your views here.
def session_live(request,cust_id,user_class):
    request.session['cust_id']=cust_id
    request.session['user_class']=user_class
    return request
def if_session_live(request):
    if request.session.has_key("cust_id"):
        return request.session['cust_id']
    else:
        return None
def session_out(request):
    if request.session.has_key("cust_id"):
        del request.session['cust_id']
        del request.session['user_class']
    return redirect('/home/noauth/')

def logged(request):
	if request.method=="POST":
		uid=request.POST.get("uid")
		passw=request.POST.get("pass")
		passw=hash(passw)
		if uid=="admin" and passw==hash("admin"):
			session_live(request,uid,'E')
			return redirect('/home/admin/')
		query="SELECT cust_id,pass,name FROM customer where cust_id='"+str(uid)+"' and  pass='"+str(passw)+"'";
		with connection.cursor() as cursor:
			cursor.execute(query)
			customer=cursor.fetchall()
			customer=customer[0]
			if len(customer)==0:
				print "Login details are wrong"
				return redirect('/home/noauth/login')
			else:
				session_live(request,uid,'E')
				return redirect('/home/customer/')
	else:
		return redirect('/home/noauth/login')

def sign(request):
	if request.method=="POST":
		uid=request.POST.get("uid")
		pass1=request.POST.get("pass1")
		pass2=request.POST.get("pass2")
		name=request.POST.get("name")
		mob_num=request.POST.get("mob_num")
		out_amt=request.POST.get("out_amt")
		add=request.POST.get("add")
		if pass1==pass2 and uid!="admin":
			query="SELECT * FROM customer where cust_id='"+str(uid)+"'";
			with connection.cursor() as cursor:
				cursor.execute(query)
				customer=cursor.fetchone()
				if customer==None:
					sql='insert into customer (cust_id,pass,name,mob_num,outstanding_amount,address) values ("%s","%s","%s","%s",%d,"%s")' %(uid,pass1.hash(),name,mob_num,int(out_amt),add)
					cursor.execute(sql)
					return redirect('/home/noauth/login')
				else:
					return render(request,'medic_app/signup.html',{})
	else:
		return redirect('/home/noauth/signup')
		

def callhome(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/')
	elif Id!='admin':
		return redirect('/home/customer/')
	else:
		return redirect('/home/admin/')

def home(request):
	Id=if_session_live(request)
	if Id==None:
		return render(request,'medic_app/noauth.html',{})
	elif Id!='admin':
		return redirect('/home/customer/')
	else:
		return redirect('/home/admin/')	

def doctor3(request):
	Id=if_session_live(request)
	if Id==None:
		query="SELECT * FROM doctor";
		with connection.cursor() as cursor:
			cursor.execute(query)
			doctors=cursor.fetchall()
			return render(request, 'medic_app/doctor3.html', {'doctors':doctors})
	elif Id!='admin':
		return redirect('/home/customer/')
	else:
		return redirect('/home/admin/')
	
def med_info(request):
	Id=if_session_live(request)
	if Id==None:
		query="SELECT * FROM medicine";
		with connection.cursor() as cursor:
			cursor.execute(query)
			medicines=cursor.fetchall()
			return render(request, 'medic_app/med_info.html', {'medicines':medicines})
	elif Id!='admin':
		return redirect('/home/customer/')
	else:
		return redirect('/home/admin/')

def login(request):
	Id=if_session_live(request)
	if Id==None:
		return render(request, 'medic_app/login.html', {})
	elif Id!='admin':
		return redirect('/home/customer/')
	else:
		return redirect('/home/admin/')

def signup(request):
	Id=if_session_live(request)
	if Id==None:
		return render(request, 'medic_app/signup.html', {})
	elif Id!='admin':
		return redirect('/home/customer/')
	else:
		return redirect('/home/admin/')

def abt_us(request):
	Id=if_session_live(request)
	if Id==None:
		return render(request, 'medic_app/abt_us.html', {})
	elif Id!='admin':
		return redirect('/home/customer/')
	else:
		return redirect('/home/admin/')




def admin(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	else:
		return render(request, 'medic_app/admin.html', {})

def sto_form(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	if request.method=="POST":
		whol_id=request.POST.get("whol_id")
		batch_id=request.POST.get("batch_id")
		dom=request.POST.get("dom")
		exp=request.POST.get("exp")
		quant=request.POST.get("quan")
		minq=request.POST.get("min")
		cost=request.POST.get("cost")
		mid=request.POST.get("med")
		with connection.cursor() as cursor:
			cursor.execute('insert into stock (wholsaler_id,batch_id,date_of_manufacture,expiry_date,quantity_non_expiry,min_quantity,cost,med_id) values (%d,%d,"%s","%s",%d,%d,%d,%d)' %(int(whol_id),int(batch_id),dom,exp,int(quant),int(minq),int(cost),int(mid)))
		return redirect('/home/admin/sto_form')
	else:
		return render(request, 'medic_app/sto_form.html',{})

def whol_form(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	if request.method=="POST":
		nof=request.POST.get("nof")
		cont=request.POST.get("cont")
		add=request.POST.get("add")
		time=request.POST.get("time")
		due=request.POST.get("due")
		with connection.cursor() as cursor:
			cursor.execute('insert into wholesaler (name_of_firm,contact_number,address,time,outstanding_amount) values ("%s","%s","%s","%s",%d)' %(nof,cont,add,time,int(due)))
		return redirect('/home/admin/whol_form')
	else:
		return render(request, 'medic_app/whol_form.html', {})

def med_form(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	if request.method=="POST":
		name=request.POST.get("name")
		salt_info=request.POST.get("salt_info")
		life=request.POST.get("life")
		price=request.POST.get("price")
		req=request.POST.get("req")
		comp_name=request.POST.get("comp_name")
		rec_dos=request.POST.get("rec_dos")
		med_id=request.POST.get("med_id")
		with connection.cursor() as cursor:
			cursor.execute('insert into medicine (name,salt_information,shelf_life,price,prescription_req,comp_name,recom_dosage,med_id) values ("%s","%s",%d,%d,%d,"%s",%d,%d)' %(name,salt_info,int(life),int(price),bool(req),comp_name,int(rec_dos),int(med_id)))
		return redirect('/home/admin/med_form')
	else:
		return render(request, 'medic_app/med_form.html',{})

def pur_form(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	if request.method=="POST":
		pur_dos=request.POST.get("pur_dos")
		pur_amt=request.POST.get("pur_amt")
		pay_mode=request.POST.get("pay_mode")
		whol=request.POST.get("whol")
		with connection.cursor() as cursor:
			cursor.execute('insert into purchase_memo (pur_dos,pur_amount,pay_mode,wholesaler) values ("%s",%d,"%s",%d)' %(pur_dos,int(pur_amt),pay_mode,int(whol)))
		return redirect('/home/admin/purchase')
	else:
		return render(request, 'medic_app/pur_form.html', {})

def sale_form(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	if request.method=="POST":
		sale_dos=request.POST.get("sale_dos")
		sale_amt=request.POST.get("sale_amt")
		cust=request.POST.get("cust")
		with connection.cursor() as cursor:
			cursor.execute('insert into sale_memo (sale_dos,sale_amount,customer) values ("%s",%d,"%s")' %(sale_dos,int(sale_amt),cust))
		request.method="GET"
		return redirect('/home/admin/sitems')
	else:
		return render(request, 'medic_app/sale_form.html', {})

def doc_form(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	if request.method=="POST":
		name=request.POST.get("name")
		spec=request.POST.get("spec")
		con=request.POST.get("con")
		with connection.cursor() as cursor:
			cursor.execute('insert into doctor (name,specialization,contact_info) values ("%s","%s","%s")' %(name,spec,con))
		return redirect('/home/admin/doc_form')
	else:
		return render(request, 'medic_app/doc_form.html', {})

def pres_form(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	if request.method=="POST":
		doc_id=request.POST.get("doc_id")
		med_id=request.POST.get("med_id")
		with connection.cursor() as cursor:
			cursor.execute('insert into prescribes (doc_id,medicine_id) values (%d,%d)' %(int(doc_id),int(med_id)))
		return redirect('/home/admin/pres_form')

	else:
		return render(request, 'medic_app/pres_form.html', {})

def sitems(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	if request.method=="POST":
		mid=request.POST.get("smid")
		quan=request.POST.get("squan")
		cost=request.POST.get("cost")
		bill=request.POST.get("bid")
		stkid=request.POST.get("stkid")
		with connection.cursor() as cursor:
			cursor.execute('insert into items_sold (s_medicine_id,s_quantity,s_cost,bill,stock_id) values (%d,%d,%d,%d,%d)' %(int(mid),int(quan),int(cost),int(bill),int(stkid)))
		query="select med_id,sum(quantity_non_expiry) as quan from stock where med_id=%s group by med_id" %(mid)
		quant=0		
		with connection.cursor() as cursor:
			cursor.execute(query)
			quant=cursor.fetchall()
		if quant[0][1]>quan:
			q=int(quan)			
			alp=0
			with connection.cursor() as cursor:
				cursor.execute('select stock_item_id,quantity_non_expiry from stock  where quantity_non_expiry>0 and med_id=%s order by stock_item_id' %(mid))
				alp=cursor.fetchall()
			alpLi=[list(j) for j in alp]
			cnt=0
			while q>0:
				toSub=min(alpLi[cnt][1],q)
				q-=toSub
				alpLi[cnt][1]-=toSub
				cnt=cnt+1				
			with connection.cursor() as cursor:
				cursor.execute('update stock set quantity_non_expiry=0 where stock_item_id<%s and med_id=%s' %(alpLi[cnt-1][0],mid))
				cursor.execute('update stock set quantity_non_expiry=%s where stock_item_id=%s' %(alpLi[cnt-1][1],alpLi[cnt-1][0]))
				
								
		return render(request, 'medic_app/sitems.html', {})
	else:
		return render(request, 'medic_app/sitems.html', {})


def stock(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	query="SELECT * FROM stock";
	with connection.cursor() as cursor:
		cursor.execute(query)
		stocks=cursor.fetchall()
	if request.method=="POST":
		id=request.POST.get("id")
		query="DELETE FROM stock where stock_item_id="+str(id)
		with connection.cursor() as cursor:
			cursor.execute(query)
		return redirect('/home/admin/stock')
	return render(request, 'medic_app/stock.html', {'stocks':stocks})

def whole(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	query="SELECT * FROM wholesaler";
	with connection.cursor() as cursor:
		cursor.execute(query)
		wholesalers=cursor.fetchall()
	if request.method=="POST":
		id=request.POST.get("id")
		query="DELETE FROM wholesaler where whol_id="+str(id)
		with connection.cursor() as cursor:
			cursor.execute(query)
		return redirect('/home/admin/wholesaler')
	return render(request, 'medic_app/wholesaler.html', {'wholesalers':wholesalers})

def med(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	query="SELECT * FROM medicine";
	with connection.cursor() as cursor:
		cursor.execute(query)
		medicines=cursor.fetchall()
	if request.method=="POST":
		id=request.POST.get("id")
		query="DELETE FROM medicine where med_id="+str(id)
		with connection.cursor() as cursor:
			cursor.execute(query)
		return redirect('/home/admin/med')
	return render(request, 'medic_app/med.html', {'medicines':medicines})

def purc(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	query="SELECT * FROM purchase_memo";
	with connection.cursor() as cursor:
		cursor.execute(query)
		purchases=cursor.fetchall()
	if request.method=="POST":
		id=request.POST.get("id")
		query="DELETE FROM purchase_memo where pur_bill_id="+str(id)
		with connection.cursor() as cursor:
			cursor.execute(query)
		return redirect('/home/admin/purchase')
	return render(request, 'medic_app/purchase.html', {'purchases':purchases})

def sale(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	query="SELECT * FROM sale_memo";
	with connection.cursor() as cursor:
		cursor.execute(query)
		sales=cursor.fetchall()
	if request.method=="POST":
		id=request.POST.get("id")
		query="DELETE FROM sale_memo where sale_bill_id="+str(id)
		with connection.cursor() as cursor:
			cursor.execute(query)
		return redirect('/home/admin/sale')
	return render(request, 'medic_app/sale.html', {'sales':sales})

def doc1(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	query="SELECT * FROM doctor";
	with connection.cursor() as cursor:
		cursor.execute(query)
		doctors=cursor.fetchall()
	if request.method=="POST":
		id=request.POST.get("id")
		query="DELETE FROM doctor where doc_id="+str(id)
		with connection.cursor() as cursor:
			cursor.execute(query)
		return redirect('/home/admin/doctor1')
	return render(request, 'medic_app/doctor1.html', {'doctors':doctors})

def cust(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer/')
	query="SELECT * FROM customer";
	with connection.cursor() as cursor:
		cursor.execute(query)
		customers=cursor.fetchall()
	if request.method=="POST":
		id=request.POST.get("id")
		query="DELETE FROM customer where cust_id='"+str(id)+"'"
		with connection.cursor() as cursor:
			cursor.execute(query)
		return redirect('/home/admin/cust')
	return render(request, 'medic_app/cust.html', {'customers': customers})

def pres(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer')
	query="SELECT * FROM prescribes";
	with connection.cursor() as cursor:
		cursor.execute(query)
		pres=cursor.fetchall()
	if request.method=="POST":
		doc_id=request.POST.get("doc_id")
		med_id=request.POST.get("med_id")
		query="DELETE FROM prescribes where doc_id="+str(doc_id)+" and medicine_id="+str(med_id)
		with connection.cursor() as cursor:
			cursor.execute(query)
		return redirect('/home/admin/pres')
	return render(request, 'medic_app/pres.html', {'pres': pres})

def short(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id!='admin':
		return redirect('/home/customer')
	query="select distinct name,min_quantity-quan from medicine as a,stock as b,(select med_id,sum(quantity_non_expiry) as quan from stock group by med_id) as c where a.med_id=c.med_id and a.med_id=b.med_id and min_quantity>quan"
	with connection.cursor() as cursor:
		cursor.execute(query)
		shortage=cursor.fetchall()
	return render(request, 'medic_app/short.html', {'shortage':shortage})




def custo(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id=='admin':
		return redirect('/home/admin')
	query="SELECT name FROM customer where cust_id='"+str(Id)+"'"
	with connection.cursor() as cursor:
		cursor.execute(query)
		name=cursor.fetchone()
	return render(request, 'medic_app/customer.html',{'name':name[0]})

def doc2(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id=='admin':
		return redirect('/home/admin')
	query="SELECT * FROM doctor";
	with connection.cursor() as cursor:
		cursor.execute(query)
		doctors=cursor.fetchall()
		query="SELECT name FROM customer where cust_id='"+str(Id)+"'"
		cursor.execute(query)
		name=cursor.fetchone()
	return render(request, 'medic_app/doctor2.html', {'doctors':doctors,'name':name[0]})

def medi_info(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id=='admin':
		return redirect('/home/admin')
	query="SELECT * FROM medicine";
	with connection.cursor() as cursor:
		cursor.execute(query)
		medicines=cursor.fetchall()
		query="SELECT name FROM customer where cust_id='"+str(Id)+"'"
		cursor.execute(query)
		name=cursor.fetchone()
	return render(request, 'medic_app/medi_info.html', {'medicines':medicines,'name':name[0]})

def person(request):
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id=='admin':
		return redirect('/home/admin')
	query="SELECT * FROM customer where cust_id='"+str(Id)+"'"
	with connection.cursor() as cursor:
		cursor.execute(query)
		cust=cursor.fetchone()
	return render(request, 'medic_app/personal.html', {'cust':cust,'name':cust[2]})

def ord(request):
	
	Id=if_session_live(request)
	if Id==None:
		return redirect('/home/noauth/login')
	elif Id=='admin':
		return redirect('/home/admin')
	query="SELECT * FROM customer where cust_id='"+str(Id)+"'"
	with connection.cursor() as cursor:
		cursor.execute(query)
		cust=cursor.fetchone()

	query="SELECT * FROM medicine"
	with connection.cursor() as cursor:	
		cursor.execute(query)
		medicines=cursor.fetchall()
	
	if request.method=="POST":
		quans=request.POST.getlist('quan')
		quans=[int(i) for i in quans]
		for i in range(len(quans)):
			if(quans[i]<0):
				quans[i]=0
		dic={}
		amount=0
		for i in range(len(medicines)):
			dic[medicines[i][0]]=quans[i]
			amount+=medicines[i][4]*quans[i]
		date=datetime.now().date()
		query='insert into sale_memo (sale_dos,sale_amount,customer) values ("%s",%d,"%s")' %(date,int(amount),Id)
		bill_id=0
		with connection.cursor() as cursor:
			cursor.execute(query)
			cursor.execute('select LAST_INSERT_ID()')
			bill_id=cursor.fetchone()
		for i in range(len(medicines)):
			if quans[i]!=0:
				with connection.cursor() as cursor:
					cursor.execute('insert into items_sold (s_medicine_id,s_quantity,s_cost,bill) values (%d,%d,%d,%d)' %(int(medicines[i][0]),int(quans[i]),int(medicines[i][4]),int(bill_id[0])))
				query="select med_id,sum(quantity_non_expiry) as quan from stock where med_id=%s group by med_id" %(int(medicines[i][0]))
				quant=0
				with connection.cursor() as cursor:
					cursor.execute(query)
					quant=cursor.fetchall()
				if quant[0][1]>quans[i]:
					q=int(quans[i])			
					alp=0
					with connection.cursor() as cursor:
						cursor.execute('select stock_item_id,quantity_non_expiry from stock where quantity_non_expiry>0 and med_id=%s order by stock_item_id' %(medicines[i][0]))
						alp=cursor.fetchall()
					alpLi=[list(j) for j in alp]
					cnt=0
					while q>0:
						toSub=min(alpLi[cnt][1],q)
						q-=toSub
						alpLi[cnt][1]-=toSub
						cnt=cnt+1				
					with connection.cursor() as cursor:
						cursor.execute('update stock set quantity_non_expiry=0 where stock_item_id<%s and med_id=%s' %(alpLi[cnt-1][0],medicines[i][0]))
						cursor.execute('update stock set quantity_non_expiry=%s where stock_item_id=%s' %(alpLi[cnt-1][1],alpLi[cnt-1][0]))
		return render(request, 'medic_app/pay.html', {'amount':amount,'name':cust[2],'bill_id':bill_id[0]})
	return render(request, 'medic_app/order.html', {'medicines':medicines,'name':cust[2]})

