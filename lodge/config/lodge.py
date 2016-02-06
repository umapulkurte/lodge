from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Booking",
					"description": _("Room Booking")
				},
				{
					"type": "doctype",
					"name": "Check Out",
					"description": _("Check Out")
				},
				{
					"type": "doctype",
					"name": "Room Change",
					"description": _("Change Room")
				},
				{
					"type": "doctype",
					"name": "Add Room",
					"description": _("Add Rooms")
				},
				{
					"type": "doctype",
					"name": "Add Room Type",
					"description": _("Add Room Type")
				},
				{
					"type": "doctype",
					"name": "Building",
					"description": _("Building")
				},
				{
					"type": "doctype",
					"name": "Class",
					"description": _("Class")
				},
				{
					"type": "doctype",
					"name": "Duplicate Bill",
					"description": _("Duplicate Bill")
				},
			]
		},
		{
		"label":_("Standard Reports"),
		"icon": "icon-star",
		"items" : [
				{
					"type":"report",
					"name" :"Available Rooms",
					"doctype": "Booking",
					"is_query_report": True,
				},
				{
					"type":"report",
					"name" :"Bookings",
					"doctype": "Booking",
					"is_query_report": True,
				},
				{
					"type":"report",
					"name" :"Check Out",
					"doctype": "Check Out",
					"is_query_report": True,
				},
		]
	}
	]