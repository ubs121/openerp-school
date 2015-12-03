# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

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

class report_db_3(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_3, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time' : time,
            'hich_jil' : self.get_hich_jil,
            'lines' : self.get_lines,
            'study_type' : self.get_study_type,
            'abt_school' : self.abt_school,
            'school' : self.school,
            'title' : self.title,
            'city' : self.city,
            'district' : self.district,
            'sum' : self.sum,
        })
        self.study_type = None
        self.year = None
        self.sum_all = 0
        self.sum_female = 0
        self.sum_new_all = 0
        self.sum_new_female = 0
        self.sum_doc_all = 0
        self.sum_mas_all = 0
        self.sum_bach_all = 0
        self.sum_dip_all = 0
        self.sum_doc_f = 0
        self.sum_mas_f = 0
        self.sum_bach_f = 0
        self.sum_dip_f = 0
        self.sum_new_doc_f = 0
        self.sum_new_mas_f = 0
        self.sum_new_bach_f = 0
        self.sum_new_dip_f = 0
        self.sum_new_doc_all = 0
        self.sum_new_mas_all = 0
        self.sum_new_bach_all = 0
        self.sum_new_dip_all = 0
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
    def get_study_type(self, form):
        self.study_type = form['study_type']
        if self.study_type == "normal":
            return "Өдрийн"
        elif self.study_type == "ext":
            return "Оройн"
        elif self.study_type == "echnee":
            return "Эчнээ"
        else:
            return self.study_type

    def get_lines(self, form):
        result = []
        for i in range(15,33):
            if i == 15:
                nas = '16 хүртэл'
                sub_sql = '''WHERE extract(years from AGE(p.birthdate)) <= 15'''
            elif i == 30:
                nas = '30-34 настай'
                sub_sql = '''WHERE extract(years from AGE(p.birthdate)) BETWEEN 30 AND 34'''
            elif i == 31:
                nas = '35-39 настай'
                sub_sql = '''WHERE extract(years from AGE(p.birthdate)) BETWEEN 35 AND 39'''
            elif i == 32:
                nas = '40-өөс дээш'
                sub_sql = '''WHERE extract(years from AGE(p.birthdate)) >= 40'''
            else:
                nas = str(i) + ' настай'
                sub_sql = '''WHERE extract(years from AGE(p.birthdate)) = %s''' % (str(i))
                
            doc_all = 0
            mas_all = 0
            bach_all = 0
            dip_all = 0
            doc_f = 0
            mas_f = 0
            bach_f = 0
            dip_f = 0
            new_doc_f = 0
            new_mas_f = 0
            new_bach_f = 0
            new_dip_f = 0
            new_doc_all = 0
            new_mas_all = 0
            new_bach_all = 0
            new_dip_all = 0
            
            sql = '''
                select c.degree, s.gender, s.admitted_date from school_student as s
                LEFT JOIN school_curriculum as c ON c.id = s.curr_id
                LEFT JOIN res_partner_contact as p ON p.id = s.contact_id
                %s 
                AND c.study_type = '%s'
                ''' % (sub_sql, str(self.study_type))
            self.cr.execute(sql)
            lst = self.cr.dictfetchall()
            for i in lst:
                if i['degree'] == 'PhD':
                    doc_all += 1
                    if  i['gender'] == 'female':
                        doc_f += 1
                    if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                        new_doc_all += 1
                        if  i['gender'] == 'female':
                            new_doc_f += 1
                elif i['degree'] == 'B.A':
                    bach_all += 1
                    if  i['gender'] == 'f':
                        bach_f += 1
                    if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                        new_bach_all += 1
                        if  i['gender'] == 'f':
                            new_bach_f += 1
                elif i['degree'] == 'M.A':
                    mas_all += 1
                    if  i['gender'] == 'f':
                        mas_f += 1
                    if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                        new_mas_all += 1
                        if  i['gender'] == 'female':
                            new_mas_f += 1
                else:
                    dip_all += 1
                    if  i['gender'] == 'female':
                        dip_f += 1
                    if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                        new_dip_all += 1
                        if  i['gender'] == 'female':
                            new_dip_f += 1
                            
            female = doc_f + mas_f + bach_f + dip_f
            new_all = new_doc_all + new_mas_all + new_bach_all + new_dip_all
            new_female = new_doc_f + new_mas_f + new_bach_f + new_dip_f
            result.append({
                            'nas':nas,
                            'all':len(lst) or '',
                            'female':female or '',
                            'new_all':new_all or '',
                            'new_female':new_female or '',
                            'doc_all':doc_all or '',
                            'mas_all':mas_all or '',
                            'bach_all':bach_all or '',
                            'dip_all': dip_all or '',
                            'doc_f':doc_f or '',
                            'mas_f':mas_f or '',
                            'bach_f':bach_f or '',
                            'dip_f':dip_f or '',
                            'new_doc_f':new_doc_f or '',
                            'new_mas_f':new_mas_f or '',
                            'new_bach_f':new_bach_f or '',
                            'new_dip_f':new_dip_f or '',
                            'new_doc_all':new_doc_all or '',
                            'new_mas_all':new_mas_all or '',
                            'new_bach_all':new_bach_all or '',
                            'new_dip_all':new_dip_all or '',
                           })
            self.sum_all += len(lst)
            self.sum_female += female
            self.sum_new_all += new_all
            self.sum_new_female += new_female
            self.sum_mas_all += mas_all
            self.sum_bach_all += bach_all
            self.sum_dip_all += dip_all
            self.sum_doc_f += doc_f
            self.sum_mas_f += mas_f
            self.sum_bach_f += bach_f
            self.sum_dip_f += dip_f
            self.sum_new_doc_f += new_doc_f
            self.sum_new_mas_f += new_mas_f
            self.sum_new_bach_f += new_bach_f
            self.sum_new_dip_f += new_dip_f
            self.sum_new_doc_all += new_doc_all
            self.sum_new_mas_all += new_mas_all
            self.sum_new_bach_all += new_bach_all
            self.sum_new_dip_all += new_dip_all
        return result
    
    def sum(self):
        res = {}
        res = {
                'all':self.sum_all or '',
                'female':self.sum_female or '',
                'new_all':self.sum_new_all or '',
                'new_female':self.sum_new_female or '',
                'doc_all':self.sum_doc_all or '',
                'mas_all':self.sum_mas_all or '',
                'bach_all':self.sum_bach_all or '',
                'dip_all': self.sum_dip_all or '',
                'doc_f':self.sum_doc_f or '',
                'mas_f':self.sum_mas_f or '',
                'bach_f':self.sum_bach_f or '',
                'dip_f':self.sum_dip_f or '',
                'new_doc_f':self.sum_new_doc_f or '',
                'new_mas_f':self.sum_new_mas_f or '',
                'new_bach_f':self.sum_new_bach_f or '',
                'new_dip_f':self.sum_new_dip_f or '',
                'new_doc_all':self.sum_new_doc_all or '',
                'new_mas_all':self.sum_new_mas_all or '',
                'new_bach_all':self.sum_new_bach_all or '',
                'new_dip_all':self.sum_new_dip_all or '',
                }
        
        return res
report_sxw.report_sxw(
    'report.db_3',
    'school.student',
    'addons/school/report/report_db_3.rml',
    parser=report_db_3, 
    header=False)
