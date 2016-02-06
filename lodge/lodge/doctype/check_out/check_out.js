cur_frm.cscript.date=function(doc,cdt,cdn)
{
	var d=doc.date;
	cur_frm.set_value('out_date',d)
}
cur_frm.cscript.allocated_room=function(doc,cdt,cdn)
{
	//var cust_id=doc.select_customer;
	//var customer=doc.select_customer;
	var date=doc.date;
	var room_no=doc.allocated_room;
	frappe.call({
		method:'lodge.lodge.doctype.check_out.check_out.get_bill',
		args:{d:date,r:room_no},
		callback:function(result)
		{
			var doclist=frappe.model.sync(result.message);
			cur_frm.set_value("bar_bill",doclist[0]);
			cur_frm.set_value("hotel_bill",doclist[1]);
			cur_frm.set_value("lodge_bill",doclist[2]);
			cur_frm.set_value("total",doclist[3]);
			cur_frm.set_value("days",doclist[4]);
			cur_frm.set_value("allocated_room",doclist[5]);
			cur_frm.set_value("room_no",doclist[6]);
			cur_frm.set_value("building_name",doclist[7]);
			cur_frm.set_value("class",doclist[8]);
			cur_frm.set_value("address",doclist[9]);
			cur_frm.set_value("occupancy",doclist[10]);
			cur_frm.set_value("advance_taken",doclist[11])
			cur_frm.set_value("customer_name",doclist[12]);
			cur_frm.set_value("in_date",doclist[13]);
			cur_frm.set_value("select_customer",doclist[14])
		}
	});
	
}
cur_frm.cscript.service_tax=function(doc,cdt,cdn)
{
	var t= parseInt(doc.total);
	var l=parseInt(doc.luxury_tax);
	var s= parseInt(doc.service_tax);
	var a = parseInt(doc.extra_person_amount);
	var adv = parseInt(doc.advance_taken);
	var gtotal=parseInt(t+l+s+a);
	var x= parseInt(gtotal- adv)
	cur_frm.set_value("total",x);
	frappe.call({
		method:'lodge.lodge.doctype.check_out.check_out.get_money_in_words',
		args:{n:gtotal},
		callback:function(r)
		{
			cur_frm.set_value('net_pay_in_words',r.message)
		}
	})
}
//Bill No Generation
cur_frm.cscript.onload=function(doc,cdt,cdn)
{
	var d=doc.date
	if(d==null)
	{
		frappe.call({
			method:'lodge.lodge.doctype.check_out.check_out.get_bill_no',
			args:{},
			callback:function(r)
			{
				cur_frm.set_value('bill_no',r.message)
			}
		})
	}
	frappe.call({
			method:'lodge.lodge.doctype.check_out.check_out.get_customer_name',
			args:{},
			callback:function(r)
			{
				//var i;
				//var len=((r.message).length);
				//var cust_name=[];
				//var room_no=[];
				//for( i=0; i < len ; i++)
				//{
				//	cust_name.push(r.message[i][0]);
				//	room_no.push(r.message[i][1]);
				//}
				//set_field_options('select_customer',cust_name)
				set_field_options('allocated_room',r.message)
			}
		})
}
cur_frm.cscript.payment_type=function(doc,cdt,cdn)
{
	if(doc.payment_type=='Cheque')
	{
		unhide_field('cheque_no');
	}
	else
	{
		hide_field('cheque_no');
	}
}

cur_frm.cscript.discount=function(doc,cdt,cdn)
{

	var lodge_bill=doc.lodge_bill;
	var discount = doc.discount;
	var t= doc.total
	var amt = (lodge_bill*10)/100;
	var a = (lodge_bill-amt);
	var b =(t-amt)
	cur_frm.set_value('lodge_bill_after_discount',a);
	cur_frm.set_value('total',b);
}