# -*- encoding: utf-8 -*-
'''
Created on Oct 28, 2009

@author: ubs121
'''

import time
from report import report_sxw
import pooler
import netsvc
import mx.DateTime
import datetime
import itertools
import pprint
import operator
#from papyon.msnp.challenge import amount

logger=netsvc.Logger()

class product:
    def __init__(self, id):
        self.name = ""
        self.amount = 0
        self.id = id
    def set_name(self, str):
        self.name = str
    def set_amount(self, qty):
        self.amount += qty
#        print"def set_amount name : %s     self.amount : %s    def set_amount qty : %s"%(self.name,self.amount,qty)
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_amount(self):
        return self.amount
    def print_all(self):
        print"name : %s    id = %s    amount : %s"%(self.name, self.id, self.amount)
    
class report_db_12(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_12, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time' : time,
            'lines' : self.get_lines,
            'abt_school' : self.abt_school,
            'school' : self.get_school,
            'city' : self.get_city,
            'district' : self.get_district,
            'hich_jil' : self.get_hich_jil,
            'number' : self.get_number,
        })
        self.number = 0
        self.name = None

    def abt_school(self, form):
        self.cr.execute("SELECT * FROM res_partner WHERE id="+str(form['school_id']))
        obj_rp = self.cr.dictfetchall()[0]
        reg_no = obj_rp['register_no'] 
        self.school = obj_rp['name']
        self.title = obj_rp['title']
        self.cr.execute("SELECT * FROM res_partner_address WHERE partner_id="+str(obj_rp['id']))
        obj_rpa = self.cr.dictfetchall()[0]
        self.cr.execute("SELECT name FROM res_country_state WHERE id="+str(obj_rpa['state_id']))
        obj_rcs = self.cr.dictfetchall()[0]
        self.city = obj_rcs['name']
        self.district = obj_rpa['city']
        return reg_no
    
    def get_number(self):
        self.number += 1
        return self.number
    def get_school(self):
        return self.school
    
    def get_city(self):
        return self.city
    
    def get_district(self):
        return self.district
    
    def get_hich_jil(self, form):
        self.year = self.pool.get('school.year').read(self.cr, self.uid, [form['year']])[0]
        return self.year['name']

    def get_lines(self, form):
        self.cr.execute("SELECT * FROM project_project WHERE state = 'open'")
        projects = self.cr.dictfetchall()
        result = []
        for project in projects:
            amount_sum = 0
            category_id = None
            self.name = project['name']
#            print"*****************project name : ",self.name
            date_start = str(project['date_start'])
            date_start = date_start[:4]
            date_end = str(project['date_end'])
            date_end = date_end[:4]
            partner_id = project['partner_id']
            category_id = project['category_id']
            dans = []
#            print"category_id : ",category_id
            if category_id:
                self.cr.execute("SELECT order_id FROM purchase_order_line WHERE account_analytic_id =  '%s'"%(str(category_id)))
                orders = self.cr.dictfetchall()
                for order in orders:
                    self.cr.execute("SELECT * FROM purchase_order WHERE id =  '%s'"%(str(order['order_id'])))
                    total = self.cr.dictfetchall()[0]
                    amount_total = total['amount_total']
                    amount_sum += amount_total
                    self.cr.execute("SELECT product_qty, product_id FROM purchase_order_line WHERE order_id =  '%s'"%(str(order['order_id'])))
                    products = self.cr.dictfetchall()
                    found = 0
                    for pro in products:
#                        print"product_id : %s     product_qty : %s"%(pro['product_id'],pro['product_qty'])
                        yes = 0
                        id = pro['product_id']
#                        print"pro['product_id'] : ",pro['product_id']
#                        print"pound : ",found
                        if found == 0:
                            i = product(pro['product_id'])
                            self.cr.execute("SELECT default_code FROM product_product WHERE id = '%s'"%(str(pro['product_id'])))
                            name = self.cr.dictfetchall()[0]
                            code = name['default_code']
                            i.set_name(code)
                            too = pro['product_qty']
                            too = int(too)
                            i.set_amount(too)
#                            i.print_all()
                            dans.append(i)
                            found = 1
                        else:
                            for a in  dans:
#                                print"* a.get_id %s     id : %s"%(a.get_id(), id)
                                if a.get_id() == id:
#                                    print"if a.get_id() == id:"
#                                    print"a.get_name :",a.get_name()
#                                    print"id'] : ",id
#                                    print"a.get_id() : ",a.get_id()
                                    too = pro['product_qty']
                                    too = int(too)
                                    a.set_amount(too)
                                    yes = 1
#                                    a.print_all()
                            if yes == 0:
#                                print"else " 
                                i = product(pro['product_id'])
                                self.cr.execute("SELECT default_code FROM product_product WHERE id = '%s'"%(str(pro['product_id'])))
                                name = self.cr.dictfetchall()[0]
                                code = name['default_code']
                                i.set_name(code)
                                too = pro['product_qty']
                                too = int(too)
                                i.set_amount(too)
#                                i.print_all()
                                dans.append(i)
            
            string = ""
            for i in dans:
                string += i.get_name() + "-" + str(i.get_amount()) + u"ш  "
#                print"String : ",string
            partner = None
            if partner_id:
                self.cr.execute("SELECT * FROM res_partner WHERE id = "+str(partner_id))
                partner = self.cr.dictfetchall()[0]
                partner = partner['name']
            result.append({
                            'name': self.name or '',
                            'date_start' : date_start or '',
                            'date_end' : date_end or '',
                            'partner' : partner or '',
                            'str' : string or '',
                            'amount' : amount_sum or ''
                           })
            
        return result

report_sxw.report_sxw(
    'report.db_12',
    'school.student',
    'addons/school/report/report_db_12.rml',
    parser=report_db_12, 
    header=False)
