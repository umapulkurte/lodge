cur_frm.cscript.mobile_no=function(doc,cdt,cdn)
{
	var num=doc.mobile_no;
	var str=String(num);
	if((str.length)!=10)
	{
		frappe.throw("Enter 10 Digit Number");
		cur_frm.set_value('mobile_no','');
	}
}
/*cur_frm.cscript.allocated_room=function(doc,cdt,cdn)
{
	var rm_no=doc.allocated_room;
	frappe.call({
		method:'lodge.lodge.doctype.booking.booking.get_room_details',
		args:{room:rm_no},
		callback:function(r)
		{
			if(r.message)
			{
				alert("This Room is not available");
				cur_frm.set_value('allocated_room','');
				cur_frm.set_value('room_no','');
				cur_frm.set_value('building_name','');
				cur_frm.set_value('class','');
				cur_frm.set_value('rent','');
			}
			else
			{
			}
		}
	});
}*/

cur_frm.cscript.onload=function(doc,cdt,cdn)
{
	/*var id=doc.id_number
	if(id!=null)
	{
		frappe.call({
		method:'lodge.lodge.doctype.booking.booking.get_image',
		args:{img:id},
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message)
			set_field_options('test',doclist[0])
			cur_frm.set_value('image_path',doclist[1])
		}
	})
		
	}*/
	frappe.call({
		method:'lodge.lodge.doctype.booking.booking.get_free_room',
		args:{},
		callback:function(r)
		{
			set_field_options('allocated_room',r.message)
		}

	})
}
cur_frm.cscript.allocated_room=function(doc,cdt,cdn)
{
	var rm_id=doc.allocated_room
	frappe.call({
		method:'lodge.lodge.doctype.booking.booking.get_details',
		args:{rm_id:rm_id},
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message)
			cur_frm.set_value("room_no",doclist[0][0])
			cur_frm.set_value('building_name',doclist[0][01])
			cur_frm.set_value('class',doclist[0][2])
		}
	})
}