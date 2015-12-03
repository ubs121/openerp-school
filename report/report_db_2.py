# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

@author: ubs121
'''

import time
from report import report_sxw
import netsvc
import itertools
import operator

logger=netsvc.Logger()

class report_db_2(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_2, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'hich_jil' : self.get_hich_jil,
            'lines' : self.get_lines,
            'abt_school' : self.abt_school,
            'school' : self.school,
            'title' : self.title,
            'city' : self.city,
            'district' : self.district,
            'result' : self.result,
            'type' : self.type,
        })
        self.curriculums = None
        self.study_type = None
        self.year = None
        self.result = []
        
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
    def type(self, form):
        res = {}
        type = form['study_type']
        if type == "normal":
            type = "Өдөр"
        elif type == "ext":
            type = "Орой"
        elif type == "echnee":
            type = "Эчнээ"
            
        degree = form['degree']
        if degree == "k12":
            degree = "Бүрэн Дунд"
        elif degree == "wrkr":
            degree = "Ажилчин"
        elif degree == "tech":
            degree = "Техникч"
        elif degree == "dip":
            degree = "Диплом"
        elif degree == "B.A":
            degree = "Бакалавр"
        elif degree == "M.A":
            degree = "Магистр"
        elif degree == "PhD":
            degree = "Доктор"
            
        res = {'degree':degree,'type':type}
        return res
                                   
    def get_lines(self, form):
        print "kkk"
        cls = [ { 'all':'','paid':'','gov_wrk':'','gov_wrk_paid':'','gov_help':'',
                  'gov_help_paid':'','gov_loan':'','gov_loan_paid':'','sc_disc':'',
                  'self_paid':'','slf':'','other':'','other_paid':'','tuition_amount':'',
                  'sc_dorm':'','other_dorm':'','sc_dorm_f':'','other_dorm_f':''} ] * 7
        all_stds = 0
        self.cr.execute("SELECT s.id,s.cls,g.tuition_amount,s.living_address,s.gender FROM school_student AS s \
                        LEFT JOIN school_curriculum AS c ON c.id = s.curr_id \
                        LEFT JOIN school_student_group AS g ON g.id = s.grp_id \
                        LEFT JOIN res_partner_contact AS p ON p.id = s.contact_id \
                        WHERE c.degree = '"+str(form['degree'])+
                        "' AND c.study_type = '"+str(form['study_type']+"'")                        
                        )
        stds = self.cr.dictfetchall()
        
        grped_stds = []
        counter=0;
        for value in stds:
            print "value : ",value['id'],value['cls'],value['living_address'],value['gender'],value['tuition_amount']
            
        for key, items in itertools.groupby(stds, operator.itemgetter('cls')):
            grped_stds.append(list(items))
        for std in grped_stds:
            ids = []
            paid = 0
            gov_wrk = 0
            gov_wrk_paid = 0
            gov_help = 0
            gov_help_paid = 0
            gov_loan = 0
            gov_loan_paid = 0
            sc_disc = 0
            slf = 0
            self_paid = 0
            other = 0
            other_paid = 0
            sc_dorm = 0
            other_dorm = 0
            sc_dorm_f = 0
            other_dorm_f = 0
            for i in std:
               ids.append(i['id'])
               print "['living_address']: ",i['living_address']
               if i['living_address'] == "sc_dorm":
                   sc_dorm += 1
                   if i['gender'] == 'female':
                       sc_dorm_f += 1
               if i['living_address'] == 'other_dorm':
                   other_dorm += 1
                   if i['gender'] == 'female':
                       other_dorm_f += 1
            self.cr.execute("SELECT is_paid, tuition_type FROM school_student_year \
                            WHERE std_id in (" + ','.join(map(str, ids))+") \
                            AND year_id = "+str(form['year']))
            std_year = self.cr.dictfetchall()
            for i in std_year:
                if i['is_paid']:
                    paid += 1
                if i['tuition_type'] == 'gov_wrk':
                    gov_wrk += 1
                    if i['is_paid']:
                        gov_wrk_paid += 1
                elif i['tuition_type'] == 'gov_help':
                    gov_help += 1
                    if i['is_paid']:
                        gov_help_paid += 1
                elif i['tuition_type'] == 'gov_loan':
                    gov_loan += 1
                    if i['is_paid']:
                        gov_loan_paid += 1
                elif i['tuition_type'] == 'sc_disc':
                    sc_disc += 1
                elif i['tuition_type'] == 'self':
                    slf += 1
                    if i['is_paid']:
                        self_paid += 1
                else:
                    other += 1
                    if i['is_paid']:
                        other_paid += 1
                    
            cls[std[0]['cls']] = {'all':len(std),
                                  'paid':paid or '',
                                  'gov_wrk':gov_wrk or '',
                                  'gov_wrk_paid':gov_wrk_paid or '',
                                  'gov_help':gov_help,
                                  'gov_help_paid':gov_help_paid or '',
                                  'gov_loan':gov_loan or '',
                                  'gov_loan_paid':gov_loan_paid or '',
                                  'sc_disc':sc_disc or '',
                                  'self_paid':self_paid or '',
                                  'slf':slf,
                                  'other':other or '',
                                  'other_paid':other_paid or '',
                                  'tuition_amount':std[0]['tuition_amount'] or '',
                                  'sc_dorm':sc_dorm or '',
                                  'other_dorm':other_dorm or '',
                                  'sc_dorm_f':sc_dorm_f or '',
                                  'other_dorm_f':other_dorm_f or ''
                                  }
        all_paid = 0
        all_gov_wrk = 0
        all_gov_wrk_paid = 0
        all_gov_help = 0
        all_gov_help_paid = 0
        all_gov_loan = 0
        all_gov_loan_paid = 0
        all_sc_disc = 0
        all_slf = 0
        all_self_paid = 0
        all_other = 0
        all_other_paid = 0
        all_sc_dorm = 0
        all_other_dorm = 0
        all_sc_dorm_f = 0
        all_other_dorm_f = 0
        for i in cls:
            if i['paid'] != '':
                all_paid += i['paid'] 
            if i['gov_wrk'] != '':
                all_gov_wrk += i['gov_wrk'] 
            if i['gov_wrk_paid'] != '':
                all_gov_wrk_paid += i['gov_wrk_paid'] 
            if i['gov_help'] != '':
                all_gov_help += i['gov_help']
            if i['gov_help_paid'] != '':
                all_gov_help_paid += i['gov_help_paid']
            if i['gov_loan'] != '':
                all_gov_loan += i['gov_loan']
            if i['gov_loan_paid'] != '':
                all_gov_loan_paid += i['gov_loan_paid']
            if i['sc_disc'] != '':
                all_sc_disc += i['sc_disc']
            if i['slf'] != '':
                all_slf += i['slf']
            if i['self_paid'] != '':
                all_self_paid += i['self_paid']
            if i['other'] != '':
                all_other += i['other']
            if i['other_paid'] != '':
                all_other_paid += i['other_paid'] 
                
            if i['sc_dorm'] != '':
                all_sc_dorm += i['sc_dorm']
            if i['sc_dorm_f'] != '':
                all_sc_dorm_f += i['sc_dorm_f']
            if i['other_dorm'] != '':
                all_other_dorm += i['other_dorm']
            if i['other_dorm_f'] != '':
                all_other_dorm_f += i['other_dorm_f'] 
            
        self.result = {
                  'all_stds':len(stds) or '',
                  'all_paid':all_paid or '',
                  'all_gov_wrk':all_gov_wrk or '',
                  'all_gov_wrk_paid':all_gov_wrk_paid or '',
                  'all_gov_help':all_gov_help or '',
                  'all_gov_help_paid':all_gov_help_paid or '',
                  'all_gov_loan':all_gov_loan or '',
                  'all_gov_loan_paid':all_gov_loan_paid or '',
                  'all_sc_disc':all_sc_disc or '',
                  'all_slf':all_slf or '',
                  'all_self_paid':all_self_paid or '',
                  'all_other':all_other or '',
                  'all_other_paid':all_other_paid or '',
                  'beltgel':cls[0] or '',
                  '1':cls[1] or '',
                  '2':cls[2] or '',
                  '3':cls[3] or '',
                  '4':cls[4] or '',
                  '5':cls[5] or '',
                  '6':cls[6] or '',
                  'all_sc_dorm':all_sc_dorm or '',
                  'all_other_dorm':all_other_dorm or '',
                  'all_sc_dorm_f':all_sc_dorm_f or '',
                  'all_other_dorm_f':all_other_dorm_f or ''
                  }
        return ''
    def result(self,form):
        return self.result
report_sxw.report_sxw(
    'report.db_2',
    'school.student',
    'addons/school/report/report_db_2.rml',
    parser=report_db_2, 
    header=False)
