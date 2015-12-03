# -*- encoding: utf-8 -*-
import wizard

d_form = u'''<?xml version="1.0"?>
            <form string="Дүнгийн тодорхойлолт хэвлэх">
                <field name="std" colspan="4"/>
            </form>'''

d_fields = {
    'std': {'string':u'Оюутан', 'type':'many2one', 'relation':'school.student', 
                'domain':[('grp_id','!=',None), ('presense','=','present'),],},
}

class wizard_print_grade_def(wizard.interface):
    def _get_defaults(self, cr, uid, data, context):
        
#        data['form']['date_from'] =  mx.DateTime.strptime(year_start_date,"%Y-%m-%d").strftime("%Y-%m-%d")
#        data['form']['date_to'] =  mx.DateTime.strptime(year_end_date,"%Y-%m-%d").strftime("%Y-%m-%d")
#        
        return data['form']
    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {'type':'form', 'arch':d_form, 'fields':d_fields, 'state':[('end',u'Болих','gtk-cancel'),('report',u'Хэвлэх','gtk-print')]}
        },
        'report': {
            'actions': [],
            'result': {'type':'print', 'report':'grade_def', 'state':'end'}
        },
    }
wizard_print_grade_def('school.grade.def')

