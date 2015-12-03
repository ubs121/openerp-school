# -*- encoding: utf-8 -*-
'''
Created on May 12, 2009

@author: ubs121
'''

from report import report_sxw
import netsvc
import itertools
import operator
import datetime

logger = netsvc.Logger()

class report_grade_def(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_grade_def, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'ognoo': self.get_date,
            'ovog': self.get_ovog,
            'ner': self.get_ner,
            'group': self.get_group,
            'hicheeliin_jil': self.get_hicheeliin_jil,
            'seq_number': self.get_seq_number,
        })
        self.context = context
        self.result = {}
        self.cnt = 1
        
    def get_date(self, form):
        self.cr.execute("SELECT * FROM school_student WHERE id=" + str(form['std']))
        resStd = self.cr.dictfetchall()
        self.cr.execute("SELECT * FROM res_partner_contact WHERE id=" + str(resStd[0]['contact_id']))
        resultSet = self.cr.dictfetchall()
        
        self.cr.execute("SELECT name FROM school_student_group WHERE id=" + str(resStd[0]['grp_id']))
        self.result['group'] = self.cr.dictfetchall()[0]['name']
        
#        q = "SELECT f.name FROM res_partner_function as f, res_partner_job as j WHERE f.id = 1 AND j.address_id = (SELECT id FROM res_partner_address as a WHERE a.name = (SELECT name FROM res_partner as p WHERE p.id = %s ))"

        self.result['ovog'] = resultSet[0]['first_name']
        self.result['ner'] = resultSet[0]['name']
        
        return datetime.datetime.now().strftime("%Y-%m-%d")  

    def get_seq_number(self):
        return self.pool.get('ir.sequence').get(self.cr, self.uid, 'grade.definition')
    def get_ovog(self):
        if self.result['ovog']:
            return self.result['ovog'] + u" овогтой "
        else:
            return ""
    def get_ner(self):
        return self.result['ner']
    def get_group(self):
        return self.result['group']
    
    def get_hicheeliin_jil(self, form):
        self.cr.execute("SELECT point, mark, gbook_id, term_id FROM school_gbook_line l WHERE l.std_id =" + str(form['std']))
        gbook_l = self.cr.dictfetchall()
        result = []
        if gbook_l:
            for i in gbook_l:   # hicheeliin id-r hicheeliin neriig avna
                self.cr.execute("SELECT sub_id, term_id FROM school_gbook WHERE id =" + str(i['gbook_id']))
                gbook = self.cr.dictfetchall()
                self.cr.execute("SELECT name FROM school_subject WHERE id =" + str(gbook[0]['sub_id']))
                sub_name = self.cr.fetchall()
                i['sub_name'] = sub_name[0][0]
                
                self.cr.execute("SELECT year_id FROM school_term WHERE id =" + str(i['term_id']))
                term = self.cr.dictfetchall()
                i['year_id'] = term[0]['year_id']
          
            gbook_l.sort(key=operator.itemgetter('year_id')) # year_id-aar n erembelj bn
    
            grped_by_year = []
            for key, items in itertools.groupby(gbook_l, operator.itemgetter('year_id')):   # jileer ylgah
                grped_by_year.append(list(items))
    
            set = []
            for year in grped_by_year:
                year.sort(key=operator.itemgetter('term_id'))
                grped_by_term = []
                for key, items in itertools.groupby(year, operator.itemgetter('term_id')):   # ylgasan jil dotroo term-eer ylgah
                    grped_by_term.append(list(items))
                set.append(grped_by_term)
            
            for s in set:
                self.cr.execute("SELECT date_start, date_stop FROM school_year WHERE id =" + str(s[0][0]['year_id']))
                year = self.cr.dictfetchall()
                
                semester = []
                for t in range(0, len(s)):
                    self.cr.execute("SELECT name FROM school_term WHERE id =" + str(s[t][0]['term_id']))  # term_id-r semesteriin neriig avj bn
                    term_name = self.cr.dictfetchall()
    
                    seq = 1
                    rating = 0.0
                    pnt_sum = 0.0
                    for i in s[t]:
                        i['seq'] = seq          # des dugaar
                        seq += 1
                        pnt_sum = pnt_sum + i['point']
                        
                    rating = float(pnt_sum / len(s[t]))   # rating dundaj olj bn
                    semester.append({"sem_name":term_name[0]['name'],
                                     "subjects":s[t],
                                     "rating":rating
                                     })
    
                result.append({"start" : year[0]['date_start'].split('-')[0],
                               "end" : year[0]['date_stop'].split('-')[0],
                               "semester" : semester
                               })
        return result     

report_sxw.report_sxw(
    'report.grade_def',
    'school.gbook.line',
    'addons/school/report/report_grade_def.rml',
    parser=report_grade_def,
    header=False)
