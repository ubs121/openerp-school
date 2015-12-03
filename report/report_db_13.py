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
class country:
    def __init__(self, str):
        self.name = str
        self.sum = 1
        self.female = 0
        self.deg_c = 0
        self.deg_d = 0
        self.deg_e = 0
        self.deg_f = 0
        self.degree = None
        self.tui_gov = 0
        self.tui_self = 0
        self.tui_foreign = 0
        self.tui_other = 0
        self.tui_com = 0
    def set_sum(self):
        self.sum += 1
        return
    def get_sum(self):
        return self.sum
    def get_name(self):
        return self.name
    def set_female(self):
        self.female += 1
    def get_female(self):
        return self.female
    def get_c(self):
        return self.deg_c
    def get_d(self):
        return self.deg_d
    def get_e(self):
        return self.deg_e
    def get_f(self):
        return self.deg_f
    def set_degree(self, deg):
        self.degree = deg
        self.check_degree()
    def get_tui_gov(self):
        return self.tui_gov
    def get_tui_self(self):
        return self.tui_self
    def get_tui_foreign(self):
        return self.tui_foreign
    def get_tui_other(self):
        return self.tui_other
    def get_tui_com(self):
        return self.tui_com
    def check_tuition_type(self, type):
        foud = 0
        if "com" == type:
            self.tui_com += 1
            foud = 1
        elif "foreign" == type:
            self.tui_foreign += 1
            foud = 1
        elif "gov" == type:
            self.tui_gov += 1
            foud = 1
        elif "other" == type:
            self.tui_other += 1
            foud = 1
        elif "self" == type:
            self.tui_self += 1
            foud = 1
        if foud == 0:
            self.tui_other += 1
    def check_degree(self):
#        print"self.name : ",self.name
        if self.degree == 'PhD':
            self.deg_f += 1
        elif self.degree == 'M.A':
            self.deg_e += 1
        elif self.degree == 'B.A':
            self.deg_d += 1
        else:
            self.deg_c += 1
    def print_all(self):
        print"Name : %s     Sum : %s    Female : %s    C : %s    D : %s    E : %s    F : %s    gov : %s    self : %s    foreign : %s    other : %s    com : %s"\
                                %(self.name,self.sum,self.female,self.deg_c,self.deg_d,self.deg_e,self.deg_f,self.tui_gov\
                                  ,self.tui_self, self.tui_foreign, self.tui_other, self.tui_com)
    
class report_db_13(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_13, self).__init__(cr, uid, name, context)
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
            'foot' : self.footer,
        })
        self.study_type = None
        self.year = None
        self.all = 0
        self.sum_female = 0
        self.sum_c = 0
        self.sum_d = 0
        self.sum_e = 0
        self.sum_f = 0
        self.sum_mon = 0
        self.sum_pri = 0
        self.sum_com = 0
        self.sum_curr = 0
        self.sum_other = 0
        self.sum_tui_gov = 0
        self.sum_tui_self = 0
        self.sum_tui_foreign = 0
        self.sum_tui_other = 0
        self.sum_tui_com = 0
        
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
        all_country = []
        self.cr.execute("SELECT * FROM school_student ")
        students = self.cr.dictfetchall()
        
        year = self.year['name']
        self.cr.execute("SELECT id FROM school_year WHERE name = '%s' "%(str(year)))
        year_id = self.cr.dictfetchall()[0]
#        print"year_id : ",year_id['id']
        
        too = 0
        first = 0
        for student in students:
            self.cr.execute("SELECT * FROM school_student_year WHERE year_id = '%s' AND is_paid = 'TRUE' "\
                            %(str(year_id['id'])))
            year_stds = self.cr.dictfetchall()
            type = None
            jil = 0
            for std in year_stds:
#                print"std['std_id'] : %s    student['id'] : %s"%(std['std_id'],student['id'])
                if std['std_id'] == student['id']:
                    type = std['tuition_type']
                    jil = 1
                    break
#                print"***************"
            if jil == 1:
                too +=1
                curr_id = None
                female = "female"
                home_add = student['address_home_id']
                std_id = student['id']
                gender = student['gender']
                code = student['code'] 
                curr_id = student['curr_id']
#                print"Curr_id : ",curr_id
                if curr_id:
                    self.cr.execute("SELECT degree FROM school_curriculum WHERE id = '%s'" %(str(curr_id)))
                    obj_degree = self.cr.dictfetchall()[0]
                    deg = obj_degree['degree']
                    #print"degree : ",deg
                if(home_add != None):
                    self.cr.execute("SELECT name FROM res_country WHERE id = (SELECT country_id FROM res_partner_address WHERE id = '%s') " %(str(home_add)))
                    countrys = self.cr.dictfetchall()[0]
                    name = countrys['name']
#                    print"name : ",name
#                    print"gender : ",gender
                    found = 0
                    if first == 0:
#                        print"** if first == 0: **"
                        all_country.append(country(name))
                        count = all_country[0]
                        if gender == female:
#                            print"if gender == female:"
                            count.set_female()
                        count.set_degree(deg)
                        count.check_tuition_type(type)
                        first = 1
                    else:
#                        print"** else **"
                        for count in all_country:
                            if name == count.get_name():
#                                print"if name == count.get_name():"
                                count.set_sum()
                                found = 1
                                if gender == female:
#                                    print"*** if gender == female:"
                                    count.set_female()
                                count.set_degree(deg)
                                count.check_tuition_type(type)
                        if found == 0:
#                            print"if found == 0:"
                            count1 = country(name)
                            if gender == female:
#                                print"if gender == female:"
                                count1.set_female()
                            count1.set_degree(deg)
                            count1.check_tuition_type(type)
                            all_country.append(count1)
                            
        for i in all_country:
#            i.print_all() 
            result.append({
                            'name':i.get_name() or '',
                            'sum':i.get_sum() or '',
                            'female':i.get_female() or '',
                            'c' : i.get_c() or '',
                            'd' : i.get_d() or '',
                            'e' : i.get_e() or '',
                            'f' : i.get_f() or '',
                            'gov' : i.get_tui_gov() or '',
                            'self' : i.get_tui_self() or '',
                            'foreign' : i.get_tui_foreign() or '',
                            'other' : i.get_tui_other() or '',
                            'com' : i.get_tui_com() or '',
                           })
            self.all += i.get_sum()
            self.sum_female += i.get_female()
            self.sum_c += i.get_c()
            self.sum_d += i.get_d()
            self.sum_e += i.get_e()
            self.sum_f += i.get_f()
            self.sum_tui_gov += i.get_tui_gov()
            self.sum_tui_self += i.get_tui_self()
            self.sum_tui_foreign += i.get_tui_foreign()
            self.sum_tui_other += i.get_tui_other()
            self.sum_tui_com += i.get_tui_com()
        return result
    def footer(self):
        foot = {}
        self.zahiral = None
        self.manager = None
        self.cr.execute("SELECT * FROM hr_employee ")
        category = self.cr.dictfetchall()
        for cat in category:
            id = cat['category_id']
            if id == 6:
                self.zahiral = cat['name']
            elif id == 5:
                self.manager = cat['name']
        foot = {
                'zah' : self.zahiral or '',
                'man' : self.manager or '',
                }
        return foot
    def sum(self):
        res = {}
        res = {
                'all':self.all or '',
                'female':self.sum_female or '',
                'sum_c' : self.sum_c or '',
                'sum_d' : self.sum_d or '',
                'sum_e' : self.sum_e or '',
                'sum_f' : self.sum_f or '',
                'sum_gov' : self.sum_tui_gov or '',
                'sum_self' : self.sum_tui_self or '',
                'sum_for' : self.sum_tui_foreign or '',
                'sum_oth' : self.sum_tui_other or '',
                'sum_com' : self.sum_tui_com or '',
                }
        
        return res
report_sxw.report_sxw(
    'report.db_13',
    'school.student',
    'addons/school/report/report_db_13.rml',
    parser=report_db_13, 
    header=False)
