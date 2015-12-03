# -*- encoding: utf-8 -*-
import wizard

dip_form = u'''<?xml version="1.0"?>
            <form string="Дипломын Хавсралт хэвлэх">
                <field name="std" colspan="4"/>
            </form>'''

dip_fields = {
    'std': {'string':u'Оюутан', 'type':'many2one', 'relation':'school.student', 
                'domain':[('is_graduate','=',True), ('presense','=','present'),],
                #'required':True,
                }
}

class wizard_diploma(wizard.interface):
    def _get_defaults(self, cr, uid, data, context):
        #dip_fields['std'] = [1]
        return data['form']

    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {'type':'form', 'arch':dip_form, 'fields':dip_fields, 'state':[('end',u'Болих','gtk-cancel'),('report',u'Хэвлэх','gtk-print')]}
        },
        'report': {
            'actions': [],
            'result': {'type':'print', 'report':'diploma', 'state':'end'}
        },
    }
wizard_diploma('diploma.report')

