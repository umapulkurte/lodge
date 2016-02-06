cur_frm.cscript.room_no=function(doc,cdt,cdn)
{
	var r = doc.room_no;
	frappe.call({
		method:'lodge.lodge.doctype.add_room.add_room.check_roomno',
		args:{r:r},
		callback:function(r)
		{
			if(r.message==1)
			{
				cur_frm.set_value('room_no','')
			}
		}
	})
}