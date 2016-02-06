# Copyright (c) 2013, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AddRoom(Document):
	def validate(self):
		room=self.room_no
		q=frappe.db.sql("""select room_no from `tabAdd Room` where room_no=%s""",(room))
		if q:
			frappe.throw("Entered Room No already exists!")

@frappe.whitelist()
def check_roomno(r):
	q = frappe.db.sql("""select name from `tabAdd Room` where room_no=%s""",(r))
	if q:
		#frappe.msgprint("Entered Room no already exists")
		return 1
	else:
		return 2