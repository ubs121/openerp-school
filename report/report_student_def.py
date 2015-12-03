# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

@author: ubs121
'''

from report import report_sxw
import datetime
import netsvc

logger=netsvc.Logger()

class report_student_def(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_student_def, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'ognoo': self.get_date,
            'ovog': self.get_ovog,
            'ner': self.get_ner,
            'year': self.get_year,
            'school_name': self.get_school_name,
            'group': self.get_group,
            'seq_number': self.get_seq_number,
        })
        self.context = context
        self.result = {}
        
    def get_date(self, form):
        self.cr.execute("SELECT * FROM school_student WHERE id="+str(form['std']))
        resStd=self.cr.dictfetchall()
        self.cr.execute("SELECT * FROM res_partner_contact WHERE id="+str(resStd[0]['contact_id']))
        resultSet=self.cr.dictfetchall()
        self.cr.execute("SELECT * FROM res_partner WHERE id="+str(form['school_id']))
        self.result['school_name'] = self.cr.dictfetchall()[0]['name']
        self.cr.execute("SELECT name FROM school_student_group WHERE id="+str(resStd[0]['grp_id']))
        self.result['group'] = self.cr.dictfetchall()[0]['name']
        self.result['ovog'] = resultSet[0]['first_name']
        self.result['ner'] = resultSet[0]['name']
        return datetime.datetime.now().strftime("%Y-%m-%d")  

    def get_ovog(self):
        if self.result['ovog']:
            return self.result['ovog'] + u" овогтой "
        else:
            return ""
    def get_ner(self):
        return self.result['ner']
    def get_year(self, form):
        self.cr.execute("SELECT extract(years from date_start) as start,extract(years from date_stop) as stop FROM school_year WHERE id="+str(form['year']))
        year=self.cr.dictfetchall()[0]
        res = str(int(year['start']))+" - "+str(int(year['stop']))
        return res
    def get_school_name(self):
        return self.result['school_name']
    def get_group(self):
        return self.result['group']
    def get_seq_number(self):
        return self.pool.get('ir.sequence').get(self.cr, self.uid, 'student.definition')

report_sxw.report_sxw(
    'report.student_def',
    'school.student',
    'addons/school/report/report_student_def.rml',
    parser=report_student_def, 
    header=False)
