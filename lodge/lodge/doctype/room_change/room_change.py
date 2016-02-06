# Copyright (c) 2013, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RoomChange(Document):
	def validate(self):
		self.flag=1
		dt=self.date
		#room=self.room_no
		room=self.allocated_room
		cust=self.customer
		#al_room=self.allocated_room
		al_room=self.room_no
		b_name=self.building_name
		cls=self.r_class
		rent=self.rent
		self.room_status='Allocated'
		sql=frappe.db.sql("""select room_no,r_status from `tabAdd Room` where room_no=%s""",(room))
		if sql:
			sql1=frappe.db.sql("""update`tabAdd Room` set r_status='Allocated' where room_no=%s""",(room))
			frappe.msgprint("Room is Allocated!")
		q=frappe.db.sql("""select allocated_room,room_no,customer_name from `tabBooking` where customer_name=%s""",(cust))
		if q:
			q1=frappe.db.sql("""update `tabBooking` set flag=2 where allocated_room=%s and room_no=%s and customer_name=%s""",(q[0][0],q[0][1],q[0][2]))
			q2=frappe.db.sql("""update `tabAdd Room` set r_status='Free' where name=%s and room_no=%s""",(q[0][0],q[0][1]))
		q5 = frappe.db.sql("""select address,occupancy,mobile_no from `tabBooking` where customer_name=%s""",(cust))
		q6 = frappe.db.sql("""select name from `tabRoom Change` where date=%s and customer=%s and allocated_room=%s""",(dt,cust,room))
		if q6:
			frappe.throw("selected room is already allocated to customer on selected date")
		else:
			q3=frappe.db.sql("""select max(cast(name as int)) from `tabBooking`""")[0][0]
			if q3:
				name=int(q3)+1
			else:
				name=1
			q4=frappe.db.sql("""insert into `tabBooking` 
			set name=%s,date=%s,customer_name=%s,allocated_room=%s,room_no=%s,building_name=%s,
			class=%s,rent=%s,room_status='Allocated',flag=1,address=%s,occupancy=%s,mobile_no=%s""",(name,dt,cust,al_room,room,b_name,cls,rent,q5[0][0],q5[0][1],q5[0][2]))
	def on_trash(self):
		cust=self.customer
		q=frappe.db.sql("""select allocated_room,room_no,customer_name from `tabBooking` where name=%s""",(cust))
		if q:
			q1=frappe.db.sql("""update `tabBooking` set flag=1 where allocated_room=%s and room_no=%s and customer_name=%s and name=%s""",(q[0][0],q[0][1],q[0][2],cust))
		room=self.room_no
		sql=frappe.db.sql("""select room_no,r_status from `tabAdd Room` where room_no=%s""",(room))
		if sql:
			sql1=frappe.db.sql("""update`tabAdd Room` set r_status='Free' where room_no=%s""",(room))

@frappe.whitelist()
def get_customer_name():
	list=[]
	q=frappe.db.sql("""select b.customer_name from `tabBooking` b where b.flag=1""")
	if q:
		for i in range(0, len(q)):
			list.append(q[i])
		q1=frappe.db.sql("""select b.name from `tabBooking` b where b.flag=1""")
		if q1:
			for j in range(0, len(q1)):
				list.append(q1[j])
		return q
@frappe.whitelist()
def customer_name(n):
	q=frappe.db.sql("""select customer_name from `tabBooking` where customer_name=%s""",(n))[0][0]
	return q

@frappe.whitelist()
def get_room():
	q=frappe.db.sql("""select room_no from `tabAdd Room` where r_status='Free'""")
	return q

@frappe.whitelist()
def get_room_detail(r):
	q=frappe.db.sql("""select name,building_name,class_name from `tabAdd Room` where room_no=%s""",(r))
	return q