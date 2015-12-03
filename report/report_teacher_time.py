# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

@author: ubs121
'''

import time
from report import report_sxw
import netsvc

logger = netsvc.Logger()

class report_teacher_time(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_teacher_time, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time':time,
            'semester': self.semester,
            'lines': self.get_lines,
        })
        self.context = context
        self.resTerm = None
        self.teacher = None
        
    def semester(self, form, teacher):
        self.teacher = teacher.id
        self.cr.execute("SELECT * FROM school_term WHERE id=" + str(form['term_id']))
        self.resTerm = self.cr.dictfetchall()[0]
        return self.resTerm['name']
    
    def get_lines(self, form):
        result = []
        self.cr.execute("SELECT * FROM school_offering WHERE thr_id = " + str(self.teacher))
        offerings = self.cr.dictfetchall()
        if offerings:
            for off in offerings:
                self.cr.execute("SELECT name FROM school_curriculum WHERE id = " + str(off['curr_id']))
                curr_name = self.cr.dictfetchone()['name']
                self.cr.execute("SELECT name FROM school_curr_line WHERE id = " + str(off['curr_sub_id']))
                sub_name = self.cr.dictfetchone()['name']
                self.cr.execute("SELECT * FROM school_teacher_consummation "\
                                "WHERE date BETWEEN '"\
                                + str(self.resTerm['date_start']) + "' AND '" + str(self.resTerm['date_stop']) + "' "\
                                "AND subject = " + str(off['curr_sub_id']))
                tchr_cons = self.cr.dictfetchall()
                subject = []
                if tchr_cons:
                    for i in tchr_cons:
                        self.cr.execute("SELECT name FROM hr_employee WHERE id = " + str(i['taught_thr']))
                        taught_thr = self.cr.dictfetchone()['name']
                        subject.append({
                                        'sedev':i['name'],
                                        'ognoo':i['date'],
                                        'helber':i['sub_type'],
                                        'tsag':i['taught_time'],
                                        'taught_thr':taught_thr
                                        }) 
                
                result.append({
                               'curr_name' : curr_name,
                               'sub_name' : sub_name,
                               'lec' : off['lec'],
                               'sem' : off['sem'],
                               'lab' : off['lab'],
                               'subject' : subject
                               })
        return result
    
report_sxw.report_sxw(
    'report.teacher_time',
    'hr.employee',
    'addons/school/report/report_teacher_time.rml',
    parser=report_teacher_time,
    header=False)
