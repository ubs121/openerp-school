# -*- encoding: utf-8 -*-
import wizard
import pooler


d_form = u'''<?xml version="1.0"?>
            <form string="Оюутны тодорхойлолт хэвлэх">
                <field name="std" colspan="4"/>
                <field name="school_id" colspan="4" />
                <field name="year" colspan="4"/>
            </form>'''

d_fields = {
    'std': {'string':u'Оюутан', 'type':'many2one', 'relation':'school.student', 
                'domain':[('grp_id','!=',None), ('presense','=','present'),],},
    'school_id': {'string':u'Сургууль', 'type':'many2one', 'relation':'res.company','required': True},
    'year': {'string': u'Хичээлийн жил', 'type': 'many2one', 'relation': 'school.year'},
}

class wizard_print_student_def(wizard.interface):
    def _get_defaults(self, cr, uid, data, context):
        current_year = pooler.get_pool(cr.dbname).get('school.year').find(cr, uid)
        data['form']['year'] = current_year
        user = pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, uid, context=context)
        
        if user.company_id:
            company_id = user.company_id.id
        else:
            company_id = pooler.get_pool(cr.dbname).get('res.company').search(cr, uid, [('parent_id', '=', False)])[0]
        
        current_year = pooler.get_pool(cr.dbname).get('school.year').find(cr, uid)
        data['form']['school_id'] = company_id
        
        return data['form']
    
    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {'type':'form', 'arch':d_form, 'fields':d_fields, 'state':[('end',u'Болих','gtk-cancel'),('report',u'Хэвлэх','gtk-print')]}
        },
        'report': {
            'actions': [],
            'result': {'type':'print', 'report':'student_def', 'state':'end'}
        },
    }
wizard_print_student_def('school.student.def')

