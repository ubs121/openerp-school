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

class report_db_1(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_db_1, self).__init__(cr, uid, name, context)
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
            'sum_all' : self.sum_all,
            'sum_female' : self.sum_female
        })
        self.curriculums = None
        self.study_type = None
        self.year = None
        self.sum_all = 0
        self.sum_female = 0
        self.school_name = ''
        self.type = ''
        self.city_name = ''
        self.district_name = ''
        
    def abt_school(self, form):
        reg_no = ''
        self.cr.execute("SELECT * FROM res_partner WHERE id="+str(form['school_id']))
        obj_rp = self.cr.dictfetchall()
        if obj_rp:
            reg_no = obj_rp[0]['register_no'] 
            self.school_name = obj_rp[0]['name']
            self.type = obj_rp[0]['title']
            self.cr.execute("SELECT * FROM res_partner_address WHERE partner_id="+str(obj_rp[0]['id']))
            obj_rpa = self.cr.dictfetchall()
            if obj_rpa:
                if obj_rpa[0]['state_id']:
                    self.cr.execute("SELECT name FROM res_country_state WHERE id="+str(obj_rpa[0]['state_id']))
                    obj_rcs = self.cr.dictfetchall()
                    if obj_rcs:
                        self.city_name = obj_rcs[0]['name']
                self.district_name = obj_rpa[0]['city']
        return reg_no
    def school(self):
        return self.school_name
    def title(self):
        return self.type
    def city(self):
        return self.city_name
    def district(self):
        return self.district_name
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
        self.cr.execute("SELECT * FROM school_curriculum WHERE study_type = '"+str(self.study_type)+"' ORDER BY degree")
        curriculums = self.cr.dictfetchall()
        
        for curr in curriculums:
            self.cr.execute("SELECT * FROM school_profession WHERE id="+str(curr['prof_id']))
            profession = self.cr.dictfetchall()[0]

            self.cr.execute("SELECT cls, contact_id, grp_id, admitted_date, pre_enroll, is_graduate FROM school_student "\
                            "WHERE curr_id='"+str(curr['id'])+"' "\
                            "AND presense='present' "\
                            "Group by cls, contact_id, grp_id, admitted_date, pre_enroll, is_graduate")
            contact_ids = self.cr.dictfetchall()
            contact_ids.sort(key=operator.itemgetter('cls'))
            
            grped_by_grp_id = []
            for key, items in itertools.groupby(contact_ids, operator.itemgetter('grp_id')):
                grped_by_grp_id.append(list(items))
            
            all = 0
            female = 0
            grp = [ {'all':'','female':''} ] * 7
            adm = []
            all_adm_f = 0
            all_grad_female = 0
            adm_non_worker = []
            adm_worker = []
            adm_k12 = []
            adm_other = []
            graduate = []
            for grped in grped_by_grp_id:
                grped_cont = []
                for i in grped:
                    grped_cont.append(i['contact_id'])
                    if i['admitted_date']:
                        if self.year['date_start'] <= i['admitted_date'] and self.year['date_stop'] > i['admitted_date']:
                            adm.append(i['contact_id'])
                            if i['pre_enroll'] == 'k12':
                                adm_k12.append(i['pre_enroll'])
                            elif i['pre_enroll'] == 'non-worker':
                                adm_non_worker.append(i['pre_enroll'])
                            elif i['pre_enroll'] == 'worker':
                                adm_worker.append(i['pre_enroll'])
                            else:
                                adm_other.append(i['pre_enroll'])
                        if i['is_graduate'] == True:
                            graduate.append(i['contact_id'])

                if grped_cont:
                    self.cr.execute("SELECT count(p.id) FROM res_partner_contact AS p "\
                                "WHERE p.id in ("+ ','.join(map(str, grped_cont))+") AND p.gender = 'f'")
                    grped_female = self.cr.dictfetchall()[0]['count']
                else:
                    grped_female = 0    
                grp[grped[0]['cls']] = {'all':len(grped),'female':grped_female}
                all += len(grped)
                female += grped_female

                if adm:
                    self.cr.execute("SELECT count(p.id) FROM res_partner_contact AS p "\
                                "WHERE p.id in ("+ ','.join(map(str, adm))+") AND p.gender = 'f'")
                    adm_female = self.cr.dictfetchall()[0]['count']
                else:
                    adm_female = 0
                all_adm_f += adm_female 
                
                if graduate:
                    self.cr.execute("SELECT count(p.id) FROM res_partner_contact AS p "\
                                "WHERE p.id in ("+ ','.join(map(str, graduate))+") AND p.gender = 'f'")
                    grad_female = self.cr.dictfetchall()[0]['count']
                else:
                    grad_female = 0
                all_grad_female += grad_female 
            
            self.sum_all = self.sum_all + all   
            self.sum_female = self.sum_female + female    

            result.append({
                           'index' : profession['index'],
                           'name' : profession['name'],
                           'degree' : curr['degree'],
                           'all' : all or '',
                           'female' : female or '',
                           'grp_0' : grp[0],
                           'grp_1' : grp[1],
                           'grp_2' : grp[2],
                           'grp_3' : grp[3],
                           'grp_4' : grp[4],
                           'grp_5' : grp[5],
                           'grp_6' : grp[6],
                           'adm_all' : len(adm) or '',
                           'adm_female' : all_adm_f or '',
                           'adm_k12' : len(adm_k12) or '',
                           'adm_other' : len(adm_other) or '',
                           'adm_non-worker' : len(adm_non_worker) or '',
                           'adm_worker' : len(adm_worker) or '',
                           'graduate' : len(graduate) or '',
                           'grad_female' : all_grad_female or '',
                           })
            male = 0
            female = 0
        return result
    
    def sum_all(self):
        return self.sum_all
    def sum_female(self):
        return self.sum_female
report_sxw.report_sxw(
    'report.db_1',
    'school.student',
    'addons/school/report/report_db_1.rml',
    parser=report_db_1, 
    header=False)
