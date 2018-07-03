from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.callhome),
	url(r'home/$',views.callhome),
	url(r'noauth/$', views.home),
	url(r'noauth/doctor3$', views.doctor3),
	url(r'noauth/med_info$',views.med_info),
	url(r'noauth/login$',views.login),
	url(r'noauth/signup$',views.signup),
	url(r'noauth/abt_us$',views.abt_us),
	url(r'noauth/error_noauth$',views.abt_us),


	url(r'logged$',views.logged),
	url(r'sign$',views.sign),

	url(r'admin/$',views.admin),
	url(r'admin/sto_form$',views.sto_form),
	url(r'admin/whol_form$',views.whol_form),
	url(r'admin/med_form$',views.med_form),
	url(r'admin/pur_form$',views.pur_form),
	url(r'admin/sale_form$',views.sale_form),
	url(r'admin/doc_form$',views.doc_form),
	url(r'admin/pres_form$',views.pres_form),
	url(r'admin/stock$',views.stock),
	url(r'admin/wholesaler$',views.whole),
	url(r'admin/med$',views.med),
	url(r'admin/purchase$',views.purc),
	url(r'admin/sale$',views.sale),
	url(r'admin/doctor1$',views.doc1),
	url(r'admin/cust$',views.cust),
	url(r'admin/pres$',views.pres),
	url(r'admin/short$',views.short),
	url(r'admin/sitems$',views.sitems),
	url(r'admin/error_admin$',views.abt_us),
	
	url(r'customer/$',views.custo),
	url(r'customer/doctor2$',views.doc2),
	url(r'customer/medi_info$',views.medi_info),
	url(r'customer/personal$',views.person),
	url(r'customer/order$',views.ord),
	url(r'customer/error_customer$',views.abt_us),
	
	url(r'logout$',views.session_out),
]
