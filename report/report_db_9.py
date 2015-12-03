# -*- encoding: utf-8 -*-
'''
Created on Oct 28, 2009

@author: ubs121
'''

import time
from report import report_sxw
import netsvc

logger = netsvc.Logger()

class report_db_9(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_9, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time' : time,
            'hich_jil' : self.get_hich_jil,
            'lines' : self.get_lines,
            'abt_school' : self.abt_school,
            'school' : self.school,
            'title' : self.title,
            'city' : self.city,
            'district' : self.district,
        })
    def abt_school(self, form):
        self.cr.execute("SELECT * FROM res_partner WHERE id=" + str(form['school_id']))
        obj_rp = self.cr.dictfetchall()[0]
        reg_no = obj_rp['register_no'] 
        self.school = obj_rp['name']
        self.title = obj_rp['title']
        self.cr.execute("SELECT * FROM res_partner_address WHERE partner_id=" + str(obj_rp['id']))
        obj_rpa = self.cr.dictfetchall()[0]
        self.cr.execute("SELECT name FROM res_country_state WHERE id=" + str(obj_rpa['state_id']))
        obj_rcs = self.cr.dictfetchall()[0]
        self.city = obj_rcs['name']
        self.district = obj_rpa['city']
        return reg_no
    def school(self):
        return self.school
    def title(self):
        return self.title
    def city(self):
        return self.city
    def district(self):
        return self.district
    def get_hich_jil(self, form):
        self.year = self.pool.get('school.year').read(self.cr, self.uid, [form['year']])[0]
        return self.year['name']
    def get_lines(self, form):
        result = []
        cnt = 1
        self.cr.execute("SELECT name, id FROM hr_employee_category")
        emp_position = self.cr.dictfetchall()
        
        for category in emp_position:
            self.cr.execute("SELECT * FROM hr_employee \
                            WHERE category_id = " + str(category['id']))
            emps = self.cr.dictfetchall()
            print "emp_position : ", emps
            female = 0
            for emp in emps:
                if emp['gender'] == 'female':
                    female += 1
            cnt += 1
            result.append({
                           'uzuulelt':category['name'],
                           'cnt':cnt,
                           'all':len(emps),
                           'female':female
                           })
        return result

report_sxw.report_sxw(
    'report.db_9',
    'hr.employee',
    'addons/school/report/report_db_9.rml',
    parser=report_db_9,
    header=False)
