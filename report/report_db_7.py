# -*- encoding: utf-8 -*-
'''
Created on Oct 27, 2009

@author: ubs121
'''

import time
from report import report_sxw
import netsvc

logger=netsvc.Logger()

class report_db_7(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_7, self).__init__(cr, uid, name, context)
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
        self.sum_all_graduate = 0
        self.sum_doc_all = 0
        self.sum_mas_all = 0
        self.sum_bach_all = 0
        self.sum_dip_all = 0
        self.sum_doc_f = 0
        self.sum_mas_f = 0
        self.sum_bach_f = 0
        self.sum_dip_f = 0
        self.sum_doc_graduate = 0
        self.sum_mas_graduate = 0
        self.sum_bach_graduate = 0
        self.sum_dip_graduate = 0
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
        self.cr.execute("SELECT s.id, s.name FROM res_country_state as s \
                        LEFT JOIN res_country as c ON c.id = s.country_id \
                        WHERE c.code = 'mn' or c.code = 'MN'")
        cntry_states = self.cr.dictfetchall()
        cnt = 0
        for state in cntry_states:
            cnt += 1
            doc_all = 0
            mas_all = 0
            bach_all = 0
            dip_all = 0
            doc_f = 0
            mas_f = 0
            bach_f = 0
            dip_f = 0
            doc_graduate = 0
            mas_graduate = 0
            bach_graduate = 0
            dip_graduate = 0
            new_doc_all = 0
            new_mas_all = 0
            new_bach_all = 0
            new_dip_all = 0
            
            sql = '''
                SELECT c.degree, s.gender, s.admitted_date,s.is_graduate FROM school_student AS s
                LEFT JOIN school_curriculum as c ON c.id = s.curr_id
                LEFT JOIN res_partner_contact as p ON p.id = s.contact_id
                LEFT JOIN res_partner_address as addr ON addr.id = s.address_home_id
                WHERE addr.state_id = '%s'
                AND c.study_type = '%s'
                ''' % (str(state['id']),str(self.study_type))
            self.cr.execute(sql)
            lst = self.cr.dictfetchall()
            
            for i in lst:
                print "gender =  ",i['gender']
                if i['degree'] == 'PhD':
                    doc_all += 1
                    if  i['gender'] == 'female':
                        doc_f += 1
                    if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                        new_doc_all += 1
                    if  i['is_graduate']:
                        doc_graduate += 1
                elif i['degree'] == 'B.A':
                    bach_all += 1
                    if  i['gender'] == 'female':
                        bach_f += 1
                    if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                        new_bach_all += 1
                    if  i['is_graduate']:
                        bach_graduate += 1
                elif i['degree'] == 'M.A':
                    mas_all += 1
                    if  i['gender'] == 'female':
                        mas_f += 1
                    if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                        new_mas_all += 1
                    if  i['is_graduate']:
                        mas_graduate += 1
                else:
                    dip_all += 1
                    if  i['gender'] == 'female':
                        dip_f += 1
                    if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                        new_dip_all += 1
                    if  i['is_graduate']:
                        dip_graduate += 1
                            
            female = doc_f + mas_f + bach_f + dip_f
            new_all = new_doc_all + new_mas_all + new_bach_all + new_dip_all
            all_graduate = doc_graduate + mas_graduate + bach_graduate + dip_graduate
            result.append({
                            'cnt':cnt,
                            'zahirgaa':state['name'],
                            'all':len(lst) or '',
                            'female':female or '',
                            'new_all':new_all or '',
                            'all_graduate':all_graduate or '',
                            'doc_all':doc_all or '',
                            'mas_all':mas_all or '',
                            'bach_all':bach_all or '',
                            'dip_all': dip_all or '',
                            'doc_f':doc_f or '',
                            'mas_f':mas_f or '',
                            'bach_f':bach_f or '',
                            'dip_f':dip_f or '',
                            'doc_graduate':doc_graduate or '',
                            'mas_graduate':mas_graduate or '',
                            'bach_graduate':bach_graduate or '',
                            'dip_graduate':dip_graduate or '',
                            'new_doc_all':new_doc_all or '',
                            'new_mas_all':new_mas_all or '',
                            'new_bach_all':new_bach_all or '',
                            'new_dip_all':new_dip_all or '',
                           })
            self.sum_all += len(lst)
            self.sum_female += female
            self.sum_new_all += new_all
            self.sum_all_graduate += all_graduate
            self.sum_mas_all += mas_all
            self.sum_bach_all += bach_all
            self.sum_dip_all += dip_all
            self.sum_doc_f += doc_f
            self.sum_mas_f += mas_f
            self.sum_bach_f += bach_f
            self.sum_dip_f += dip_f
            self.sum_doc_graduate += doc_graduate
            self.sum_mas_graduate += mas_graduate
            self.sum_bach_graduate += bach_graduate
            self.sum_dip_graduate += dip_graduate
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
                'all_graduate':self.sum_all_graduate or '',
                'doc_all':self.sum_doc_all or '',
                'mas_all':self.sum_mas_all or '',
                'bach_all':self.sum_bach_all or '',
                'dip_all': self.sum_dip_all or '',
                'doc_f':self.sum_doc_f or '',
                'mas_f':self.sum_mas_f or '',
                'bach_f':self.sum_bach_f or '',
                'dip_f':self.sum_dip_f or '',
                'doc_graduate':self.sum_doc_graduate or '',
                'mas_graduate':self.sum_mas_graduate or '',
                'bach_graduate':self.sum_bach_graduate or '',
                'dip_graduate':self.sum_dip_graduate or '',
                'new_doc_all':self.sum_new_doc_all or '',
                'new_mas_all':self.sum_new_mas_all or '',
                'new_bach_all':self.sum_new_bach_all or '',
                'new_dip_all':self.sum_new_dip_all or '',
                }
        
        return res

report_sxw.report_sxw(
    'report.db_7',
    'school.student',
    'addons/school/report/report_db_7.rml',
    parser=report_db_7, 
    header=False)
