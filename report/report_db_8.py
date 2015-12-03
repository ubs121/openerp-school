# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

@author: ubs121
'''

from datetime import datetime
import time
from report import report_sxw
import netsvc
from string import atoi

logger = netsvc.Logger()

class report_db_8(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_8, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'hich_jil' : self.get_hich_jil,
            'lines' : self.get_lines,
            'abt_school' : self.abt_school,
            'school' : self.school,
            'title' : self.title,
            'city' : self.city,
            'district' : self.district,
            'type' : self.type,
        })
        self.this_year_int=0
        self.curriculums = None
        self.study_type = None
        self.year = None
        self.result = []
        self.sum_last_year=0
        self.sum_last_year_f=0
        self.sum_end=0
        self.sum_end_f=0
        self.sum_travel=0
        self.sum_travel_f=0
        self.sum_outer=0
        self.sum_outer_f=0
        self.sum_baldly=0
        self.sum_baldly_f=0
        self.sum_bad=0
        self.sum_bad_f=0
        self.sum_discipline=0
        self.sum_discipline_f=0
        self.sum_l_other = 0
        self.sum_l_other_f = 0
        self.sum_l_all=0
        self.sum_l_all_f=0
        self.sum_other_school=0
        self.sum_other_school_f=0
        self.sum_foreign_std=0
        self.sum_foreign_std_f=0
        self.sum_new_std = 0
        self.sum_new_std_f = 0
        self.sum_a_other = 0
        self.sum_a_other_f = 0
        self.sum_a_all = 0
        self.sum_a_all_f = 0
        self.sum_now = 0
        self.sum_now_f = 0
        
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
            
        res = {'degree':degree, 'type':type}
        return res
    def get_cls(self, reason, gender,a_reason,year,dic):
            last_year = dic[0]['last_year']
            last_year_f = dic[0]['last_year_f']
            end = dic[0]['end']
            end_f = dic[0]['end_f']
            travel = dic[0]['travel']
            travel_f = dic[0]['travel_f']
            outer = dic[0]['outer']
            outer_f = dic[0]['outer_f']
            baldly = dic[0]['baldly']
            baldly_f = dic[0]['baldly_f']
            bad = dic[0]['bad']
            bad_f = dic[0]['bad_f']
            discipline = dic[0]['discipline']
            discipline_f = dic[0]['discipline_f']
            l_other= dic[0]['l_other']
            l_other_f= dic[0]['l_other_f']

            other_school = dic[0]['other_school']
            other_school_f = dic[0]['other_school_f']
            foreign_std = dic[0]['foreign_std']
            foreign_std_f = dic[0]['foreign_std_f']
            new_std = dic[0]['new_std']
            new_std_f = dic[0]['new_std_f']
            a_other = dic[0]['a_other']
            a_other_f = dic[0]['a_other_f']
            cur_date = dic[0]['now']
            cur_date_f = dic[0]['now_f']
            
            if year == self.this_year_int-1:
                last_year+=1
                if gender == 'female':
                    last_year_f+=1
            if year == self.this_year_int:
                cur_date+=1
                if gender == 'female':
                    cur_date_f+=1
            if reason == 'end':
                end += 1
                if gender == 'female':
                     end_f += 1
            elif reason == 'travel':
                travel += 1
                if gender == 'female':
                     travel_f += 1
            elif reason == 'outer':
                outer += 1
                if gender == 'female':
                     outer_f += 1
            elif reason == 'baldly':
                baldly += 1
                if gender == 'female':
                     baldly_f += 1
            elif reason == 'bad':
                bad += 1
                if gender == 'female':
                     bad_f += 1
            elif reason == 'discipline':
                discipline += 1
                if gender == 'female':
                    discipline_f += 1
            elif reason == 'l_other':
                l_other += 1
                if gender == 'female':
                    l_other_f += 1
            l_sum = end + travel + outer + baldly + discipline + l_other
            l_sum_f = end_f + travel_f + outer_f + baldly_f + discipline_f + l_other_f 
                    
            if a_reason == 'other_school':
                other_school += 1
                if gender == 'female':
                    other_school_f += 1
            elif a_reason == 'foreign_std':
                foreign_std += 1
                if gender == 'female':
                    foreign_std_f += 1
            elif a_reason == 'new_std':
                new_std += 1
                if gender == 'female':
                    new_std_f += 1   
            elif a_reason == 'a_other':
                a_other += 1
                if gender == 'female':
                    a_other_f += 1   

            a_sum = other_school + foreign_std + new_std + a_other
            a_sum_f = other_school_f + foreign_std_f + new_std_f + a_other_f      
           
            dic = [{'last_year':last_year,
                    'last_year_f':last_year_f,
                    'end':end,
                    'end_f':end_f,
                    'travel':travel,
                    'travel_f':travel_f,
                    'outer':outer,
                    'outer_f':outer_f,
                    'baldly':baldly,
                    'baldly_f':baldly_f,
                    'bad':bad,
                    'bad_f':bad_f,
                    'discipline':discipline,
                    'discipline_f':discipline_f,
                    'l_other':l_other,
                    'l_other_f':l_other_f,
                    'l_sum':l_sum,
                    'l_sum_f':l_sum_f,
                    'other_school':other_school,
                    'other_school_f':other_school_f,
                    'foreign_std':foreign_std,
                    'foreign_std_f':foreign_std_f,
                    'new_std':new_std,
                    'new_std_f':new_std_f,
                    'a_other':a_other,
                    'a_other_f':a_other_f,
                    'a_sum':a_sum,
                    'a_sum_f':a_sum_f,
                    'now': cur_date,
                    'now_f': cur_date_f,
                    }]
            
            return dic
             
    def get_lines(self, form):
        
        self.cr.execute("SELECT status,gender,cls,admitted_date,pre_enroll FROM school_student ")
        stds_r = self.cr.dictfetchall()

        sinfo = []
        dic = [{'last_year':0,
                'last_year_f':0,
                'end':0,
                'end_f':0,
                'travel':0,
                'travel_f':0,
                'outer':0,
                'outer_f':0,
                'baldly':0,
                'baldly_f':0,
                'bad':0,
                'bad_f':0,
                'discipline':0,
                'discipline_f':0,
                'l_other':0,
                'l_other_f':0,
                'l_sum':0,
                'l_sum_f':0,
                'other_school':0,
                'other_school_f':0,
                'foreign_std':0,
                'foreign_std_f':0,
                'new_std':0,
                'new_std_f':0,
                'a_other':0,
                'a_other_f':0,
                'a_sum':0,
                'a_sum_f':0,
                'now':0,
                'now_f':0
                }]
        
        cls1=dic
        cls2=dic
        cls3=dic
        cls4=dic
        cls5=dic
        cls6=dic
        
        
        current_date = datetime.now()
        this_year_str = current_date.strftime('%Y')
        self.this_year_int = atoi(this_year_str)
        
        for sr in stds_r:
            print sr['admitted_date']
            d = datetime.strptime(sr['admitted_date'], '%Y-%m-%d')
            year_str = d.strftime('%Y')
            year_int = atoi(year_str)
            if sr['cls'] == 1:
                cls1 = self.get_cls(sr['status'], sr['gender'],sr['pre_enroll'],year_int, cls1) 
            elif sr['cls'] == 2:
                cls2 = self.get_cls(sr['status'], sr['gender'],sr['pre_enroll'],year_int,cls2)
            elif sr['cls'] == 3:
                cls3 = self.get_cls(sr['status'], sr['gender'],sr['pre_enroll'],year_int, cls3)
            elif sr['cls'] == 4:
                cls4 = self.get_cls(sr['status'], sr['gender'],sr['pre_enroll'],year_int, cls4)
            elif sr['cls'] == 5:
                cls5 = self.get_cls(sr['status'], sr['gender'],sr['pre_enroll'],year_int, cls5) 
            elif sr['cls'] == 6:
                cls6 = self.get_cls(sr['status'], sr['gender'],sr['pre_enroll'],year_int, cls6)

    
        i=0
        clss = [cls1[0],cls2[0],cls3[0],cls4[0],cls5[0],cls6[0]]
        for cls in clss:
            self.sum_last_year+=cls['last_year']
            self.sum_last_year_f+=cls['last_year_f']
            self.sum_end+=cls['end']
            self.sum_end_f+=cls['end_f']
            self.sum_travel+=cls['travel']
            self.sum_travel_f+=cls['travel_f']
            self.sum_outer+=cls['outer']
            self.sum_outer_f+=cls['outer_f']
            self.sum_baldly+=cls['baldly']
            self.sum_baldly_f+=cls['baldly_f']
            self.sum_bad+=cls['bad']
            self.sum_bad_f+=cls['bad_f']
            self.sum_discipline+=cls['discipline']
            self.sum_discipline_f+=cls['discipline_f']
            self.sum_l_other+=cls['l_other']
            self.sum_l_other_f+=cls['l_other_f']
            self.sum_l_all+=cls['l_sum']
            self.sum_l_all_f+=cls['l_sum_f']
            self.sum_other_school+=cls['other_school']
            self.sum_other_school_f+=cls['other_school_f']
            self.sum_foreign_std+=cls['foreign_std']
            self.sum_foreign_std_f+=cls['foreign_std_f']
            self.sum_a_other+=cls['a_other']
            self.sum_a_other_f+=cls['a_other_f']
            self.sum_new_std+=cls['new_std']
            self.sum_new_std_f+=cls['new_std_f']
            self.sum_a_all+=cls['a_sum']
            self.sum_a_all_f+=cls['a_sum_f']
            self.sum_now+=cls['now']
            self.sum_now_f+=cls['now_f']
            
        result = []
        for i in range(0, 5):
            if i == 0:
                uunees = ''
                sub_lines = [{'name':'Өнгөрсөн хичээлийн жилийн эхний суралцагчдын тоо','cls1':0,'cls2':cls1[0]['last_year'],'cls3':cls2[0]['last_year'],'cls4':cls3[0]['last_year'],'cls5':cls4[0]['last_year'],'cls6':cls5[0]['last_year'],'cls7':cls6[0]['last_year'],'sum':self.sum_last_year},
                             {'name':'Үүнээс: эмэгтэй','cls1':0,'cls2':cls1[0]['last_year_f'],'cls3':cls2[0]['last_year_f'],'cls4':cls3[0]['last_year_f'],'cls5':cls4[0]['last_year_f'],'cls6':cls5[0]['last_year_f'],'cls7':cls6[0]['last_year_f'],'sum':self.sum_last_year_f},
                             {'name':'Шилжсэн, цөөрсөн бүгд','cls1':cls1[0]['l_sum'],'cls2':cls2[0]['l_sum'],'cls3':cls3[0]['l_sum'],'cls4':cls4[0]['l_sum'],'cls5':cls5[0]['l_sum'],'cls6':cls6[0]['l_sum'],'cls7':0, 'sum': self.sum_l_all },
                             {'name':'Үүнээс: эмэгтэй',     'cls1':cls1[0]['l_sum_f'],'cls2':cls2[0]['l_sum_f'],'cls3':cls3[0]['l_sum_f'],     'cls4':cls4[0]['l_sum_f'],'cls5':cls5[0]['l_sum_f'],'cls6':cls6[0]['l_sum_f'],'cls7':0, 'sum': self.sum_l_all_f}]
            elif i == 1:
                uunees = u'Үүнээс'
                
                sub_lines = [{'name':'Сургууль төгссөн',      'cls1':cls1[0]['end'],     'cls2':cls2[0]['end'],     'cls3':cls3[0]['end'],      'cls4':cls4[0]['end'],     'cls5':cls5[0]['end'],     'cls6':cls6[0]['end'],  'cls7':0,'sum':self.sum_end},
                             {'name':'Үүнээс: эмэгтэй',       'cls1':cls1[0]['end_f'],   'cls2':cls2[0]['end_f'],   'cls3':cls3[0]['end_f'],    'cls4':cls4[0]['end_f'],   'cls5':cls5[0]['end_f'],   'cls6':cls6[0]['end_f'],'cls7':0, 'sum':self.sum_end_f},
                             {'name':'Өөр сургуульд шилжсэн', 'cls1':cls1[0]['travel'],  'cls2':cls2[0]['travel'],  'cls3':cls3[0]['travel'],   'cls4':cls4[0]['travel'],  'cls5':cls5[0]['travel'],  'cls6':cls6[0]['travel'],'cls7':0, 'sum':self.sum_travel},
                             {'name':'Үүнээс: эмэгтэй',       'cls1':cls1[0]['travel_f'],'cls2':cls2[0]['travel_f'],'cls3':cls3[0]['travel_f'],         'cls4':cls4[0]['travel_f'],'cls5':cls5[0]['travel_f'],'cls6':cls6[0]['travel_f'],'cls7':0,'sum':self.sum_travel_f},
                             {'name':'Гадаадад суралцахаар явсан',     'cls1':cls1[0]['outer'],   'cls2':cls2[0]['outer'],   'cls3':cls3[0]['outer'],   'cls4':cls4[0]['outer'],   'cls5':cls5[0]['outer'],   'cls6':cls6[0]['outer'],  'cls7':0, 'sum':self.sum_outer},
                             {'name':'Үүнээс: эмэгтэй',                'cls1':cls1[0]['outer_f'], 'cls2':cls2[0]['outer_f'], 'cls3':cls3[0]['outer_f'], 'cls4':cls4[0]['outer_f'], 'cls5':cls5[0]['outer_f'], 'cls6':cls6[0]['outer_f'],'cls7':0, 'sum':self.sum_outer_f},
                             {'name':'Сургалтын төлбөрөө төлөөгүйгээс','cls1':cls1[0]['baldly'],  'cls2':cls2[0]['baldly'],  'cls3':cls3[0]['baldly'],  'cls4':cls4[0]['baldly'],  'cls5':cls5[0]['baldly'],  'cls6':cls6[0]['baldly'], 'cls7':0, 'sum':self.sum_baldly},
                             {'name':'Үүнээс: эмэгтэй',        'cls1':cls1[0]['baldly_f'],'cls2':cls2[0]['baldly_f'],'cls3':cls3[0]['baldly_f'],        'cls4':cls4[0]['baldly_f'],'cls5':cls5[0]['baldly_f'],'cls6':cls6[0]['baldly_f'],'cls7':0, 'sum':self.sum_baldly_f},
                             {'name':'Сурлагаар хасагдсан',    'cls1':cls1[0]['bad'],     'cls2':cls2[0]['bad'],     'cls3':cls3[0]['bad'],    'cls4':cls4[0]['bad'],     'cls5':cls5[0]['bad'],     'cls6':cls6[0]['bad'],   'cls7':0, 'sum':self.sum_bad},
                             {'name':'Үүнээс: эмэгтэй',        'cls1':cls1[0]['bad_f'],   'cls2':cls2[0]['bad_f'],   'cls3':cls3[0]['bad_f'],  'cls4':cls4[0]['bad_f'],   'cls5':cls5[0]['bad_f'],   'cls6':cls6[0]['bad_f'], 'cls7':0,'sum':self.sum_bad_f},
                             {'name':'Сахилгаар хасагдсан',    'cls1':cls1[0]['discipline'],  'cls2':cls2[0]['discipline'],  'cls3':cls3[0]['discipline'],    'cls4':cls4[0]['discipline'],  'cls5':cls5[0]['discipline'],  'cls6':cls6[0]['discipline'], 'cls7':0,'sum':self.sum_discipline},
                             {'name':'Үүнээс: эмэгтэй',        'cls1':cls1[0]['discipline_f'],'cls2':cls2[0]['discipline_f'],'cls3':cls3[0]['discipline_f'],  'cls4':cls4[0]['discipline_f'],'cls5':cls5[0]['discipline_f'],'cls6':cls6[0]['discipline_f'],'cls7':0,'sum':self.sum_discipline_f},
                             {'name':'Бусад шалтгаанаар',      'cls1':cls1[0]['l_other'],      'cls2':cls2[0]['l_other'],      'cls3':cls3[0]['l_other'],     'cls4':cls4[0]['l_other'],     'cls5':cls5[0]['l_other'],     'cls6':cls6[0]['l_other'],'cls7':0,'sum':self.sum_l_other},
                             {'name':'Үүнээс: эмэгтэй',        'cls1':cls1[0]['l_other_f'],    'cls2':cls2[0]['l_other_f'],    'cls3':cls3[0]['l_other_f'],   'cls4':cls4[0]['l_other_f'],   'cls5':cls5[0]['l_other_f'],   'cls6':cls6[0]['l_other_f'],'cls7':0,'sum':self.sum_l_other_f}]

            elif i == 2:
                uunees = ''
                sub_lines = [{'name':'Нэмэгдсэн бүгд', 'cls1':cls1[0]['a_sum'],  'cls2':cls2[0]['a_sum'],  'cls3':cls3[0]['a_sum'], 'cls4':cls4[0]['a_sum'],  'cls5':cls5[0]['a_sum'],  'cls6':cls6[0]['a_sum'],'cls7':0, 'sum':self.sum_a_all},
                             {'name':'Үүнээс: эмэгтэй','cls1':cls1[0]['a_sum_f'],'cls2':cls2[0]['a_sum_f'],'cls3':cls3[0]['a_sum_f'],'cls4':cls4[0]['a_sum_f'],'cls5':cls5[0]['a_sum_f'],'cls6':cls6[0]['a_sum_f'],'cls7':0, 'sum':self.sum_a_all_f}]
            elif i == 3:
                uunees = u'Үүнээс'
                sub_lines = [{'name':'Шинээр элссэн',   'cls1':cls1[0]['new_std'],  'cls2':cls2[0]['new_std'],  'cls3':cls3[0]['new_std'],   'cls4':cls4[0]['new_std'],  'cls5':cls5[0]['new_std'],  'cls6':cls6[0]['new_std'], 'cls7':0,'sum':self.sum_new_std},
                             {'name':'Үүнээс: эмэгтэй', 'cls1':cls1[0]['new_std_f'],'cls2':cls2[0]['new_std_f'],'cls3':cls3[0]['new_std_f'], 'cls4':cls4[0]['new_std_f'],'cls5':cls5[0]['new_std_f'],'cls6':cls6[0]['new_std_f'],'cls7':0, 'sum':self.sum_new_std},
                             {'name':'Өөр сургуулиас шилжиж ирсэн','cls1':cls1[0]['other_school'],'cls2':cls2[0]['other_school'],'cls3':cls3[0]['other_school'],'cls4':cls4[0]['other_school'],'cls5':cls5[0]['other_school'],'cls6':cls6[0]['other_school'],'cls7':0, 'sum':self.sum_other_school},
                             {'name':'Үүнээс: эмэгтэй', 'cls1':cls1[0]['other_school_f'], 'cls2':cls2[0]['other_school_f'], 'cls3':cls3[0]['other_school_f'], 'cls4':cls4[0]['other_school_f'], 'cls5':cls5[0]['other_school_f'], 'cls6':cls6[0]['other_school_f'],'cls7':0, 'sum':self.sum_other_school_f},
                             {'name':'Гадаадад суралцагчдаас шилжиж ирсэн','cls1':cls1[0]['foreign_std'],'cls2':cls2[0]['foreign_std'],'cls3':cls3[0]['foreign_std'],'cls4':cls4[0]['foreign_std'],'cls5':cls5[0]['foreign_std'],'cls6':cls6[0]['foreign_std'],'cls7':0, 'sum':self.sum_foreign_std},
                             {'name':'Үүнээс: эмэгтэй',  'cls1':cls1[0]['foreign_std_f'], 'cls2':cls2[0]['foreign_std_f'], 'cls3':cls3[0]['foreign_std_f'],  'cls4':cls4[0]['foreign_std_f'], 'cls5':cls5[0]['foreign_std_f'], 'cls6':cls6[0]['foreign_std_f'],'cls7':0, 'sum':self.sum_foreign_std_f},
                             {'name':'Бусад шалтгаанаар','cls1':cls1[0]['a_other'],  'cls2':cls2[0]['a_other'],  'cls3':cls3[0]['a_other'],  'cls4':cls4[0]['a_other'],  'cls5':cls5[0]['a_other'],  'cls6':cls6[0]['a_other'],'cls7':0,'sum':self.sum_a_other},
                             {'name':'Үүнээс: эмэгтэй',  'cls1':cls1[0]['a_other_f'],'cls2':cls2[0]['a_other_f'],'cls3':cls3[0]['a_other_f'],'cls4':cls4[0]['a_other_f'],'cls5':cls5[0]['a_other_f'],'cls6':cls6[0]['a_other_f'],'cls7':0,'sum':self.sum_a_other_f}]
            elif i == 4:
                uunees = ''
                sub_lines = [{'name':'Тайлан гаргах үеийн суралцагчдын тоо','cls1':cls1[0]['now'],  'cls2':cls2[0]['now'],  'cls3':cls3[0]['now'],  'cls4':cls4[0]['now'],  'cls5':cls5[0]['now'],  'cls6':cls6[0]['now'],'cls7':0,'sum':self.sum_now},
                             {'name':'Үүнээс: эмэгтэй','cls1':cls1[0]['now_f'],  'cls2':cls2[0]['now_f'],  'cls3':cls3[0]['now_f'],  'cls4':cls4[0]['now_f'],  'cls5':cls5[0]['now_f'],  'cls6':cls6[0]['now_f'],'cls7':0,'sum':self.sum_now_f}]
                
#            for sub_line in sub_lines:
                
            result.append({
                           'uunees':uunees,
                           'sub_lines':sub_lines
                           })


            
        return result
report_sxw.report_sxw(
    'report.db_8',
    'school.student',
    'addons/school/report/report_db_8.rml',
    parser=report_db_8,
    header=False)