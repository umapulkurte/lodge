# Copyright (c) 2013, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.auth import _update_password

#from frappe.utils.email_lib import sendmail
#from frappe.utils.email_lib.email_body import get_email
#from frappe.utils.email_lib.smtp import send
from frappe.utils.user import get_user_fullname
#from frappe.utils import get_url
#import frappe.permissions

from frappe.model.document import Document


class CheckOut(Document):
	def on_submit(self):
		alc_room = self.allocated_room
		customer = self.select_customer
		bk_id = self.customer_name
		q = frappe.db.sql("""update `tabBooking` set room_status='Free' where name=%s""",(bk_id))  
	def validate(self):
		user = frappe.session.user
		self.receptionist=get_user_fullname(user)
		self.guest=self.select_customer
		#room_id=self.allocated_room
		room=self.room_no
		q0=frappe.db.sql("""select name from `tabAdd Room` where room_no=%s""",(room))
		room_id=q0[0]
		bk_id=self.customer_name
		c=self.select_customer
		self.room_status='Free'
		sql=frappe.db.sql("""select room_no,r_status from `tabAdd Room` where room_no=%s and name=%s""",(room,room_id))
		if sql:
			sql1=frappe.db.sql("""update `tabAdd Room` set r_status='Free' where room_no=%s and name=%s""",(room,room_id))
		q1=frappe.db.sql("""update `tabBooking` set flag=2 where name=%s and customer_name=%s and allocated_room=%s and room_no=%s""",(bk_id,c,room_id,room))
@frappe.whitelist()
def get_bill(d,r):
	#a = datetime.strptime(d, "%Y-%m-%d") #checkout date
	date_format = "%Y-%m-%d %H:%M:%S"
	a = datetime.strptime(d, date_format) #checkout date
	q8=frappe.db.sql("""select name,customer_name,date,rent,allocated_room,room_no,building_name,class,address,occupancy,advance_amount from `tabBooking` where room_no=%s and flag=1 and room_status='Allocated'""",(r))
	if q8:
		c=q8[0][1]
		c_id=q8[0][0]
		rmch_date=str(q8[0][2])
		bk_date=q8[0][2]
		rent1=int(q8[0][3])
		al_rm=q8[0][5]
		rm_no=q8[0][5]
		bldg_no=q8[0][6]
		cls=q8[0][7]
		adrs=q8[0][8]
		ocpancy=q8[0][9]
		advance = q8[0][10]
		#z = datetime.strptime(rmch_date, "%Y-%m-%d")
		date_format = "%Y-%m-%d %H:%M:%S"
		z = datetime.strptime(rmch_date, date_format)
		#if (a==z): #Same date of booking and checkout
		#	day1=1
		#else:
		#day1=(a-z).days
		min1 = ((a-z).total_seconds())/60
		hr1 =min1/60
		if hr1>24:
			day1 = int(hr1/24)
			d2 = (hr1 % 24)
			if (d2 > 0):
				day1=day1+1
		else:
			day1 = 1
		amt1=(day1*rent1)
		q10=frappe.db.sql("""select customer_name from `tabBooking` where customer_name=%s and flag=2""",(q8[0][1]))
		if(len(q10)>1): #fOR REPEATABLE NAMES OF CUSTOMER
			q9=frappe.db.sql("""select name,customer_name,date,rent from `tabBooking` where room_no=%s and customer_name=%s and flag=2""",(r,c))
			if q9:
				c=q9[0][1]
				c_id=q8[0][0]
				pbk_date=str(q9[0][2])
				bk_date=q9[0][2]
				pbk_rent=int(q9[0][3])
				#y = datetime.strptime(pbk_date, "%Y-%m-%d")
				date_format = "%Y-%m-%d %H:%M:%S"
				y = datetime.strptime(pbk_date, date_format)
				#if (z==y):
				#	day2=1
				#else:
				#	day2=(z-y).days
				min1 = ((z-y).total_seconds())/60
				hr1 =min1/60
				if hr1>24:
					day2 = int(hr1/24)
					d2 = (hr1 % 24)
					if (d2 > 0):
						day2=day2+1
				else:
					day2 = 1
				amt2=(day2*pbk_rent)
			else:
				day2=0
				amt2=0
			#frappe.msgprint(amt2)
		else:
			q9=frappe.db.sql("""select name,customer_name,date,rent from `tabBooking` where customer_name=%s and flag=2""",(c))
			if q9:
				c=q9[0][1]
				c_id=q8[0][0]
				pbk_date=str(q9[0][2])
				bk_date=q9[0][2]
				pbk_rent=int(q9[0][3])
				#y = datetime.strptime(pbk_date, "%Y-%m-%d")
				date_format = "%Y-%m-%d %H:%M:%S"
				y = datetime.strptime(pbk_date, date_format)
				#if (z==y):
				#	day2=1
				#else:
				#	day2=(z-y).days
				min1 = ((z-y).total_seconds())/60
				hr1 =min1/60
				if hr1>24:
					day2 = int(hr1/24)
					d2 = (hr1 % 24)
					if (d2 > 0):
						day2=day2+1
				else:
					day2 = 1
				amt2=(day2*pbk_rent)
			else:
				day2=0
				amt2=0
			#frappe.msgprint(amt2)
		days=(day1+day2)
		amt=(amt1+amt2)
		#--------------------------------------------------------------------------------------
		#-----------Bar Bill-------------------------------------------------------------------
		q=frappe.db.sql("""select name,room_no from `tabBooking` where customer_name=%s and date=%s and flag=2""",(c,bk_date))
		if q:
			q1=frappe.db.sql("""select total_amount from `tabLodge Item` where customer_name=%s and select_room=%s order by order_id desc limit 1""",(c,q[0][1]))
			if q1:
				b1=int(q1[0][0])
			else:
				b1=0
		else:
			b1=0
		t=frappe.db.sql("""select total_amount from `tabLodge Item` where customer_name=%s and select_room=%s order by order_id desc limit 1""",(c,r))
		if t:
			b2=int(t[0][0])
		else:
			b2=0
		bar=int(b1)+int(b2)
		#--------------------------------------------------------------------------------------
		#-----------Hotel Bill-------------------------------------------------------------------
		#q0=frappe.db.sql("""select room_no from `tabBooking` where customer_name=%s and date=%s and flag=2""",(c,bk_date))
		#if q0:
		#	q2=frappe.db.sql("""select total_amount from `tabHotelorder` where customer_name=%s and select_room=%s order by order_id desc limit 1""",(c,q0[0][0]))
		#	if q2:
		#		h1=int(q2[0][0])
		#	else:
		#		h1=0
		#else:
		#	h1=0
		#u=frappe.db.sql("""select total_amount from `tabHotelorder` where customer_name=%s and select_room=%s order by order_id desc limit 1""",(c,r))
		#if u:
		#	h2=int(u[0][0])
		#else:
		#	h2=0
		#hotel=int(h1)+int(h2)
		#hotel=int(h1)+int(h2)
		#------------------------------------------------------------------------------------------
		#----------Total Bill----------------------------------------------------------------------
		#add= bar+hotel+int(amt)
		add= int(bar)+int(amt)
		#result=[bar,hotel,amt,add,days,al_rm,rm_no,bldg_no,cls,adrs,ocpancy,c_id,bk_date,c]
		result=[bar,0,amt,add,days,al_rm,rm_no,bldg_no,cls,adrs,ocpancy,advance,c_id,bk_date,c]
		#frappe.msgprint(result)
		return result
@frappe.whitelist()
def get_bill_no():
	q=frappe.db.sql("""select max(bill_no) from `tabCheck Out`""")[0][0]
	if q:
		b=int(q)+1
	else:
		b=1
	return (b)

@frappe.whitelist()
def get_customer_name():
	list=[]
	q=frappe.db.sql("""select b.room_no from `tabBooking` b where b.flag=1 and b.room_status='Allocated'""")
	if q:
		#for i in range(0, len(q)):
		#	list.append(q[i])
		#q0=frappe.db.sql("""select r.allocated_room from `tabRoom Change` r where r.flag=1""")
		#if q0:
		#	for j in range (0,len(q0)):
		#		list.append(q0[j])
		return q
	else:
		q1=frappe.db.sql("""select b.room_no from `tabBooking` b where b.flag=1 and b.room_status='Allocated'""")
		return (q1)

@frappe.whitelist()
def get_money_in_words(n):
	from frappe.utils import money_in_words
	from frappe.utils import in_words
	x=money_in_words(n)
	return (x)