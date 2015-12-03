# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

@author: ubs121
'''

import time
from report import report_sxw
import netsvc

logger=netsvc.Logger()

class report_print_gbook(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_print_gbook, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time':time,
            'lines':self.get_lines,
        })
        self.context = context
        self.gbook_id = None
    
    def get_lines(self, gbook):
        result = []
        self.cr.execute("SELECT * FROM school_gbook_line WHERE gbook_id="+str(gbook.id))
        self.gbook_line = self.cr.dictfetchall()
        cnt = 0
        for i in self.gbook_line:
            self.cr.execute("SELECT name FROM res_partner_contact WHERE id = (SELECT contact_id FROM school_student WHERE id="+str(i['std_id'])+")")
            std_name = self.cr.dictfetchone()['name']
            cnt += 1
            result.append({
                           'std_name':std_name,
                           'p1':i['p1'],
                           'p2':i['p2'],
                           'p3':i['p3'],
                           'point':i['point'],
                           'mark':i['mark'],
                           'dd':cnt,
                           })
        return result
    
report_sxw.report_sxw(
    'report.print_gbook',
    'school.gbook',
    'addons/school/report/report_print_gbook.rml',
    parser=report_print_gbook, 
    header=False)
