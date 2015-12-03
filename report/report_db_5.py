# -*- encoding: utf-8 -*-
'''
Created on Oct 26, 2009

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

class report_db_5(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_5, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time' : time,
            'hich_jil' : self.get_hich_jil,
            'abt_school' : self.abt_school,
            'school' : self.school,
            'title' : self.title,
            'city' : self.city,
            'district' : self.district,
            'by_angil' : self.get_by_angil,
            'last_lines' : self.last_lines,
        })
        self.cnt = 1
        self.city = ''
        self.school = ''
        self.title = ''
        self.district = ''
        
    def abt_school(self, form):
        reg_no = ''
        self.cr.execute("SELECT * FROM res_partner WHERE id="+str(form['school_id']))
        obj_rp = self.cr.dictfetchall()[0]
        if obj_rp:
            reg_no = obj_rp['register_no'] 
            self.school = obj_rp['name']
            self.title = obj_rp['title']
            if obj_rp['id']:
                self.cr.execute("SELECT * FROM res_partner_address WHERE partner_id="+str(obj_rp['id']))
                obj_rpa = self.cr.dictfetchall()[0]
                if obj_rpa['state_id']:
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
    def get_by_angil(self):
        result = []
        count=0

        for i in range(0,6):
            sub_lines = []
            if i == 0:
                name1 = ''
                name2 = ''
                sub_lines = [{'code':'dip','name':'Дипломын (дээд) боловсрол олгох ангид хичээл заадаг'},
                             {'code':'PhD','name':'Докторантурт хичээл заадаг'},
                             {'code':'M.A','name':'Магистрантурт хичээл заадаг'},
                             {'code':'B.A','name':'Бакалаврын дээд боловсрол олгох ангид хичээл заадаг'}]
            elif i == 1:
                name1 = u'Албан тушаал'
                name2 = ''
                sub_lines = [{'code':'lead','name':'Тэргүүлэх'},
                             {'code':'ass','name':'Зөвлөх'},
                             {'code':'cert','name':'Мэргэшсэн'},
                             {'code':'senior','name':'Ахлах'},
                             {'code':'prf','name':'Профессор'}]
            elif i == 2:
                name1 = u'Ажилласан'
                name2 = u'жил'
                sub_lines = [{'code1':'1','code2':'5','name':'1-5 жил'},
                             {'code1':'6','code2':'10','name':'6-10 жил'},
                             {'code1':'11','code2':'15','name':'11-15 жил'},
                             {'code1':'16','code2':'20','name':'16-20 жил'},
                             {'code1':'21','code2':'25','name':'21-25 жил'},
                             {'code1':'26','code2':'','name':'25-аас дээш жил'}]
            elif i == 3:
                name1 = u'Нас'
                name2 = ''
                sub_lines = [{'code1':'29','code2':'','name':'30 хүртэл настай'},
                             {'code1':'30','code2':'50','name':'30-50 настай'},
                             {'code1':'51','code2':'54','name':'51-54 настай'},
                             {'code1':'55','code2':'','name':'55 настай'},
                             {'code1':'56','code2':'59','name':'56-59 настай'},
                             {'code1':'60','code2':'','name':'60 настай'},
                             {'code1':'61','code2':'','name':'60-аас дээш настай'}]
            elif i == 4:
                name1 = u'Боловсролын'
                name2 = u'түвшин'
                sub_lines = [{'code':'dip','name':'Дипломын'},
                             {'code':'PhD','name':'Доктор'},
                             {'code':'M.A','name':'Магистр'},
                             {'code':'B.A','name':'Бакалавр'}]
            elif i == 5:
                name1 = u'Мэргэжлийн'
                name2 = u'чиглэл'
                self.cr.execute("SELECT id, name FROM school_teacher_profession")
                teacher_profs = self.cr.dictfetchall()
                for prof in teacher_profs:
                    sub_lines.append({
                                      'code':prof['id'] or '',
                                      'name':prof['name'] or ''
                                      })
#            else:
#                name = ''
            lines = []
            come = True
            for sub_line in sub_lines:
                if i == 0:
                    sub_query = "LEFT JOIN school_curriculum as curr ON curr.id = offer.curr_id WHERE curr.degree = '"+str(sub_line['code'])+"'"
                    uzuulelt = sub_line['name']
                    print "uzuulelt:  ",uzuulelt
                elif i == 1:
                    sub_query = "WHERE emp.rank = '"+str(sub_line['code'])+"'"
                    uzuulelt = sub_line['name']
                elif i == 2:
                    if sub_line['code2']:
                        sub_query = "WHERE emp.worked BETWEEN "+str(sub_line['code1'])+" AND "+str(sub_line['code2'])
                    else:
                        sub_query = "WHERE emp.worked >= "+str(sub_line['code1'])
                    uzuulelt = sub_line['name']
                elif i == 3:
                    if sub_line['code1'] == '29':
                        sub_query = "WHERE extract(years from AGE(emp.birthday)) <= "+str(sub_line['code1'])
                    elif sub_line['code1'] == '55' or sub_line['code1'] == '60':
                        sub_query = "WHERE extract(years from AGE(emp.birthday)) = "+str(sub_line['code1'])
                    elif sub_line['code1'] == '61':
                        sub_query = "WHERE extract(years from AGE(emp.birthday)) >= "+str(sub_line['code1'])
                    else:
                        sub_query = "WHERE extract(years from AGE(emp.birthday)) BETWEEN "+str(sub_line['code1'])+" AND "+str(sub_line['code2'])
                    uzuulelt = sub_line['name']
                elif i == 4:
                    sub_query = "WHERE emp.degree = '"+str(sub_line['code'])+"'"
                    uzuulelt = sub_line['name']
                elif i == 5:
                    sub_query = "WHERE emp.profession_id = '"+str(sub_line['code'])+"'"
                    uzuulelt = sub_line['name']
                
                zahi = 0
                zahi_f = 0
                ded_zahi = 0
                ded_zahi_f = 0
                hariya_sur_zahi = 0
                hariya_sur_zahi_f = 0
                hariya_sur_ded_zahi = 0
                hariya_sur_ded_zahi_f = 0
                sur_alba = 0
                sur_alba_f = 0
                basic_thr = 0
                time_thr = 0
                dep_mngr = 0
                dekan = 0
                basic_thr_f = 0
                time_thr_f = 0
                dep_mngr_f = 0
                dekan_f = 0
                self.cr.execute("SELECT emp.gender,emp.category_id as cat \
                            FROM hr_employee as emp \
                            LEFT JOIN school_offering as offer ON emp.id = offer.teacher_id \
                            LEFT JOIN school_teacher_profession as prof ON prof.id = emp.profession_id \
                            "+str(sub_query)+" \
                            GROUP BY emp.gender,emp.category_id")
                offs = self.cr.dictfetchall()
                
                for off in offs:
#                    print off['pos_name'],
#                    if off['pos_name'] == u'Захирал':
#                        zahi += 1
#                        if off['gender'] == 'female':
#                            zahi_f +=1
#                    if off['pos_name'] == u'Дэд захирал':
#                        ded_zahi += 1
#                        if off['gender'] == 'female':
#                            ded_zahi_f +=1
#                    if off['pos_name'] == u'Харьяа сургуулийн захирал':
#                        hariya_sur_zahi += 1
#                        if off['gender'] == 'female':
#                            hariya_sur_zahi_f +=1
#                    if off['pos_name'] == u'Харьяа сургуулийн дэд захирал':
#                        hariya_sur_ded_zahi += 1
#                        if off['gender'] == 'female':
#                            hariya_sur_ded_zahi_f +=1
#                    if off['pos_name'] == u'Сургалтын албаны дарга':
#                        sur_alba += 1
#                        if off['gender'] == 'female':
#                            sur_alba_f +=1
#                    
                    if off['cat']:
                        self.cr.execute("SELECT name FROM hr_employee_category WHERE id = "+str(off['cat']))
                        cat_name = self.cr.dictfetchone()['name']
                        if cat_name == u'Үндсэн багш':
                            basic_thr += 1
                            if off['gender'] == 'female':
                                basic_thr_f += 1
                            if cat_name == u'Декан':
                                dekan += 1
                                if off['gender'] == 'female':
                                    dekan_thr_f += 1
                            if cat_name == u'Тэнхмийн эрхлэгч':
                                dep_mngr += 1
                                if off['gender'] == 'female':
                                    dep_mngr_thr_f += 1
                        if cat_name == u'Цагийн багш':
                            time_thr += 1
                            if off['gender'] == 'female':
                                time_thr_f += 1
                        if cat_name == u'Захирал':
                            zahi += 1
                            if off['gender'] == 'female':
                                zahi_f +=1
                        if cat_name == u'Дэд захирал':
                            ded_zahi += 1
                            if off['gender'] == 'female':
                                ded_zahi_f +=1
                        if cat_name == u'Харьяа сургуулийн захирал':
                            hariya_sur_zahi += 1
                            if off['gender'] == 'female':
                                hariya_sur_zahi_f +=1
                        if cat_name == u'Харьяа сургуулийн дэд захирал':
                            hariya_sur_ded_zahi += 1
                            if off['gender'] == 'female':
                                hariya_sur_ded_zahi_f +=1
                        if cat_name == u'Сургалтын албаны дарга':
                            sur_alba += 1
                            if off['gender'] == 'female':
                                sur_alba_f +=1

                                
                self.cnt += 1
                lines.append({
                              'uzuulelt':uzuulelt or '',
                              'cnt':self.cnt or '',
                              'zahi':zahi or '',
                               'zahi_f':zahi_f or '',
                               'ded_zahi':ded_zahi or '',
                               'ded_zahi_f':ded_zahi_f or '',
                               'hariya_sur_zahi':hariya_sur_zahi or '',
                               'hariya_sur_zahi_f':hariya_sur_zahi_f or '',
                               'hariya_sur_ded_zahi':hariya_sur_ded_zahi or '',
                               'hariya_sur_ded_zahi_f':hariya_sur_ded_zahi_f or '',
                               'sur_alba':sur_alba or '',
                               'sur_alba_f':sur_alba_f or '',
                               'basic_thr':basic_thr or '',
                               'basic_thr_f':basic_thr_f or '',
                               'time_thr':time_thr or '',
                               'time_thr_f':time_thr_f or '',
                               'dekan':dekan or '',
                               'dekan_f':dekan_f or '',
                               'dep_mngr':dep_mngr or '',
                               'dep_mngr_f':dep_mngr_f or '',
                              })
            result.append({
                           'name1':name1,
                           'name2':name2,
                           'lines':lines
                           })
#        for val in result: 
#            print "result : ",val['name1']
        
        return result
    def last_lines(self, form):
        self.cnt += 1
        res = [{'code':'retired','name':'Тэтгэврээ тогтоолгоод ажиллаж байгаа','cnt':self.cnt},
               {'code':'badge','name':'Төрийн одонтой','cnt':self.cnt+1},
               {'code':'terguunii','name':'Боловсролын тэргүүний ажилтан','cnt':self.cnt+2},
               {'code':'dotoodod','name':'Өнгөрсөн хичээлийн жилд дотоодод мэргэжил дээшлүүлсэн','cnt':self.cnt+3},
               {'code':'gadaadad','name':'Өнгөрсөн хичээлийн жилд гадаадад мэргэжил дээшлүүлсэн','cnt':self.cnt+4},
               {'code':'dot_sanaltai','name':'Төвлөрсөн, бүсчилсэн шугамаар дотоодод мэргэжил дээшлүүлэх саналтай','cnt':self.cnt+5},
               {'code':'gad_sanaltai','name':'Төвлөрсөн, бүсчилсэн шугамаар гадаадад мэргэжил дээшлүүлэх саналтай','cnt':self.cnt+6}]
        return res
report_sxw.report_sxw(
    'report.db_5',
    'hr.employee',
    'addons/school/report/report_db_5.rml',
    parser=report_db_5, 
    header=False)