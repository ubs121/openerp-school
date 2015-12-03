# -*- encoding: utf-8 -*-
import wizard
import pooler

b_form = u'''<?xml version="1.0"?>
<form string="'Б' маягт хэвлэх">
    <field name="year" colspan="4"/>
    <field name="std_grp" colspan="4"/>
</form>'''

b_fields = {
    'year': {'string': u'Хичээлийн жил', 'type': 'many2one', 'relation': 'school.year'},
    'std_grp': {'string':u'Групп', 'type':'many2one', 'relation':'school.student.group', 
                'required':True},
#                'required':True, 'domain':[('year','=', 1), ('graduate','=',True)]},
}

class wizard_bsheet(wizard.interface):
    def _get_defaults(self, cr, uid, data, context):
        current_year = pooler.get_pool(cr.dbname).get('school.year').find(cr, uid)
        data['form']['year'] = current_year
        #stdgrp_obj=pooler.get_pool(cr.dbname).get('school.student.group')
#        b_fields['std_grp']['domain'] = [('year','=', data['form']['year']), ('graduate','=',True)]
        return data['form']

    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {'type':'form', 'arch':b_form, 'fields':b_fields, 'state':[('end',u'Болих','gtk-cancel'),('report',u'Хэвлэх','gtk-print')]}
        },
        'report': {
            'actions': [],
            'result': {'type':'print', 'report':'bsheet', 'state':'end'}
        },
    }
wizard_bsheet('bsheet.report')

