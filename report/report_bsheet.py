# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

@author: ub121
'''

import time
from report import report_sxw
import pooler
import netsvc


logger=netsvc.Logger()

class report_bsheet(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_bsheet, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_students': self.get_students,
            'get_group': self.get_group,
        })
        self.context = context
     
    def get_group(self, form):
        return self.pool.get('school.student.group').read(self.cr, self.uid, [form['std_grp']], ['id', 'name'])[0]['name']
        
    def get_students(self, form):
        result = []
        # form['std_grp'] ангийн оюутнуудын дүн
        std1 = {'no':1, 'name': u'Ууганбаяр', 'regno': u'ЛЖ79011218', 'dipno':'111' }
        std2 = {'no':2, 'name': u'Болормаа', 'regno': u'УБ79011218', 'dipno':'222' }
        
        result.append(std1)
        result.append(std2)
        return result

report_sxw.report_sxw(
    'report.bsheet',
    'school.student.group',
    'addons/school/report/report_b.rml',
    parser=report_bsheet, 
    header=False)
