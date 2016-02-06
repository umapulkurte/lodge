# Copyright (c) 2013, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Booking(Document):
	def on_submit(self):
		#self.flag=1
		room=self.room_no
		#self.room_status='Allocated'
		sql=frappe.db.sql("""select room_no,r_status from `tabAdd Room` where room_no=%s""",(room))
		if sql:
			sql1=frappe.db.sql("""update `tabAdd Room` set r_status='Allocated' where room_no=%s""",(room))
			frappe.msgprint("Room is Allocated!")
	def validate(self):
		self.flag=1
		self.room_status='Allocated'
	def on_trash(self):
		room=self.room_no
		sql=frappe.db.sql("""select room_no,r_status from `tabAdd Room` where room_no=%s""",(room))
		if sql:
			sql1=frappe.db.sql("""update`tabAdd Room` set r_status='Free' where room_no=%s""",(room))

@frappe.whitelist()
def get_image(img):
	#from PIL import Image
	#image = Image.open("/home/wayzon2/Desktop/Nilesh/"+img)
	#path1="assets/"
	#temp = image.copy() 
  	#temp.save('%s%s' % (path1, img))
	path="assets/"+img
	str1="""
	<html>
	<body>
	<img src=%s align=right height="100" width="150">
	</body>
	</html>
	""" % path
	return (str1,path)

@frappe.whitelist()
def get_room_details(room):
	#q=frappe.db.sql("""select allocated_room from `tabBooking` where allocated_room=%s""",room)
	q=frappe.db.sql("""select room_no from `tabAdd Room` where name=%s and r_status='Allocated'""",(room))
	if q:
		return q

@frappe.whitelist()
def get_free_room():
	s=frappe.db.sql("""select room_no from `tabAdd Room` where r_status='Free'""")
	return (s)

@frappe.whitelist()
def get_details(rm_id):
	s1=frappe.db.sql("""select room_no,building_name,class_name from `tabAdd Room` where room_no=%s""",(rm_id))
	return(s1)