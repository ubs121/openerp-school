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

logger=netsvc.Logger()

class report_db_10(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_10, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time' : time,
            'lines' : self.get_lines,
            'abt_school' : self.abt_school,
            'school' : self.get_school,
            'city' : self.get_city,
            'district' : self.get_district,
            'hich_jil' : self.get_hich_jil,
        })
        self.school = None
        self.city = None
        self.district = None
        self.title = None
        
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
        result = []
        return result

report_sxw.report_sxw(
    'report.db_10',
    'school.student',
    'addons/school/report/report_db_10.rml',
    parser=report_db_10, 
    header=False)
